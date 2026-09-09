import asyncio
import time

import httpx

from app.api import create_app


def test_parallel_routine_reviews_remain_isolated_and_zero_call():
    app = create_app(database=":memory:")
    transport = httpx.ASGITransport(app=app)

    async def review(index):
        async with httpx.AsyncClient(transport=transport, base_url="http://quality") as client:
            country = ("EG", "SA", "AE")[index % 3]
            session = await client.post("/api/v1/sessions", json={
                "scenario": "routine",
                "country": country,
            })
            result = await client.post("/api/v1/payments", json={
                "request_id": f"parallel-{index}",
                "amount": 200,
                "recipient": "family",
                "channel": "INSTANT_PAYMENT",
            })
            return session, result

    async def run():
        async with app.router.lifespan_context(app):
            return await asyncio.gather(*(review(index) for index in range(60)))

    started = time.perf_counter()
    results = asyncio.run(run())
    elapsed_ms = (time.perf_counter() - started) * 1000

    assert all(session.status_code == 200 and result.status_code == 200
               for session, result in results)
    payloads = [result.json() for _, result in results]
    assert all(payload["decision"] == "APPROVE" for payload in payloads)
    assert all(payload["telecom_calls"] == 0 and payload["model_calls"] == 0
               for payload in payloads)
    assert elapsed_ms < 3000
