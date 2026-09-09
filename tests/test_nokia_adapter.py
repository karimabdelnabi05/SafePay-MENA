import asyncio
from urllib.parse import parse_qs

import httpx
import pytest

from app.services.nokia import NokiaGateway


def test_sim_swap_preserves_provider_result_without_inventing_swap_age():
    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(
            lambda request: httpx.Response(200, json={"swapped": True})
        )) as client:
            gateway = NokiaGateway(api_key="test-key", client=client)
            evidence = await gateway.check("sim_swap", "+99999991000")
            assert evidence["status"] == "SUCCESS"
            assert evidence["source"] == "NOKIA_SANDBOX"
            assert evidence["data"] == {"swapped": True}
            assert evidence["subject"] == "+99999991000"
            assert "test-key" not in str(evidence)
    asyncio.run(run())


@pytest.mark.parametrize("tool,field,path", [
    ("device_swap", "swapped", "/device-swap/device-swap/v1/check"),
    ("roaming", "roaming", "/device-status/device-roaming-status/v1/retrieve"),
    ("reachability", "reachable", "/device-status/device-reachability-status/v1/retrieve"),
])
def test_each_tool_exposes_only_its_independent_evidence(tool, field, path):
    def respond(request):
        assert request.url.path.endswith(path)
        return httpx.Response(200, json={field: False})

    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
            result = await NokiaGateway("test-key", client).check(tool, "+99999991001")
            assert result["data"] == {field: False}
    asyncio.run(run())


def test_real_subscriber_number_is_rejected_before_network_access():
    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(
            lambda request: pytest.fail("Real subscriber must not be queried")
        )) as client:
            result = await NokiaGateway("test-key", client).check("sim_swap", "+966501234567")
            assert result["status"] == "UNSUPPORTED"
    asyncio.run(run())


@pytest.mark.parametrize("valid_state", [True, False])
def test_number_verification_requires_bound_oauth_callback(valid_state):
    def respond(request):
        path = request.url.path
        if path.endswith("clientcredentials"):
            return httpx.Response(200, json={"client_id": "client", "client_secret": "secret"})
        if "well-known" in path:
            return httpx.Response(200, json={"fast_flow_csp_auth_endpoint":
                "https://nb-auth.nac-runtime-stg-eu.g002.saas.nokia.com/oauth2/v1/retrieve_csp_auth_url"})
        if path.endswith("retrieve_csp_auth_url"):
            query = parse_qs(request.url.query.decode())
            state = query["state"][0] if valid_state else "wrong-session"
            return httpx.Response(302, headers={"location": query["redirect_uri"][0] + "?code=private-code&state=" + state})
        if path.endswith("/verify"):
            assert valid_state, "Invalid state must not reach verification"
            return httpx.Response(200, json={"devicePhoneNumberVerified": True})
        pytest.fail("Unexpected network request")

    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
            evidence = await NokiaGateway("test-key", client).check("number_verification", "+99999991000")
            assert evidence["status"] == ("SUCCESS" if valid_state else "UNKNOWN")
            if valid_state:
                assert evidence["data"] == {"devicePhoneNumberVerified": True}
            assert "private-code" not in str(evidence)
            assert "secret" not in str(evidence)
    asyncio.run(run())


@pytest.mark.parametrize("failure", ["timeout", "invalid_json", "invalid_boolean", "unauthorized", "rate_limited"])
def test_provider_failure_is_unknown_never_a_clean_result(failure):
    def respond(request):
        if failure == "timeout":
            raise httpx.ReadTimeout("upstream timeout", request=request)
        if failure == "invalid_json":
            return httpx.Response(200, text="not JSON")
        if failure == "invalid_boolean":
            return httpx.Response(200, json={"swapped": "false"})
        if failure == "rate_limited":
            return httpx.Response(429, json={"message": "Too many requests"})
        return httpx.Response(401, json={"message": "Authorization header is missing"})

    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
            evidence = await NokiaGateway("test-key", client).check("sim_swap", "+99999991000")
            assert evidence["status"] == "UNKNOWN"
            assert evidence["data"] == {}
    asyncio.run(run())


def test_number_verification_cancellation_stops_later_oauth_requests():
    credentials_started = asyncio.Event()
    release_credentials = asyncio.Event()
    cancelled = False
    paths = []

    async def respond(request):
        paths.append(request.url.path)
        credentials_started.set()
        await release_credentials.wait()
        return httpx.Response(200, json={"client_id": "client"})

    async def run():
        nonlocal cancelled
        async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
            check = asyncio.create_task(NokiaGateway("test-key", client).check(
                "number_verification", "+99999991000", should_stop=lambda: cancelled,
            ))
            await credentials_started.wait()
            cancelled = True
            release_credentials.set()
            result = await check

            assert result["status"] == "UNKNOWN"
            assert result["error"] == "ProviderCheckCancelled"
            assert paths == ["/oauth2/v1/auth/clientcredentials"]

    asyncio.run(run())
