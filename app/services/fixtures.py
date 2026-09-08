"""Explicit offline evidence for the demo; never used as a live failure fallback."""

from datetime import datetime, timezone


class FixtureGateway:
    def __init__(self, values=None):
        self.values = values or {"sim_swap": False, "number_verification": True}

    async def check(self, tool, phone=None):
        field = {"sim_swap": "swapped", "device_swap": "swapped",
                 "number_verification": "devicePhoneNumberVerified", "roaming": "roaming",
                 "reachability": "reachable"}.get(tool)
        value = self.values.get(tool)
        return {"tool": tool, "source": "FIXTURE", "status": "SUCCESS" if field and value is not None else "UNKNOWN",
                "data": {field: value} if field and value is not None else {},
                "observed_at": datetime.now(timezone.utc).isoformat(), "latency_ms": 0,
                "http_status": None, "endpoint": None}
