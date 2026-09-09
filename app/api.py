"""Session-scoped SafePay demonstration API. No real payment execution."""

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
from app.services.nokia import NokiaGateway


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


def create_app(database=":memory:", allow_live=False, external_transport=None, nokia_key="", gemini_key=""):
    db = sqlite3.connect(database, check_same_thread=False)
    db.execute("CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, data TEXT NOT NULL)")
    db.execute("CREATE TABLE IF NOT EXISTS runs (session TEXT, id TEXT, payload TEXT, result TEXT, PRIMARY KEY(session,id))")

    @asynccontextmanager
    async def lifespan(app):
        app.state.db = db
        try:
            yield
        finally:
            db.close()

    app = FastAPI(title="SafePay MENA", version="2.0", lifespan=lifespan)

    @app.get("/api/v1/catalog")
    async def catalog():
        return {"countries": COUNTRIES, "live_enabled": allow_live,
                "scenarios": [{"id": key, "name": value[0], "description": value[1]} for key, value in SCENARIOS.items()],
                "model": "gemini-3.5-flash-lite", "production_networks": False}

    @app.get("/api/v1/health")
    async def health():
        return {"status": "healthy", "mode": "SANDBOX_ENABLED" if allow_live else "FIXTURE_ONLY",
                "nokia_configured": bool(nokia_key), "gemini_configured": bool(gemini_key),
                "production_networks": False}

    @app.post("/api/v1/evaluations")
    async def evaluate_workflows():
        from app.evaluation import evaluate
        return await evaluate()

    def begin(request, body, kind):
        sid = request.cookies["safepay_session"]
        payload = json.dumps({"kind": kind, **body.model_dump()}, sort_keys=True)
        row = db.execute("SELECT payload,result FROM runs WHERE session=? AND id=?", (sid, body.request_id)).fetchone()
        if row:
            if row[0] != payload:
                raise HTTPException(409, "Request ID already belongs to a different intent")
            return json.loads(row[1])
        pending = {"id": body.request_id, "decision": "PENDING", "kind": kind}
        db.execute("INSERT INTO runs VALUES (?,?,?,?)", (sid, body.request_id, payload, json.dumps(pending)))
        db.commit()
        return None

    def finish(request, result):
        row = db.execute("SELECT result FROM runs WHERE session=? AND id=?", (request.cookies["safepay_session"], result["id"])).fetchone()
        if row and json.loads(row[0])["decision"] == "CANCELLED":
            return json.loads(row[0])
        db.execute("UPDATE runs SET result=? WHERE session=? AND id=?",
                   (json.dumps(result), request.cookies["safepay_session"], result["id"]))
        db.commit()
        return result

    def run_cancelled(request, run_id):
        row = db.execute(
            "SELECT result FROM runs WHERE session=? AND id=?",
            (request.cookies["safepay_session"], run_id),
        ).fetchone()
        return bool(row and json.loads(row[0]).get("decision") == "CANCELLED")

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
        return finish(request, result)

    def session(request):
        row = db.execute("SELECT data FROM sessions WHERE id=?", (request.cookies.get("safepay_session", ""),)).fetchone()
        if not row:
            raise HTTPException(401, "Start a demo session first")
        data = json.loads(row[0])
        if data.get("created_at", 0) < time.time() - 3600:
            raise HTTPException(401, "Demo session expired")
        return data

    @app.post("/api/v1/sessions")
    async def start_session(body: SessionInput, response: Response):
        if body.scenario not in SCENARIOS:
            raise HTTPException(422, "Unknown scenario")
        if body.mode == "NOKIA_SANDBOX" and not allow_live:
            raise HTTPException(403, "Live sandbox mode is disabled on this deployment")
        if body.mode == "NOKIA_SANDBOX" and body.scenario in {"provider_outage", "enrollment_outage"}:
            raise HTTPException(422, "Outage scenarios use offline fixtures; live failures are never simulated silently")
        sid = secrets.token_urlsafe(32)
        data = body.model_dump()
        data["created_at"] = time.time()
        data["trusted_device"] = body.scenario not in {"first_setup", "new_device", "enrollment_outage"}
        db.execute("INSERT INTO sessions VALUES (?,?)", (sid, json.dumps(data)))
        db.commit()
        response.set_cookie("safepay_session", sid, httponly=True, samesite="strict", max_age=3600)
        return data

    @app.post("/api/v1/payments")
    async def payment(body: PaymentInput, request: Request):
        data = session(request)
        existing = begin(request, body, "payment")
        if existing:
            return existing
        context = context_for(data["scenario"])
        recent = [value for value in data.get("attempt_times", []) if value > time.time() - 3600]
        recent.append(time.time())
        data["attempt_times"] = recent
        db.execute("UPDATE sessions SET data=? WHERE id=?", (json.dumps(data), request.cookies["safepay_session"]))
        db.commit()
        context["recent_attempts"] = len(recent)
        pre_score, reasons = screen(context, body.amount, body.recipient)
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
                async with httpx.AsyncClient(transport=external_transport) as external:
                    result.update(await investigate(investigation_context, NokiaGateway(nokia_key, external), subjects,
                                                    external, gemini_key,
                                                    should_stop=lambda: run_cancelled(request, body.request_id)))
                return finish(request, result)
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
        return finish(request, result)

    @app.post("/api/v1/enrollments")
    async def enroll(body: EnrollmentInput, request: Request):
        data = session(request)
        existing = begin(request, body, "enrollment")
        if existing:
            return existing
        if data["mode"] == "NOKIA_SANDBOX":
            async with httpx.AsyncClient(transport=external_transport) as external:
                gateway = NokiaGateway(nokia_key, external)
                evidence = []
                for tool, phone in (("number_verification", "+99999991000"),
                                    ("sim_swap", "+99999991001")):
                    if run_cancelled(request, body.request_id):
                        return await get_run(body.request_id, request)
                    evidence.append(await gateway.check(
                        tool,
                        phone,
                        should_stop=lambda: run_cancelled(request, body.request_id),
                    ))
        else:
            gateway = FixtureGateway(signals_for(data["scenario"]))
            evidence = [await gateway.check(tool) for tool in ("number_verification", "sim_swap")]
        current = await get_run(body.request_id, request)
        if current["decision"] == "CANCELLED":
            return current
        trusted_device = all(e["status"] == "SUCCESS" for e in evidence) and evidence[0]["data"].get("devicePhoneNumberVerified") is True and evidence[1]["data"].get("swapped") is False
        data = session(request)
        data["trusted_device"] = trusted_device
        db.execute("UPDATE sessions SET data=? WHERE id=?", (json.dumps(data), request.cookies["safepay_session"]))
        db.commit()
        return finish(request, {"id": body.request_id, "decision": "TRUST_ESTABLISHED" if data["trusted_device"] else "RETRY",
            "evidence": evidence, "pre_call_score": None, "final_risk_score": None,
            "telecom_calls": 2 if data["mode"] == "NOKIA_SANDBOX" else 0, "model_calls": 0,
            "decision_source": "MANDATORY_ENROLLMENT_POLICY", "reasons": ["Fresh Number Verification and SIM Swap are required for device trust"],
            "agent_trace": [{"actor": "POLICY", "tool": e["tool"], "reason": "Mandatory fresh enrollment check", "status": e["status"]} for e in evidence]})

    return app
