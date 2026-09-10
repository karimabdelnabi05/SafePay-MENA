"""Agent/provider contract regressions exercised through the payment API."""
import asyncio
import json

import httpx
import pytest
from fastapi.testclient import TestClient

from app.api import create_app


def nokia_response(request):
    if request.url.path.endswith("clientcredentials"):
        return httpx.Response(200, json={"client_id": "client"})
    if "well-known" in request.url.path:
        return httpx.Response(200, json={"fast_flow_csp_auth_endpoint":
            "https://nb-auth.nac-runtime-stg-eu.g002.saas.nokia.com/oauth2/v1/retrieve_csp_auth_url"})
    if request.url.path.endswith("retrieve_csp_auth_url"):
        params = dict(request.url.params)
        return httpx.Response(302, headers={
            "location": params["redirect_uri"] + "?code=code&state=" + params["state"]})
    if request.url.path.endswith("/verify"):
        return httpx.Response(200, json={"devicePhoneNumberVerified": True})
    return httpx.Response(200, json={"swapped": True})


def function(name, **args):
    return {"functionCall": {"name": name, "args": args, "id": name + "-id"}}


def payment(external):
    with TestClient(create_app(allow_live=True, external_transport=httpx.MockTransport(external),
                               nokia_key="test", gemini_key="test")) as client:
        client.post("/api/v1/sessions", json={"scenario": "sim_swap", "mode": "NOKIA_SANDBOX"})
        response = client.post("/api/v1/payments", json={
            "request_id": "agent-regression", "amount": 35000, "recipient": "new_payee"})
        assert response.status_code == 200
        return response.json()


def test_number_verification_then_batched_sim_and_device_checks_completes():
    requests = []
    batch = [function("sim_swap", reason="Check recent SIM change"),
             function("device_swap", reason="Check the unusual device session")]
    batch[0]["thoughtSignature"] = "opaque-signature-preserve-unchanged"

    def external(request):
        if request.url.host != "generativelanguage.googleapis.com":
            return nokia_response(request)
        body = json.loads(request.content)
        requests.append(body)
        if len(requests) == 1:
            parts = [function("number_verification", reason="Verify the number")]
        elif len(requests) == 2:
            parts = batch
        else:
            assert body["contents"][-2] == {"role": "model", "parts": batch}
            responses = body["contents"][-1]["parts"]
            assert [p["functionResponse"]["id"] for p in responses] == ["sim_swap-id", "device_swap-id"]
            parts = [function("finish", decision="BLOCK", reason="SIM and device changes with unusual session")]
        return httpx.Response(200, json={"candidates": [{"content": {"role": "model", "parts": parts}}]})

    result = payment(external)
    assert result["decision"] == "BLOCK", result
    assert result["agent_error"] is None
    assert result["telecom_calls"] == 3
    assert result["model_calls"] == 3
    assert [e["tool"] for e in result["evidence"]] == ["number_verification", "sim_swap", "device_swap"]


@pytest.mark.parametrize("status,code", [(429, "GEMINI_RATE_LIMITED"), (401, "GEMINI_AUTH_FAILED"),
                                        (400, "GEMINI_REQUEST_REJECTED")])
def test_model_http_failure_after_number_verification_explains_missing_sim(status, code):
    model_calls = 0

    def external(request):
        nonlocal model_calls
        if request.url.host != "generativelanguage.googleapis.com":
            return nokia_response(request)
        model_calls += 1
        if model_calls == 1:
            return httpx.Response(200, json={"candidates": [{"content": {"role": "model", "parts": [
                function("number_verification", reason="Verify the number")]}}]})
        return httpx.Response(status, json={"error": {"message": "sensitive-provider-message-do-not-expose"}})

    result = payment(external)
    assert result["decision"] == "RETRY"
    assert result["agent_diagnostic"]["code"] == code
    assert result["agent_diagnostic"]["http_status"] == status
    assert result["agent_diagnostic"]["model_call"] == 2
    assert result["missing_evidence"] == ["sim_swap"]
    assert result["pre_call_score"] == 80
    assert result["final_risk_score"] is None
    assert result["risk_score_status"] == "INCOMPLETE"
    assert result["telecom_calls"] == 1
    assert result["model_calls"] == 2
    assert "sensitive-provider-message" not in json.dumps(result)
    assert "SIM Swap was not called" in " ".join(result["reasons"])


def test_unknown_evidence_does_not_get_a_final_score_or_validate_agent_approval():
    calls = 0

    def external(request):
        nonlocal calls
        if request.url.host != "generativelanguage.googleapis.com":
            return httpx.Response(503)
        calls += 1
        part = (function("number_verification", reason="Verify number") if calls == 1 else
                function("finish", decision="APPROVE", reason="Identity is clear"))
        return httpx.Response(200, json={"candidates": [{"content": {"role": "model", "parts": [part]}}]})

    result = payment(external)
    assert result["decision"] == "RETRY"
    assert result["agent_proposal"] == "APPROVE"
    assert result["policy_override"] is True
    assert result["risk_score_status"] == "INCOMPLETE"
    assert result["final_risk_score"] is None
    assert result["missing_evidence"] == ["sim_swap", "number_verification"]
    assert result["evidence"][0]["http_status"] == 503
    assert result["evidence"][0]["failure_step"] == "/oauth2/v1/auth/clientcredentials"


def test_nokia_429_starts_shared_cooldown_and_prevents_more_provider_calls():
    requests = []

    def external(request):
        requests.append(request)
        return httpx.Response(429, headers={"Retry-After": "120"}, json={"error": "private"})

    with TestClient(create_app(allow_live=True, nokia_key="test",
                               external_transport=httpx.MockTransport(external))) as client:
        client.post("/api/v1/sessions", json={"scenario": "first_setup", "mode": "NOKIA_SANDBOX"})
        result = client.post("/api/v1/enrollments", json={"request_id": "quota"}).json()
        assert result["decision"] == "RETRY"
        assert len(requests) == 1
        assert result["telecom_calls"] == 1
        assert result["evidence"][0]["http_status"] == 429
        assert result["evidence"][0]["retry_after_seconds"] == 120
        assert result["evidence"][1]["request_made"] is False
        availability = client.get("/api/v1/live-access").json()["nokia"]
        assert availability["status"] == "RATE_LIMITED"
        assert 0 < availability["retry_after_seconds"] <= 120
        assert availability["reset_confirmed"] is False
        client.post("/api/v1/enrollments", json={"request_id": "quota-again"})
        assert len(requests) == 1


def test_transient_model_retry_is_counted_and_traced_with_mock_transport():
    requests = []

    def external(request):
        requests.append(request)
        if len(requests) == 1:
            return httpx.Response(503)
        return httpx.Response(200, json={"candidates": [{"content": {"role": "model", "parts": [
            function("finish", decision="RETRY", reason="Evidence is unavailable")]}}]})

    result = payment(external)
    assert len(requests) == 2
    assert result["model_calls"] == 2
    assert result["model_turns"] == 1
    assert result["agent_error"] is None
    assert any(t.get("status") == "RETRY" for t in result["agent_trace"])


def test_cancellation_during_model_backoff_prevents_the_retry_request():
    started = asyncio.Event()
    requests = []

    async def external(request):
        requests.append(request)
        started.set()
        return httpx.Response(503)

    async def run():
        app = create_app(allow_live=True, nokia_key="test", gemini_key="test",
                         external_transport=httpx.MockTransport(external))
        async with app.router.lifespan_context(app), httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            await client.post("/api/v1/sessions", json={"scenario": "sim_swap", "mode": "NOKIA_SANDBOX"})
            task = asyncio.create_task(client.post("/api/v1/payments", json={"request_id": "cancel-retry", "amount": 35000}))
            await started.wait()
            await client.post("/api/v1/runs/cancel-retry/cancel")
            assert (await task).json()["decision"] == "CANCELLED"
            assert len(requests) == 1
    asyncio.run(run())
