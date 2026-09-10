"""Restricted Nokia simulator adapter. Credentials never enter evidence records."""

import asyncio
import math
import secrets
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import ClassVar
from urllib.parse import parse_qs, urljoin, urlparse

import httpx


class ProviderCheckCancelled(Exception):
    """Stop a multi-request provider flow after the current HTTP call returns."""


class NokiaAvailability:
    """Shared, single-process cooldown; not a claim about the account's quota reset."""

    def __init__(self):
        self.blocked_until = 0
        self.last_status = None

    def snapshot(self):
        seconds = max(0, math.ceil(self.blocked_until - time.time()))
        return {"status": "RATE_LIMITED" if seconds else "NOT_CHECKED" if self.last_status is None else
                "RETRY_AVAILABLE" if self.last_status == 429 else
                "LAST_CHECK_SUCCEEDED" if self.last_status == 200 else "LAST_CHECK_FAILED",
                "retry_after_seconds": seconds, "last_http_status": self.last_status,
                "reset_confirmed": False}

    def rate_limited(self, response):
        retry = response.headers.get("retry-after", "")
        try:
            seconds = float(retry) if retry.isdigit() else parsedate_to_datetime(retry).timestamp() - time.time()
            seconds = max(1, min(seconds, 86400))
        except (ValueError, TypeError, OverflowError):
            seconds = 60
        self.blocked_until = max(self.blocked_until, time.time() + seconds)
        self.last_status = 429
        return math.ceil(seconds)


class NokiaGateway:
    HOST = "network-as-code.p.rapidapi.com"
    ROUTES: ClassVar[dict[str, tuple[str, str]]] = {
        "sim_swap": ("/passthrough/camara/v1/sim-swap/sim-swap/v0/check", "swapped"),
        "device_swap": ("/passthrough/camara/v1/device-swap/device-swap/v1/check", "swapped"),
        "roaming": ("/device-status/device-roaming-status/v1/retrieve", "roaming"),
        "reachability": ("/device-status/device-reachability-status/v1/retrieve", "reachable"),
        "number_verification": ("/passthrough/camara/v1/number-verification/number-verification/v0/verify", "devicePhoneNumberVerified"),
    }
    def __init__(self, api_key, client, availability=None):
        self.api_key = api_key
        self.client = client
        self.availability = availability or NokiaAvailability()

    async def check(self, tool, phone, should_stop=None):
        start = time.perf_counter()
        if tool not in self.ROUTES or phone not in {"+99999991000", "+99999991001"}:
            return {"tool": tool, "source": "NOKIA_SANDBOX", "status": "UNSUPPORTED",
                    "subject": phone, "data": {}, "error": "Unsupported tool or simulator subject", "latency_ms": 0}
        path, field = self.ROUTES[tool]
        if self.availability.snapshot()["status"] == "RATE_LIMITED":
            return {"tool": tool, "source": "NOKIA_SANDBOX", "status": "UNKNOWN", "subject": phone,
                    "data": {}, "error": "NOKIA_COOLDOWN", "http_status": None, "request_made": False,
                    "retry_after_seconds": self.availability.snapshot()["retry_after_seconds"],
                    "endpoint": path, "latency_ms": 0, "observed_at": datetime.now(timezone.utc).isoformat()}
        payload = ({"phoneNumber": phone, "maxAge": 120} if tool in {"sim_swap", "device_swap"}
                   else {"device": {"phoneNumber": phone}})
        data, status, error, http_status = {}, "UNKNOWN", None, None
        failure_step, retry_after = None, None
        try:
            self._raise_if_cancelled(should_stop)
            if tool == "number_verification":
                response = await asyncio.wait_for(self._verify_number(phone, path, should_stop), timeout=20)
            else:
                response = await self.client.post(
                    "https://" + self.HOST + path,
                    headers=self._headers(), json=payload, timeout=8, follow_redirects=False,
                )
            http_status = response.status_code
            response.raise_for_status()
            body = response.json()
            if type(body.get(field)) is not bool:
                raise ValueError("Invalid provider response")
            data, status = {field: body[field]}, "SUCCESS"
            if self.availability.snapshot()["status"] != "RATE_LIMITED":
                self.availability.last_status = http_status
        except (httpx.HTTPError, ValueError, AttributeError, KeyError, TypeError,
                TimeoutError, ProviderCheckCancelled) as exc:
            error = type(exc).__name__
            self.availability.last_status = 0
            if isinstance(exc, httpx.HTTPStatusError):
                http_status = exc.response.status_code
                self.availability.last_status = http_status
                failure_step = exc.request.url.path
                if http_status == 429:
                    error = "NOKIA_RATE_LIMITED"
                    retry_after = self.availability.rate_limited(exc.response)
        return {"tool": tool, "source": "NOKIA_SANDBOX", "status": status,
                "subject": phone, "data": data, "error": error, "http_status": http_status,
                "failure_step": failure_step, "retry_after_seconds": retry_after, "request_made": True,
                "latency_ms": round((time.perf_counter() - start) * 1000, 2),
                "observed_at": datetime.now(timezone.utc).isoformat(), "endpoint": path}

    def _headers(self):
        return {"x-rapidapi-key": self.api_key, "x-rapidapi-host": self.HOST}

    @staticmethod
    def _raise_if_cancelled(should_stop):
        if should_stop and should_stop():
            raise ProviderCheckCancelled

    async def _verify_number(self, phone, path, should_stop=None):
        base = "https://" + self.HOST
        credentials = await self.client.get(base + "/oauth2/v1/auth/clientcredentials",
                                             headers=self._headers(), timeout=8, follow_redirects=False)
        self._raise_if_cancelled(should_stop)
        credentials.raise_for_status()
        client_id = credentials.json()["client_id"]
        metadata = await self.client.get(base + "/.well-known/oauth-authorization-server",
                                         headers=self._headers(), timeout=8, follow_redirects=False)
        self._raise_if_cancelled(should_stop)
        metadata.raise_for_status()
        endpoint = metadata.json()["fast_flow_csp_auth_endpoint"]
        allowed = {"nb-auth.nac-runtime-stg-eu.g002.saas.nokia.com",
                   "camara-auth.nac-runtime-stg-eu.g002.saas.nokia.com"}

        def permitted(url):
            parsed = urlparse(url)
            return parsed.scheme == "https" and parsed.hostname in allowed and parsed.port in (None, 443) and not parsed.username

        if not permitted(endpoint):
            raise ValueError("Untrusted OAuth endpoint")
        state, nonce = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
        callback = "http://127.0.0.1:8765/nokia-verification-probe"
        response = await self.client.get(endpoint, params={
            "client_id": client_id, "scope": "dpv:FraudPreventionAndDetection number-verification:verify",
            "response_type": "code", "redirect_uri": callback, "login_hint": phone,
            "prompt": "none", "state": state, "nonce": nonce,
        }, timeout=8, follow_redirects=False)
        for _ in range(6):
            self._raise_if_cancelled(should_stop)
            if response.status_code >= 400:
                response.raise_for_status()
            location = response.headers.get("location")
            if not location or response.status_code not in (302, 303, 307):
                raise ValueError("Incomplete simulator authorization")
            location = urljoin(str(response.url), location)
            parsed = urlparse(location)
            query = parse_qs(parsed.query)
            if location.split("?")[0] == callback:
                if query.get("state") != [state] or len(query.get("code", [])) != 1:
                    raise ValueError("Invalid OAuth callback")
                self._raise_if_cancelled(should_stop)
                return await self.client.post(base + path, headers=self._headers(),
                    params={"code": query["code"][0], "state": state},
                    json={"phoneNumber": phone}, timeout=8, follow_redirects=False)
            if not permitted(location):
                raise ValueError("Untrusted OAuth redirect")
            self._raise_if_cancelled(should_stop)
            response = await self.client.get(location, timeout=8, follow_redirects=False)
        raise ValueError("OAuth redirect limit")
