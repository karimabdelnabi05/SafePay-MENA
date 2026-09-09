"""Repeatable acceptance evaluation through HTTP, with independent expected outcomes."""

import time
from datetime import datetime, timezone

import httpx

CASES = [
    ("routine", "payment", "family", "APPROVE", [], "SUCCESS", "LOCAL_SCREENING"),
    ("first_setup", "enrollment", "family", "TRUST_ESTABLISHED",
     ["number_verification", "sim_swap"], "SUCCESS", "MANDATORY_ENROLLMENT_POLICY"),
    ("new_device", "enrollment", "family", "TRUST_ESTABLISHED",
     ["number_verification", "sim_swap"], "SUCCESS", "MANDATORY_ENROLLMENT_POLICY"),
    ("scam_transfer", "payment", "new_payee", "HOLD",
     ["sim_swap", "number_verification"], "SUCCESS", "DETERMINISTIC_FIXTURE"),
    ("sim_swap", "payment", "new_payee", "BLOCK",
     ["sim_swap", "number_verification", "device_swap"], "SUCCESS", "DETERMINISTIC_FIXTURE"),
    ("card_misuse", "payment", "merchant", "BLOCK",
     ["sim_swap", "number_verification", "device_swap"], "SUCCESS", "DETERMINISTIC_FIXTURE"),
    ("combined_attack", "payment", "wallet", "BLOCK",
     ["sim_swap", "number_verification", "device_swap"], "SUCCESS", "DETERMINISTIC_FIXTURE"),
    ("legitimate_travel", "payment", "new_payee", "APPROVE",
     ["sim_swap", "number_verification", "roaming"], "SUCCESS", "DETERMINISTIC_FIXTURE"),
    ("velocity", "payment", "new_payee", "HOLD",
     ["sim_swap", "number_verification"], "SUCCESS", "DETERMINISTIC_FIXTURE"),
    ("provider_outage", "payment", "new_payee", "RETRY",
     ["sim_swap", "number_verification"], "UNKNOWN", "DETERMINISTIC_FIXTURE"),
    ("enrollment_outage", "enrollment", "family", "RETRY",
     ["number_verification", "sim_swap"], "UNKNOWN", "MANDATORY_ENROLLMENT_POLICY"),
    ("identity_mismatch", "payment", "new_payee", "HOLD",
     ["sim_swap", "number_verification"], "SUCCESS", "DETERMINISTIC_FIXTURE"),
]


async def evaluate():
    from app.api import create_app
    app = create_app()
    rows = []
    start = time.perf_counter()
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://evaluation") as client,
    ):
            for country in ("EG", "SA", "AE"):
                for scenario, kind, recipient, expected, expected_tools, expected_status, expected_source in CASES:
                    await client.post("/api/v1/sessions", json={"country": country, "scenario": scenario})
                    payload = {"request_id": "evaluation"}
                    if kind == "payment":
                        channel = {"card_misuse": "CARD_CHECKOUT", "combined_attack": "WALLET_TRANSFER"}.get(
                            scenario, "INSTANT_PAYMENT"
                        )
                        payload.update(amount=200, recipient=recipient, channel=channel)
                    response = await client.post(
                        "/api/v1/enrollments" if kind == "enrollment" else "/api/v1/payments", json=payload
                    )
                    result = response.json()
                    actual = result.get("decision", "ERROR")
                    actual_tools = [item.get("tool") for item in result.get("evidence", [])]
                    checks = {
                        "decision": response.status_code == 200 and actual == expected,
                        "tool_plan": actual_tools == expected_tools,
                        "evidence_status": all(
                            item.get("status") == expected_status for item in result.get("evidence", [])
                        ),
                        "no_external_calls": (
                            result.get("telecom_calls", 0) == 0 and result.get("model_calls", 0) == 0
                        ),
                    }
                    rows.append({"country": country, "scenario": scenario, "expected": expected, "actual": actual,
                                 "expected_tools": expected_tools, "actual_tools": actual_tools,
                                 "checks": checks, "passed": all(checks.values())})
    check_summary = {
        name: {
            "passed": sum(row["checks"][name] for row in rows),
            "failed": sum(not row["checks"][name] for row in rows),
        }
        for name in ("decision", "tool_plan", "evidence_status", "no_external_calls")
    }
    return {"mode": "FIXTURE", "passed": sum(row["passed"] for row in rows),
            "failed": sum(not row["passed"] for row in rows), "checks": check_summary, "cases": rows,
            "elapsed_ms": round((time.perf_counter() - start) * 1000, 2),
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
            "scope": "Synthetic acceptance cases; not measured real-world fraud detection accuracy"}
