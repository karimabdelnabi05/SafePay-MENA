"""Run a controlled Nokia sandbox check using only documented simulator subjects."""

import argparse
import asyncio

import httpx

from app.config import settings
from app.services.nokia import NokiaGateway

TOOLS = ("sim_swap", "number_verification", "device_swap", "roaming", "reachability")
SUBJECTS = ("+99999991000", "+99999991001")


async def verify(subject: str, tools: tuple[str, ...]) -> int:
    if not settings.NOKIA_RAPIDAPI_KEY:
        print("Nokia sandbox key is not configured.")
        return 1

    failures = 0
    async with httpx.AsyncClient() as client:
        gateway = NokiaGateway(settings.NOKIA_RAPIDAPI_KEY, client)
        for tool in tools:
            result = await gateway.check(tool, subject)
            print({
                "tool": tool,
                "subject": subject,
                "status": result["status"],
                "http_status": result.get("http_status"),
                "data": result["data"],
                "error": result.get("error"),
                "latency_ms": result["latency_ms"],
            })
            failures += result["status"] != "SUCCESS"
    return 0 if failures == 0 else 2


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Nokia Network as Code sandbox access")
    parser.add_argument("--subject", choices=SUBJECTS, default=SUBJECTS[0])
    parser.add_argument("--all", action="store_true", help="Run all five logical CAMARA tools")
    args = parser.parse_args()
    selected = TOOLS if args.all else ("sim_swap",)
    return asyncio.run(verify(args.subject, selected))


if __name__ == "__main__":
    raise SystemExit(main())
