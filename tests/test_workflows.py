import asyncio
import json
import sqlite3

import httpx
import pytest
from fastapi.testclient import TestClient

from app.api import create_app


def test_application_closes_database_on_shutdown():
    app = create_app(database=":memory:")
    with TestClient(app):
        assert app.state.db.execute("SELECT 1").fetchone() == (1,)

    with pytest.raises(sqlite3.ProgrammingError, match="closed database"):
        app.state.db.execute("SELECT 1")


def test_routine_payment_has_separate_scores_and_zero_external_calls():
    with TestClient(create_app(database=":memory:")) as client:
        session = client.post("/api/v1/sessions", json={"scenario": "routine", "country": "EG"})
        assert session.status_code == 200
        response = client.post("/api/v1/payments", json={"request_id": "routine-1", "amount": 200, "recipient": "family"})
        assert response.status_code == 200
        result = response.json()
        assert result["decision"] == "APPROVE"
        assert result["pre_call_score"] == 0
        assert result["final_risk_score"] == 0
        assert result["telecom_calls"] == 0
        assert result["model_calls"] == 0
        assert result["evidence"] == []


def test_clean_identity_evidence_does_not_erase_high_value_new_payee_risk():
    with TestClient(create_app(database=":memory:")) as client:
        client.post("/api/v1/sessions", json={"scenario": "routine", "country": "EG"})
        result = client.post("/api/v1/payments", json={
            "request_id": "high-new-payee",
            "amount": 2000,
            "recipient": "new_payee",
        }).json()

        assert result["pre_call_score"] == 45
        assert result["decision"] == "HOLD"
        assert result["final_risk_score"] >= 45
        assert {item["tool"] for item in result["evidence"]} == {
            "sim_swap", "number_verification",
        }
        assert "Amount exceeds the customer's usual range" in result["reasons"]
        assert "Recipient has no established relationship" in result["reasons"]


@pytest.mark.parametrize("scenario", ["first_setup", "new_device"])
def test_enrollment_is_required_before_even_a_small_payment(scenario):
    with TestClient(create_app(database=":memory:")) as client:
        assert client.post("/api/v1/sessions", json={"scenario": scenario}).status_code == 200
        result = client.post("/api/v1/payments", json={"request_id": "small", "amount": 1}).json()
        assert result["decision"] == "VERIFY_DEVICE"
        enrollment = client.post("/api/v1/enrollments", json={"request_id": "setup-1"}).json()
        assert enrollment["decision"] == "TRUST_ESTABLISHED"
        assert {e["tool"] for e in enrollment["evidence"]} == {"number_verification", "sim_swap"}
        assert all(e["source"] == "FIXTURE" for e in enrollment["evidence"])
        after = client.post("/api/v1/payments", json={"request_id": "after", "amount": 200}).json()
        assert after["decision"] == "APPROVE"
        assert after["telecom_calls"] == 0


def test_unavailable_enrollment_evidence_does_not_create_trust():
    with TestClient(create_app(database=":memory:")) as client:
        client.post("/api/v1/sessions", json={"scenario": "enrollment_outage"})
        result = client.post("/api/v1/enrollments", json={"request_id": "setup-1"}).json()
        assert result["decision"] == "RETRY"
        assert any(e["status"] == "UNKNOWN" for e in result["evidence"])
        payment = client.post("/api/v1/payments", json={"request_id": "after", "amount": 1}).json()
        assert payment["decision"] == "VERIFY_DEVICE"


@pytest.mark.parametrize("country", ["EG", "SA", "AE"])
@pytest.mark.parametrize("scenario,decision", [
    ("sim_swap", "BLOCK"), ("card_misuse", "BLOCK"),
    ("combined_attack", "BLOCK"), ("scam_transfer", "HOLD"),
    ("legitimate_travel", "APPROVE"), ("provider_outage", "RETRY"),
    ("velocity", "HOLD"),
])
def test_payment_investigates_observations_across_three_markets(country, scenario, decision):
    with TestClient(create_app(database=":memory:")) as client:
        assert client.post("/api/v1/sessions", json={"scenario": scenario, "country": country}).status_code == 200
        result = client.post("/api/v1/payments", json={"request_id": "case-1", "amount": 200, "recipient": "new_payee"}).json()
        assert result["decision"] == decision
        assert result["pre_call_score"] >= 20
        assert result["evidence"]


def test_number_mismatch_never_approves_even_without_other_anomalies():
    with TestClient(create_app(database=":memory:")) as client:
        client.post("/api/v1/sessions", json={"scenario": "identity_mismatch"})
        result = client.post("/api/v1/payments", json={"request_id": "mismatch", "amount": 200, "recipient": "new_payee"}).json()
        assert result["decision"] == "HOLD"
        assert result["final_risk_score"] == 55
        assert result["decision_source"] == "DETERMINISTIC_FIXTURE"
        assert all(e["source"] == "FIXTURE" for e in result["evidence"])


def test_payment_retry_is_idempotent_and_conflicting_intent_is_rejected():
    with TestClient(create_app(database=":memory:")) as client:
        client.post("/api/v1/sessions", json={"scenario": "routine"})
        payload = {"request_id": "once", "amount": 200}
        first = client.post("/api/v1/payments", json=payload).json()
        assert client.post("/api/v1/payments", json=payload).json() == first
        assert client.get("/api/v1/runs/once").json() == first
        assert client.post("/api/v1/payments", json={**payload, "amount": 300}).status_code == 409


@pytest.mark.parametrize("payload", [
    {"request_id": " ", "amount": 200},
    {"request_id": "boolean-amount", "amount": True},
    {"request_id": "string-amount", "amount": "200"},
    {"request_id": "bad-channel", "amount": 200, "channel": "CRYPTO"},
    {"request_id": "extra-field", "amount": 200, "unexpected": "value"},
])
def test_payment_rejects_ambiguous_or_unsupported_input(payload):
    with TestClient(create_app(database=":memory:")) as client:
        client.post("/api/v1/sessions", json={"scenario": "routine"})
        assert client.post("/api/v1/payments", json=payload).status_code == 422


def test_expired_session_cannot_start_a_payment(monkeypatch):
    clock = {"now": 1000.0}
    monkeypatch.setattr("app.api.time.time", lambda: clock["now"])
    with TestClient(create_app(database=":memory:")) as client:
        client.post("/api/v1/sessions", json={"scenario": "routine"})
        sid = client.cookies.get("safepay_session")
        clock["now"] += 3601
        client.cookies.clear()
        response = client.post("/api/v1/payments", json={"request_id": "late", "amount": 200},
                               headers={"cookie": f"safepay_session={sid}"})
        assert response.status_code == 401


def test_held_payment_can_be_cancelled_but_not_released_by_client_biometric_claim():
    app = create_app(database=":memory:")
    with TestClient(app) as client:
        client.post("/api/v1/sessions", json={"scenario": "scam_transfer"})
        client.post("/api/v1/payments", json={"request_id": "hold", "amount": 200})
        assert client.post("/api/v1/transfer/step-up/verify", json={"transaction_id": "hold", "success": True}).status_code in (404, 410)
        cancelled = client.post("/api/v1/runs/hold/cancel").json()
        assert cancelled["decision"] == "CANCELLED"
        assert client.get("/api/v1/runs/hold").json()["decision"] == "CANCELLED"
        client.post("/api/v1/sessions", json={"scenario": "routine"})
        assert client.get("/api/v1/runs/hold").status_code == 404


def test_live_agent_selects_tools_observes_results_and_cannot_override_block():
    seen_model_inputs = []
    def external(request):
        if request.url.host == "generativelanguage.googleapis.com":
            body = json.loads(request.content)
            seen_model_inputs.append(body)
            text = json.dumps(body)
            if '"functionResponse"' not in text:
                call = {"name": "sim_swap", "args": {"reason": "Check recent SIM changes"}}
            elif '"device_swap"' not in json.dumps(body["contents"]):
                call = {"name": "device_swap", "args": {"reason": "Compare device change with the SIM observation"}}
            else:
                call = {"name": "finish", "args": {"decision": "APPROVE", "reason": "No further checks"}}
            return httpx.Response(200, json={"candidates": [{"content": {"role": "model", "parts": [{"functionCall": call}]}}]})
        return httpx.Response(200, json={"swapped": True})

    with TestClient(create_app(database=":memory:", allow_live=True, external_transport=httpx.MockTransport(external),
                               nokia_key="test", gemini_key="test")) as client:
        client.post("/api/v1/sessions", json={"scenario": "sim_swap", "mode": "NOKIA_SANDBOX"})
        result = client.post("/api/v1/payments", json={"request_id": "agent", "amount": 200}).json()
        assert result["decision"] == "BLOCK"
        assert result["decision_source"] == "GEMINI_WITH_POLICY"
        assert result["model_calls"] >= 2
        assert {e["tool"] for e in result["evidence"]} >= {"sim_swap", "device_swap"}
        assert "sim_swap" not in seen_model_inputs[0]["contents"][0]["parts"][0]["text"].split('"context"')[0]
        assert "scenario" not in json.dumps(seen_model_inputs[0]["contents"])
        agent_context = json.loads(seen_model_inputs[0]["contents"][0]["parts"][0]["text"])["context"]
        assert agent_context["transaction"] == {
            "amount": 200.0, "recipient_relationship": "family", "country": "EG",
            "channel": "INSTANT_PAYMENT",
        }
        assert agent_context["pre_call_score"] >= 20
        assert agent_context["pre_call_reasons"]


@pytest.mark.parametrize("recipient,channel", [
    ("family", "CARD_CHECKOUT"),
    ("merchant", "INSTANT_PAYMENT"),
    ("new_payee", "WALLET_TRANSFER"),
])
def test_agent_receives_the_actual_payment_channel(recipient, channel):
    observed = {}

    def external(request):
        observed.update(json.loads(request.content))
        call = {"name": "finish", "args": {"decision": "RETRY", "reason": "No provider calls in this test"}}
        return httpx.Response(200, json={"candidates": [{"content": {"role": "model", "parts": [{"functionCall": call}]}}]})

    with TestClient(create_app(database=":memory:", allow_live=True, external_transport=httpx.MockTransport(external),
                               nokia_key="test", gemini_key="test")) as client:
        client.post("/api/v1/sessions", json={"scenario": "card_misuse", "mode": "NOKIA_SANDBOX"})
        response = client.post("/api/v1/payments", json={
            "request_id": channel,
            "amount": 200,
            "recipient": recipient,
            "channel": channel,
        })
        assert response.status_code == 200
    context = json.loads(observed["contents"][0]["parts"][0]["text"])["context"]
    assert context["transaction"]["recipient_relationship"] == recipient
    assert context["transaction"]["channel"] == channel


def test_model_block_proposal_cannot_override_deterministic_hold():
    calls = 0

    def external(request):
        nonlocal calls
        if request.url.host == "generativelanguage.googleapis.com":
            calls += 1
            if calls == 1:
                call = {"name": "sim_swap", "args": {"reason": "Confirm recent SIM state"}}
            elif calls == 2:
                call = {"name": "number_verification", "args": {"reason": "Confirm bearer identity"}}
            else:
                call = {"name": "finish", "args": {"decision": "BLOCK", "reason": "Manual fraud review required"}}
            return httpx.Response(200, json={"candidates": [{"content": {"role": "model", "parts": [{"functionCall": call}]}}]})
        if request.url.path.endswith("clientcredentials"):
            return httpx.Response(200, json={"client_id": "client"})
        if "well-known" in request.url.path:
            return httpx.Response(200, json={"fast_flow_csp_auth_endpoint":
                "https://nb-auth.nac-runtime-stg-eu.g002.saas.nokia.com/oauth2/v1/retrieve_csp_auth_url"})
        if request.url.path.endswith("retrieve_csp_auth_url"):
            params = dict(request.url.params)
            return httpx.Response(302, headers={
                "location": params["redirect_uri"] + "?code=code&state=" + params["state"],
            })
        if request.url.path.endswith("/verify"):
            return httpx.Response(200, json={"devicePhoneNumberVerified": True})
        return httpx.Response(200, json={"swapped": False})

    with TestClient(create_app(database=":memory:", allow_live=True, external_transport=httpx.MockTransport(external),
                               nokia_key="test", gemini_key="test")) as client:
        client.post("/api/v1/sessions", json={"scenario": "scam_transfer", "mode": "NOKIA_SANDBOX"})
        result = client.post("/api/v1/payments", json={"request_id": "agent-block", "amount": 200,
                                                       "recipient": "new_payee"}).json()
        assert result["agent_proposal"] == "BLOCK"
        assert result["decision"] == "HOLD"
        assert result["decision_source"] == "GEMINI_WITH_POLICY"


def test_model_cannot_turn_rate_limited_nokia_evidence_into_a_network_block():
    model_calls = 0

    def external(request):
        nonlocal model_calls
        if request.url.host == "generativelanguage.googleapis.com":
            model_calls += 1
            call = (
                {"name": "sim_swap", "args": {"reason": "Check recent SIM state"}}
                if model_calls == 1
                else {"name": "finish", "args": {"decision": "BLOCK", "reason": "Protective review"}}
            )
            return httpx.Response(200, json={
                "candidates": [{"content": {"role": "model", "parts": [{"functionCall": call}]}}],
            })
        return httpx.Response(429, json={"message": "Too many requests"})

    with TestClient(create_app(database=":memory:", allow_live=True,
            external_transport=httpx.MockTransport(external), nokia_key="test", gemini_key="test")) as client:
        client.post("/api/v1/sessions", json={"scenario": "sim_swap", "mode": "NOKIA_SANDBOX"})
        result = client.post("/api/v1/payments", json={
            "request_id": "rate-limited",
            "amount": 200,
            "recipient": "family",
        }).json()

        assert result["agent_proposal"] == "BLOCK"
        assert result["decision"] == "RETRY"
        assert result["final_risk_score"] == 35
        assert result["evidence"][0]["status"] == "UNKNOWN"
        assert result["evidence"][0]["http_status"] == 429


def test_live_agent_that_exhausts_its_tool_budget_fails_closed():
    requested = iter(["sim_swap", "device_swap", "roaming", "reachability", "number_verification"])

    def external(request):
        if request.url.host == "generativelanguage.googleapis.com":
            call = {"name": next(requested), "args": {"reason": "Collect bounded evidence"}}
            return httpx.Response(200, json={"candidates": [{"content": {"role": "model", "parts": [{"functionCall": call}]}}]})
        if request.url.path.endswith("clientcredentials"):
            return httpx.Response(200, json={"client_id": "client"})
        if "well-known" in request.url.path:
            return httpx.Response(200, json={"fast_flow_csp_auth_endpoint":
                "https://nb-auth.nac-runtime-stg-eu.g002.saas.nokia.com/oauth2/v1/retrieve_csp_auth_url"})
        if request.url.path.endswith("retrieve_csp_auth_url"):
            params = dict(request.url.params)
            return httpx.Response(302, headers={"location": params["redirect_uri"] + "?code=code&state=" + params["state"]})
        if request.url.path.endswith("/verify"):
            return httpx.Response(200, json={"devicePhoneNumberVerified": True})
        field = "roaming" if "roaming" in request.url.path else "reachable" if "reachability" in request.url.path else "swapped"
        return httpx.Response(200, json={field: False})

    with TestClient(create_app(database=":memory:", allow_live=True, external_transport=httpx.MockTransport(external),
                               nokia_key="test", gemini_key="test")) as client:
        client.post("/api/v1/sessions", json={"scenario": "legitimate_travel", "mode": "NOKIA_SANDBOX"})
        result = client.post("/api/v1/payments", json={"request_id": "budget", "amount": 200,
                                                       "recipient": "new_payee"}).json()
        assert result["agent_proposal"] is None
        assert result["decision"] == "RETRY"
        assert result["decision_source"] == "POLICY_FAIL_CLOSED"


def test_live_agent_rejects_a_repeated_tool_without_a_second_telecom_call():
    model_calls = 0

    def external(request):
        nonlocal model_calls
        if request.url.host == "generativelanguage.googleapis.com":
            model_calls += 1
            call = {"name": "sim_swap", "args": {"reason": "Check recent SIM state"}}
            return httpx.Response(200, json={
                "candidates": [{"content": {"role": "model", "parts": [{"functionCall": call}]}}],
            })
        return httpx.Response(200, json={"swapped": False})

    with TestClient(create_app(database=":memory:", allow_live=True,
            external_transport=httpx.MockTransport(external), nokia_key="test", gemini_key="test")) as client:
        client.post("/api/v1/sessions", json={"scenario": "scam_transfer", "mode": "NOKIA_SANDBOX"})
        result = client.post("/api/v1/payments", json={
            "request_id": "repeat-tool",
            "amount": 200,
            "recipient": "new_payee",
        }).json()

        assert result["decision"] == "RETRY"
        assert result["agent_error"] == "ValueError"
        assert result["model_calls"] == 2
        assert result["telecom_calls"] == 1
        assert [item["tool"] for item in result["evidence"]] == ["sim_swap"]


def test_live_agent_rejects_a_tool_call_without_a_reason_before_network_access():
    def external(request):
        if request.url.host != "generativelanguage.googleapis.com":
            pytest.fail("Malformed tool call must not reach Nokia")
        call = {"name": "sim_swap", "args": {}}
        return httpx.Response(200, json={
            "candidates": [{"content": {"role": "model", "parts": [{"functionCall": call}]}}],
        })

    with TestClient(create_app(database=":memory:", allow_live=True,
            external_transport=httpx.MockTransport(external), nokia_key="test", gemini_key="test")) as client:
        client.post("/api/v1/sessions", json={"scenario": "scam_transfer", "mode": "NOKIA_SANDBOX"})
        result = client.post("/api/v1/payments", json={
            "request_id": "missing-reason",
            "amount": 200,
            "recipient": "new_payee",
        }).json()

        assert result["decision"] == "RETRY"
        assert result["agent_error"] == "ValueError"
        assert result["telecom_calls"] == 0


def test_concurrent_enrollment_preserves_payment_attempt_history():
    enrollment_started = asyncio.Event()
    release_enrollment = asyncio.Event()

    async def external(request):
        if request.url.path.endswith("clientcredentials"):
            enrollment_started.set()
            await release_enrollment.wait()
            return httpx.Response(200, json={"client_id": "client"})
        if "well-known" in request.url.path:
            return httpx.Response(200, json={"fast_flow_csp_auth_endpoint":
                "https://nb-auth.nac-runtime-stg-eu.g002.saas.nokia.com/oauth2/v1/retrieve_csp_auth_url"})
        if request.url.path.endswith("retrieve_csp_auth_url"):
            params = dict(request.url.params)
            return httpx.Response(302, headers={
                "location": params["redirect_uri"] + "?code=code&state=" + params["state"],
            })
        if request.url.path.endswith("/verify"):
            return httpx.Response(200, json={"devicePhoneNumberVerified": True})
        return httpx.Response(200, json={"swapped": False})

    async def run():
        app = create_app(database=":memory:", allow_live=True,
                         external_transport=httpx.MockTransport(external), nokia_key="test", gemini_key="test")
        async with (
            app.router.lifespan_context(app),
            httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client,
        ):
                await client.post("/api/v1/sessions", json={"scenario": "new_device", "mode": "NOKIA_SANDBOX"})
                session_id = client.cookies.get("safepay_session")
                enrollment = asyncio.create_task(client.post(
                    "/api/v1/enrollments", json={"request_id": "concurrent-enrollment"}
                ))
                await enrollment_started.wait()
                for index in range(3):
                    response = await client.post("/api/v1/payments", json={
                        "request_id": f"waiting-payment-{index}", "amount": 10,
                    })
                    assert response.json()["decision"] == "VERIFY_DEVICE"
                release_enrollment.set()
                assert (await enrollment).json()["decision"] == "TRUST_ESTABLISHED"
                row = app.state.db.execute("SELECT data FROM sessions WHERE id=?", (session_id,)).fetchone()
                assert len(json.loads(row[0])["attempt_times"]) == 3

    asyncio.run(run())


def test_cancelling_a_live_run_stops_later_external_calls():
    tool_started = asyncio.Event()
    release_tool = asyncio.Event()
    calls = {"model": 0, "nokia": 0}

    async def external(request):
        if request.url.host == "generativelanguage.googleapis.com":
            calls["model"] += 1
            call = ({"name": "sim_swap", "args": {"reason": "Check SIM state"}}
                    if calls["model"] == 1 else
                    {"name": "finish", "args": {"decision": "HOLD", "reason": "Review"}})
            return httpx.Response(200, json={
                "candidates": [{"content": {"role": "model", "parts": [{"functionCall": call}]}}],
            })
        calls["nokia"] += 1
        tool_started.set()
        await release_tool.wait()
        return httpx.Response(200, json={"swapped": False})

    async def run():
        app = create_app(database=":memory:", allow_live=True,
                         external_transport=httpx.MockTransport(external), nokia_key="test", gemini_key="test")
        async with (
            app.router.lifespan_context(app),
            httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client,
        ):
                await client.post("/api/v1/sessions", json={
                    "scenario": "scam_transfer", "mode": "NOKIA_SANDBOX",
                })
                payment = asyncio.create_task(client.post("/api/v1/payments", json={
                    "request_id": "cancel-live", "amount": 200, "recipient": "new_payee",
                }))
                await tool_started.wait()
                cancelled = await client.post("/api/v1/runs/cancel-live/cancel")
                release_tool.set()
                completed = await payment

                assert cancelled.json()["decision"] == "CANCELLED"
                assert completed.json()["decision"] == "CANCELLED"
                assert calls == {"model": 1, "nokia": 1}

    asyncio.run(run())


def test_cancelling_while_gemini_is_pending_prevents_its_tool_call():
    model_started = asyncio.Event()
    release_model = asyncio.Event()
    calls = {"model": 0, "nokia": 0}

    async def external(request):
        if request.url.host == "generativelanguage.googleapis.com":
            calls["model"] += 1
            model_started.set()
            await release_model.wait()
            call = {"name": "sim_swap", "args": {"reason": "Check SIM state"}}
            return httpx.Response(200, json={
                "candidates": [{"content": {"role": "model", "parts": [{"functionCall": call}]}}],
            })
        calls["nokia"] += 1
        return httpx.Response(200, json={"swapped": False})

    async def run():
        app = create_app(database=":memory:", allow_live=True,
                         external_transport=httpx.MockTransport(external), nokia_key="test", gemini_key="test")
        async with (
            app.router.lifespan_context(app),
            httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client,
        ):
                await client.post("/api/v1/sessions", json={
                    "scenario": "scam_transfer", "mode": "NOKIA_SANDBOX",
                })
                payment = asyncio.create_task(client.post("/api/v1/payments", json={
                    "request_id": "cancel-model", "amount": 200, "recipient": "new_payee",
                }))
                await model_started.wait()
                cancelled = await client.post("/api/v1/runs/cancel-model/cancel")
                release_model.set()
                completed = await payment

                assert cancelled.json()["decision"] == "CANCELLED"
                assert completed.json()["decision"] == "CANCELLED"
                assert calls == {"model": 1, "nokia": 0}

    asyncio.run(run())


def test_cancelling_live_enrollment_stops_later_oauth_calls():
    credentials_started = asyncio.Event()
    release_credentials = asyncio.Event()
    paths = []

    async def external(request):
        paths.append(request.url.path)
        if request.url.path.endswith("clientcredentials"):
            credentials_started.set()
            await release_credentials.wait()
            return httpx.Response(200, json={"client_id": "client"})
        if "well-known" in request.url.path:
            return httpx.Response(200, json={"fast_flow_csp_auth_endpoint":
                "https://nb-auth.nac-runtime-stg-eu.g002.saas.nokia.com/oauth2/v1/retrieve_csp_auth_url"})
        return httpx.Response(500)

    async def run():
        app = create_app(database=":memory:", allow_live=True,
                         external_transport=httpx.MockTransport(external), nokia_key="test", gemini_key="test")
        async with (
            app.router.lifespan_context(app),
            httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client,
        ):
            await client.post("/api/v1/sessions", json={
                "scenario": "first_setup", "mode": "NOKIA_SANDBOX",
            })
            enrollment = asyncio.create_task(client.post(
                "/api/v1/enrollments", json={"request_id": "cancel-enrollment"},
            ))
            await credentials_started.wait()
            cancelled = await client.post("/api/v1/runs/cancel-enrollment/cancel")
            release_credentials.set()
            completed = await enrollment

            assert cancelled.json()["decision"] == "CANCELLED"
            assert completed.json()["decision"] == "CANCELLED"
            assert paths == ["/oauth2/v1/auth/clientcredentials"]

    asyncio.run(run())


def test_live_enrollment_does_not_silently_use_fixtures_on_provider_failure():
    with TestClient(create_app(database=":memory:", allow_live=True, nokia_key="test",
            external_transport=httpx.MockTransport(lambda r: httpx.Response(503)))) as client:
        client.post("/api/v1/sessions", json={"scenario": "first_setup", "mode": "NOKIA_SANDBOX"})
        result = client.post("/api/v1/enrollments", json={"request_id": "setup"}).json()
        assert result["decision"] == "RETRY"
        assert len(result["evidence"]) == 2
        assert all(e["source"] == "NOKIA_SANDBOX" and e["status"] == "UNKNOWN" for e in result["evidence"])
        assert client.post("/api/v1/payments", json={"request_id": "payment", "amount": 1}).json()["decision"] == "VERIFY_DEVICE"


def test_live_enrollment_with_malformed_oauth_metadata_is_recoverable():
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json=[]))
    with TestClient(create_app(database=":memory:", allow_live=True, nokia_key="test",
                               external_transport=transport)) as client:
        client.post("/api/v1/sessions", json={"scenario": "first_setup", "mode": "NOKIA_SANDBOX"})
        response = client.post("/api/v1/enrollments", json={"request_id": "malformed-oauth"})
        assert response.status_code == 200
        assert response.json()["decision"] == "RETRY"
        assert client.get("/api/v1/runs/malformed-oauth").json()["decision"] == "RETRY"


def test_public_demo_exposes_catalog_and_blocks_unapproved_live_spending():
    with TestClient(create_app(database=":memory:")) as client:
        catalog = client.get("/api/v1/catalog").json()
        assert set(catalog["countries"]) == {"EG", "SA", "AE"}
        assert catalog["live_enabled"] is False
        assert client.post("/api/v1/sessions", json={"mode": "NOKIA_SANDBOX"}).status_code == 403
        assert client.post("/api/v1/payments", json={"request_id": "forged", "amount": 1}).status_code == 401
        assert client.get("/api/v1/telecom/nokia-probe").status_code in (404, 410)


def test_session_payment_velocity_cannot_keep_taking_zero_call_path():
    with TestClient(create_app(database=":memory:")) as client:
        client.post("/api/v1/sessions", json={"scenario": "routine"})
        for index in range(5):
            result = client.post("/api/v1/payments", json={"request_id": str(index), "amount": 10}).json()
        assert result["decision"] == "HOLD"
        assert result["pre_call_score"] >= 20
        assert result["evidence"]


@pytest.mark.parametrize("content", [None, {"parts": [{"functionCall": {"name": "finish", "args": None}}]}])
def test_malformed_model_response_becomes_recoverable_not_stuck(content):
    transport = httpx.MockTransport(lambda r: httpx.Response(200, json={"candidates": [{"content": content}]}))
    with TestClient(create_app(allow_live=True, external_transport=transport, nokia_key="test", gemini_key="test")) as client:
        client.post("/api/v1/sessions", json={"scenario": "sim_swap", "mode": "NOKIA_SANDBOX"})
        response = client.post("/api/v1/payments", json={"request_id": "bad-model", "amount": 200})
        assert response.status_code == 200
        assert response.json()["decision"] == "RETRY"
        assert client.get("/api/v1/runs/bad-model").json()["decision"] == "RETRY"


def test_sandbox_rejects_fixture_only_outage_scenario():
    with TestClient(create_app(allow_live=True)) as client:
        response = client.post("/api/v1/sessions", json={"scenario": "provider_outage", "mode": "NOKIA_SANDBOX"})
        assert response.status_code == 422


def test_evaluation_reports_actual_public_workflow_outcomes():
    with TestClient(create_app()) as client:
        result = client.post("/api/v1/evaluations").json()
        assert result["failed"] == 0
        assert result["passed"] == 36
        assert result["mode"] == "FIXTURE"
        assert result["checks"] == {
            "decision": {"passed": 36, "failed": 0},
            "tool_plan": {"passed": 36, "failed": 0},
            "evidence_status": {"passed": 36, "failed": 0},
            "no_external_calls": {"passed": 36, "failed": 0},
        }
        assert all(all(row["checks"].values()) for row in result["cases"])
        routine = [row for row in result["cases"] if row["scenario"] == "routine"]
        assert all(row["actual_tools"] == [] for row in routine)
        investigated = [row for row in result["cases"] if row["scenario"] == "sim_swap"]
        assert all(set(row["actual_tools"]) == {"sim_swap", "number_verification", "device_swap"}
                   for row in investigated)
