"""Repeatable acceptance evaluation through HTTP, with independent expected outcomes."""

import time
from datetime import datetime, timezone

import httpx

CASES = [
    ("routine", "payment", "family", "APPROVE"),
    ("first_setup", "enrollment", "family", "TRUST_ESTABLISHED"),
    ("new_device", "enrollment", "family", "TRUST_ESTABLISHED"),
    ("scam_transfer", "payment", "new_payee", "HOLD"),
    ("sim_swap", "payment", "new_payee", "BLOCK"),
    ("card_misuse", "payment", "merchant", "BLOCK"),
    ("combined_attack", "payment", "wallet", "BLOCK"),
    ("legitimate_travel", "payment", "new_payee", "APPROVE"),
    ("velocity", "payment", "new_payee", "HOLD"),
    ("provider_outage", "payment", "new_payee", "RETRY"),
    ("enrollment_outage", "enrollment", "family", "RETRY"),
    ("identity_mismatch", "payment", "new_payee", "HOLD"),
]


async def evaluate():
    from app.api import create_app
    app = create_app()
    rows = []
    start = time.perf_counter()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://evaluation") as client:
        for country in ("EG", "SA", "AE"):
            for scenario, kind, recipient, expected in CASES:
                await client.post("/api/v1/sessions", json={"country": country, "scenario": scenario})
                payload = {"request_id": "evaluation"}
                if kind == "payment":
                    payload.update(amount=200, recipient=recipient)
                response = await client.post("/api/v1/enrollments" if kind == "enrollment" else "/api/v1/payments", json=payload)
                actual = response.json().get("decision", "ERROR")
                rows.append({"country": country, "scenario": scenario, "expected": expected, "actual": actual,
                             "passed": response.status_code == 200 and actual == expected})
    return {"mode": "FIXTURE", "passed": sum(row["passed"] for row in rows),
            "failed": sum(not row["passed"] for row in rows), "cases": rows,
            "elapsed_ms": round((time.perf_counter() - start) * 1000, 2),
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
            "scope": "Synthetic acceptance cases; not measured real-world fraud detection accuracy"}
