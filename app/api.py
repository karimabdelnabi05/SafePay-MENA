"""Session-scoped SafePay demonstration API. No real payment execution."""

import asyncio
import json
import secrets
import sqlite3
import time
from contextlib import asynccontextmanager
from typing import Literal

import httpx
from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.demo import COUNTRIES, SCENARIOS, context_for, signals_for
from app.core.policy import assess, screen
from app.services.fixtures import FixtureGateway
from app.services.investigator import investigate
from app.services.nokia import NokiaAvailability, NokiaGateway


class SessionInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    scenario: str = "routine"
    country: Literal["EG", "SA", "AE"] = "EG"
    mode: Literal["FIXTURE", "NOKIA_SANDBOX"] = "FIXTURE"


class PaymentInput(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    request_id: str = Field(min_length=1, max_length=80)
    amount: float = Field(gt=0, le=1000000)
    recipient: Literal["family", "new_payee", "merchant", "wallet"] = "family"
    channel: Literal["INSTANT_PAYMENT", "CARD_CHECKOUT", "WALLET_TRANSFER"] = "INSTANT_PAYMENT"

    @field_validator("request_id")
    @classmethod
    def validate_request_id(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Request ID cannot be blank")
        return value

    @field_validator("amount", mode="before")
    @classmethod
    def require_numeric_amount(cls, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            # Pydantic v2 propagates TypeError instead of producing an HTTP 422.
            raise ValueError("Amount must be a JSON number")  # noqa: TRY004
        return value


class EnrollmentInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    request_id: str = Field(min_length=1, max_length=80)

    @field_validator("request_id")
    @classmethod
    def validate_request_id(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Request ID cannot be blank")
        return value


class LiveAccessInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: str = Field(min_length=1, max_length=128)


def create_app(
    database=":memory:",
    allow_live=False,
    external_transport=None,
    nokia_key="",
    gemini_key="",
    judge_access_code="",
    live_run_limit=4,
    live_global_limit=12,
):
    db = sqlite3.connect(database, check_same_thread=False)
    db.execute("CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, data TEXT NOT NULL)")
    db.execute("CREATE TABLE IF NOT EXISTS runs (session TEXT, id TEXT, payload TEXT, result TEXT, PRIMARY KEY(session,id))")
    access_grants = {}
    failed_access = {}
    global_failures = []
    global_runs = []
    nokia_availability = NokiaAvailability()
    background_tasks = set()
    access_required = bool(judge_access_code)
    access_ttl = 2 * 3600
    quota_window = 3600

    @asynccontextmanager
    async def lifespan(app):
        app.state.db = db
        app.state.background_tasks = background_tasks
        try:
            yield
        finally:
            for task in background_tasks:
                task.cancel()
            if background_tasks:
                await asyncio.gather(*background_tasks, return_exceptions=True)
            db.close()

    app = FastAPI(title="SafePay MENA", version="2.0", lifespan=lifespan)

    @app.get("/api/v1/catalog")
    async def catalog():
        return {"countries": COUNTRIES, "live_enabled": allow_live,
                "live_access_required": allow_live and access_required,
                "scenarios": [{"id": key, "name": value[0], "description": value[1]} for key, value in SCENARIOS.items()],
                "model": "gemini-3.5-flash-lite", "production_networks": False}

    @app.get("/api/v1/health")
    async def health():
        return {"status": "healthy", "mode": "SANDBOX_ENABLED" if allow_live else "FIXTURE_ONLY",
                "nokia_configured": bool(nokia_key), "gemini_configured": bool(gemini_key),
                "production_networks": False}

    def prune(values, cutoff):
        values[:] = [value for value in values if value > cutoff]

    def access_grant(request):
        if not allow_live:
            return None
        if not access_required:
            return {"expires_at": time.time() + access_ttl, "runs": []}
        token = request.cookies.get("safepay_live_access", "")
        grant = access_grants.get(token)
        if not grant or grant["expires_at"] <= time.time():
            access_grants.pop(token, None)
            return None
        return grant

    def uses_https(request):
        forwarded = request.headers.get("x-forwarded-proto", "").split(",", 1)[0].strip()
        return request.url.scheme == "https" or forwarded == "https"

    def access_payload(request):
        now = time.time()
        prune(global_runs, now - quota_window)
        grant = access_grant(request)
        if grant:
            prune(grant["runs"], now - quota_window)
        return {
            "available": allow_live,
            "authorized": bool(grant),
            "remaining": max(0, live_run_limit - len(grant["runs"])) if grant else 0,
            "global_remaining": max(0, live_global_limit - len(global_runs)),
            "expires_at": grant["expires_at"] if grant and access_required else None,
            "nokia": nokia_availability.snapshot(),
        }

    def require_live_access(request):
        grant = access_grant(request)
        if not grant:
            raise HTTPException(403, "Unlock connected sandbox mode with the judge access code")
        return grant

    def consume_live_quota(request):
        grant = require_live_access(request)
        now = time.time()
        prune(grant["runs"], now - quota_window)
        prune(global_runs, now - quota_window)
        if len(grant["runs"]) >= live_run_limit:
            raise HTTPException(429, "This judge session has reached its hourly connected-run limit")
        if len(global_runs) >= live_global_limit:
            raise HTTPException(429, "SafePay's shared connected-run allowance is exhausted; this is separate from provider quota")
        grant["runs"].append(now)
        global_runs.append(now)

    @app.get("/api/v1/live-access")
    async def get_live_access(request: Request):
        return access_payload(request)

    @app.post("/api/v1/live-access")
    async def unlock_live_access(body: LiveAccessInput, request: Request, response: Response):
        if not allow_live or not access_required:
            raise HTTPException(404, "Protected connected mode is not configured")
        now = time.time()
        forwarded = request.headers.get("x-forwarded-for", "").split(",", 1)[0].strip()
        client_id = forwarded or (request.client.host if request.client else "unknown")
        attempts = failed_access.setdefault(client_id, [])
        prune(attempts, now - 600)
        prune(global_failures, now - 600)
        if len(attempts) >= 5 or len(global_failures) >= 30:
            raise HTTPException(429, "Too many access attempts; wait before trying again")
        if not secrets.compare_digest(body.code.encode(), judge_access_code.encode()):
            attempts.append(now)
            global_failures.append(now)
            raise HTTPException(401, "Invalid judge access code")
        failed_access.pop(client_id, None)
        if access_grant(request):
            return access_payload(request)
        for expired in [key for key, grant in access_grants.items() if grant["expires_at"] <= now]:
            del access_grants[expired]
        token = secrets.token_urlsafe(32)
        access_grants[token] = {"expires_at": now + access_ttl, "runs": []}
        response.set_cookie(
            "safepay_live_access",
            token,
            httponly=True,
            secure=uses_https(request),
            samesite="strict",
            max_age=access_ttl,
        )
        return access_payload(request) | {
            "authorized": True,
            "remaining": live_run_limit,
            "expires_at": now + access_ttl,
        }

    @app.delete("/api/v1/live-access")
    async def lock_live_access(request: Request, response: Response):
        access_grants.pop(request.cookies.get("safepay_live_access", ""), None)
        response.delete_cookie("safepay_live_access")
        return {"authorized": False}

    @app.post("/api/v1/evaluations")
    async def evaluate_workflows():
        from app.evaluation import evaluate
        return await evaluate()

    def begin(request, body, kind, connected=False):
        sid = request.cookies["safepay_session"]
        payload = json.dumps({"kind": kind, **body.model_dump()}, sort_keys=True)
        row = db.execute("SELECT payload,result FROM runs WHERE session=? AND id=?", (sid, body.request_id)).fetchone()
        if row:
            if row[0] != payload:
                raise HTTPException(409, "Request ID already belongs to a different intent")
            return json.loads(row[1])
        pending = {"id": body.request_id, "decision": "PENDING", "kind": kind}
        if connected:
            pending.update({
                "connected": True,
                "stage": "QUEUED",
                "progress": [{
                    "stage": "QUEUED",
                    "actor": "SAFEPAY",
                    "message": "Connected sandbox review queued",
                    "observed_at": time.time(),
                }],
            })
        db.execute("INSERT INTO runs VALUES (?,?,?,?)", (sid, body.request_id, payload, json.dumps(pending)))
        db.commit()
        return None

    def finish_for_session(sid, result):
        row = db.execute("SELECT result FROM runs WHERE session=? AND id=?", (sid, result["id"])).fetchone()
        if row and json.loads(row[0])["decision"] == "CANCELLED":
            return json.loads(row[0])
        if row and "progress" not in result:
            result["progress"] = json.loads(row[0]).get("progress", [])
        if row and json.loads(row[0]).get("connected"):
            result["connected"] = True
            result["stage"] = ("CANCELLED" if result["decision"] == "CANCELLED" else
                               "INCOMPLETE" if result["decision"] == "RETRY" or result.get("agent_error") else
                               "COMPLETE" if result["decision"] != "PENDING" else result.get("stage", "QUEUED"))
        db.execute("UPDATE runs SET result=? WHERE session=? AND id=?",
                   (json.dumps(result), sid, result["id"]))
        db.commit()
        return result

    def finish(request, result):
        return finish_for_session(request.cookies["safepay_session"], result)

    def run_cancelled_for_session(sid, run_id):
        row = db.execute(
            "SELECT result FROM runs WHERE session=? AND id=?",
            (sid, run_id),
        ).fetchone()
        return bool(row and json.loads(row[0]).get("decision") == "CANCELLED")

    def run_cancelled(request, run_id):
        return run_cancelled_for_session(request.cookies["safepay_session"], run_id)

    def add_progress(sid, run_id, stage, actor, message, **details):
        if stage == "COMPLETE" and details.get("decision") == "RETRY":
            stage, message = "INCOMPLETE", "Verification stopped without sufficient evidence; no automatic release"
        row = db.execute("SELECT result FROM runs WHERE session=? AND id=?", (sid, run_id)).fetchone()
        if not row:
            return
        result = json.loads(row[0])
        if result.get("decision") != "PENDING":
            return
        event = {
            "stage": stage,
            "actor": actor,
            "message": str(message)[:300],
            "observed_at": time.time(),
        }
        event.update({key: value for key, value in details.items() if value is not None})
        result["stage"] = stage
        if stage == "LOCAL_SCREEN":
            result.update(pre_call_score=details.get("pre_call_score"), reasons=details.get("reasons", []))
        if stage == "AGENT_DECISION":
            result["model_calls"] = details.get("model_call", 0)
        if stage == "EVIDENCE_RECEIVED" and details.get("observation"):
            result.setdefault("evidence", []).append(details["observation"])
            result["telecom_calls"] = sum(e.get("request_made", True) for e in result["evidence"])
        result.setdefault("progress", []).append(event)
        result["progress"] = result["progress"][-64:]
        db.execute("UPDATE runs SET result=? WHERE session=? AND id=?", (json.dumps(result), sid, run_id))
        db.commit()

    @app.get("/api/v1/runs/{run_id}")
    async def get_run(run_id: str, request: Request):
        session(request)
        row = db.execute("SELECT result FROM runs WHERE session=? AND id=?", (request.cookies["safepay_session"], run_id)).fetchone()
        if not row:
            raise HTTPException(404, "Run not found")
        return json.loads(row[0])

    @app.post("/api/v1/runs/{run_id}/cancel")
    async def cancel(run_id: str, request: Request):
        result = await get_run(run_id, request)
        if result["decision"] not in {"PENDING", "HOLD", "RETRY", "VERIFY_DEVICE", "CANCELLED"}:
            raise HTTPException(409, "This run is already final")
        result["decision"] = "CANCELLED"
        result["stage"] = "CANCELLED"
        return finish(request, result)

    def session_for_id(sid):
        row = db.execute("SELECT data FROM sessions WHERE id=?", (sid,)).fetchone()
        if not row:
            raise HTTPException(401, "Start a demo session first")
        data = json.loads(row[0])
        if data.get("created_at", 0) < time.time() - 3600:
            raise HTTPException(401, "Demo session expired")
        return data

    def session(request):
        return session_for_id(request.cookies.get("safepay_session", ""))

    @app.post("/api/v1/sessions")
    async def start_session(body: SessionInput, request: Request, response: Response):
        if body.scenario not in SCENARIOS:
            raise HTTPException(422, "Unknown scenario")
        if body.mode == "NOKIA_SANDBOX" and not allow_live:
            raise HTTPException(403, "Live sandbox mode is disabled on this deployment")
        if body.mode == "NOKIA_SANDBOX":
            require_live_access(request)
        if body.mode == "NOKIA_SANDBOX" and body.scenario in {"provider_outage", "enrollment_outage"}:
            raise HTTPException(422, "Outage scenarios use offline fixtures; live failures are never simulated silently")
        sid = secrets.token_urlsafe(32)
        data = body.model_dump()
        data["created_at"] = time.time()
        data["trusted_device"] = body.scenario not in {"first_setup", "new_device", "enrollment_outage"}
        db.execute("INSERT INTO sessions VALUES (?,?)", (sid, json.dumps(data)))
        db.commit()
        response.set_cookie(
            "safepay_session", sid, httponly=True, secure=uses_https(request),
            samesite="strict", max_age=3600,
        )
        return data

    async def run_payment(body, sid, data, connected=False):
        data = session_for_id(sid)
        context = context_for(data["scenario"])
        recent = [value for value in data.get("attempt_times", []) if value > time.time() - 3600]
        recent.append(time.time())
        data["attempt_times"] = recent
        db.execute("UPDATE sessions SET data=? WHERE id=?", (json.dumps(data), sid))
        db.commit()
        context["recent_attempts"] = len(recent)
        pre_score, reasons = screen(context, body.amount, body.recipient)
        if connected:
            add_progress(sid, body.request_id, "LOCAL_SCREEN", "POLICY",
                         f"Local screening score: {pre_score}; investigation threshold: 20",
                         pre_call_score=pre_score, reasons=reasons)
        investigation_context = {**context,
            "transaction": {"amount": body.amount, "recipient_relationship": body.recipient,
                            "country": data["country"], "channel": body.channel},
            "pre_call_score": pre_score, "pre_call_reasons": reasons}
        result = {"id": body.request_id, "decision": "APPROVE" if data["trusted_device"] else "VERIFY_DEVICE",
                  "pre_call_score": pre_score, "final_risk_score": pre_score, "telecom_calls": 0,
                  "model_calls": 0, "evidence": [], "reasons": reasons, "decision_source": "LOCAL_SCREENING"}
        if data["trusted_device"] and pre_score >= 20:
            values = signals_for(data["scenario"])
            if data["mode"] == "NOKIA_SANDBOX":
                subjects = {tool: "+99999991000" if value else "+99999991001" for tool, value in values.items()}

                async def report(event):
                    add_progress(sid, body.request_id, **event)

                async with httpx.AsyncClient(transport=external_transport) as external:
                    result.update(await investigate(investigation_context, NokiaGateway(nokia_key, external, nokia_availability), subjects,
                                                    external, gemini_key,
                                                    should_stop=lambda: run_cancelled_for_session(sid, body.request_id),
                                                    on_progress=report if connected else None))
                if connected:
                    add_progress(sid, body.request_id, "COMPLETE", "SAFEPAY",
                                 "Connected investigation completed with policy controls",
                                 decision=result["decision"])
                return finish_for_session(sid, result)
            gateway = FixtureGateway(values)
            tools = ["sim_swap", "number_verification"]
            if context["session_anomaly"]:
                tools.append("device_swap")
            if context["travel_expected"]:
                tools.append("roaming")
            result["evidence"] = [await gateway.check(tool) for tool in tools]
            result["decision"], result["final_risk_score"], result["reasons"] = assess(
                investigation_context, result["evidence"]
            )
            result["decision_source"] = "DETERMINISTIC_FIXTURE"
        if connected:
            add_progress(sid, body.request_id, "POLICY_DECISION", "POLICY",
                         "Local policy completed the review without a network request",
                         decision=result["decision"])
            add_progress(sid, body.request_id, "COMPLETE", "SAFEPAY",
                         "Review completed", decision=result["decision"])
        return finish_for_session(sid, result)

    async def run_enrollment(body, sid, data, connected=False):
        if data["mode"] == "NOKIA_SANDBOX":
            async with httpx.AsyncClient(transport=external_transport) as external:
                gateway = NokiaGateway(nokia_key, external, nokia_availability)
                evidence = []
                for tool, phone in (("number_verification", "+99999991000"),
                                    ("sim_swap", "+99999991001")):
                    if run_cancelled_for_session(sid, body.request_id):
                        row = db.execute("SELECT result FROM runs WHERE session=? AND id=?",
                                         (sid, body.request_id)).fetchone()
                        return json.loads(row[0])
                    if connected:
                        add_progress(sid, body.request_id, "API_SELECTED", "POLICY",
                                     f"Mandatory enrollment policy selected {tool.replace('_', ' ').title()}",
                                     tool=tool)
                    observation = await gateway.check(
                        tool,
                        phone,
                        should_stop=lambda: run_cancelled_for_session(sid, body.request_id),
                    )
                    evidence.append(observation)
                    if connected:
                        add_progress(sid, body.request_id, "EVIDENCE_RECEIVED", "NOKIA",
                                     f"Nokia sandbox returned {observation['status']}",
                                     tool=tool, status=observation["status"],
                                     source=observation["source"], latency_ms=observation["latency_ms"],
                                     http_status=observation.get("http_status"), observation=observation)
        else:
            gateway = FixtureGateway(signals_for(data["scenario"]))
            evidence = [await gateway.check(tool) for tool in ("number_verification", "sim_swap")]
        row = db.execute("SELECT result FROM runs WHERE session=? AND id=?", (sid, body.request_id)).fetchone()
        if row and json.loads(row[0])["decision"] == "CANCELLED":
            return json.loads(row[0])
        trusted_device = all(e["status"] == "SUCCESS" for e in evidence) and evidence[0]["data"].get("devicePhoneNumberVerified") is True and evidence[1]["data"].get("swapped") is False
        data = session_for_id(sid)
        data["trusted_device"] = trusted_device
        db.execute("UPDATE sessions SET data=? WHERE id=?", (json.dumps(data), sid))
        db.commit()
        decision = "TRUST_ESTABLISHED" if data["trusted_device"] else "RETRY"
        if connected:
            add_progress(sid, body.request_id, "POLICY_DECISION", "POLICY",
                         "Mandatory device-trust policy evaluated the Nokia evidence", decision=decision)
            add_progress(sid, body.request_id, "COMPLETE", "SAFEPAY",
                         "Connected enrollment review completed", decision=decision)
        return finish_for_session(sid, {"id": body.request_id, "decision": decision,
            "evidence": evidence, "pre_call_score": None, "final_risk_score": None,
            "telecom_calls": sum(e.get("request_made", True) for e in evidence) if data["mode"] == "NOKIA_SANDBOX" else 0, "model_calls": 0,
            "decision_source": "MANDATORY_ENROLLMENT_POLICY", "reasons": ["Fresh Number Verification and SIM Swap are required for device trust"],
            "agent_trace": [{"actor": "POLICY", "tool": e["tool"], "reason": "Mandatory fresh enrollment check", "status": e["status"]} for e in evidence]})

    @app.post("/api/v1/payments")
    async def payment(body: PaymentInput, request: Request):
        data = session(request)
        if access_required and data["mode"] == "NOKIA_SANDBOX":
            raise HTTPException(409, "Protected connected sessions must use the live-payments endpoint")
        existing = begin(request, body, "payment")
        if existing:
            return existing
        return await run_payment(body, request.cookies["safepay_session"], data)

    @app.post("/api/v1/enrollments")
    async def enroll(body: EnrollmentInput, request: Request):
        data = session(request)
        if access_required and data["mode"] == "NOKIA_SANDBOX":
            raise HTTPException(409, "Protected connected sessions must use the live-enrollments endpoint")
        existing = begin(request, body, "enrollment")
        if existing:
            return existing
        return await run_enrollment(body, request.cookies["safepay_session"], data)

    async def run_in_background(kind, body, sid, data):
        try:
            if kind == "payment":
                await run_payment(body, sid, data, connected=True)
            else:
                await run_enrollment(body, sid, data, connected=True)
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001 - detached work must always settle fail-closed.
            row = db.execute("SELECT result FROM runs WHERE session=? AND id=?", (sid, body.request_id)).fetchone()
            partial = json.loads(row[0]) if row else {}
            add_progress(sid, body.request_id, "POLICY_DECISION", "POLICY",
                         "The connected investigation stopped safely after an internal error",
                         status=type(exc).__name__)
            add_progress(sid, body.request_id, "COMPLETE", "SAFEPAY",
                         "Verification incomplete", decision="RETRY")
            finish_for_session(sid, {
                "id": body.request_id,
                "decision": "RETRY",
                "pre_call_score": partial.get("pre_call_score"),
                "final_risk_score": None,
                "telecom_calls": partial.get("telecom_calls", 0),
                "model_calls": partial.get("model_calls", 0),
                "evidence": partial.get("evidence", []),
                "reasons": ["Connected investigation did not complete"],
                "decision_source": "POLICY_FAIL_CLOSED",
                "agent_error": type(exc).__name__,
            })

    def schedule_connected(kind, body, request):
        data = session(request)
        if data["mode"] != "NOKIA_SANDBOX":
            raise HTTPException(409, "Connected runs require a Nokia sandbox session")
        require_live_access(request)
        existing = begin(request, body, kind, connected=True)
        if existing:
            return existing
        sid = request.cookies["safepay_session"]
        try:
            consume_live_quota(request)
        except HTTPException:
            db.execute("DELETE FROM runs WHERE session=? AND id=?", (sid, body.request_id))
            db.commit()
            raise
        task = asyncio.create_task(run_in_background(kind, body, sid, data))
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)
        row = db.execute("SELECT result FROM runs WHERE session=? AND id=?", (sid, body.request_id)).fetchone()
        return json.loads(row[0])

    @app.post("/api/v1/live-payments", status_code=202)
    async def live_payment(body: PaymentInput, request: Request):
        return schedule_connected("payment", body, request)

    @app.post("/api/v1/live-enrollments", status_code=202)
    async def live_enrollment(body: EnrollmentInput, request: Request):
        return schedule_connected("enrollment", body, request)

    return app
