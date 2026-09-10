import json
import os
import subprocess
import sys

import pytest


@pytest.mark.parametrize(("live_flag", "nokia_key", "gemini_key", "access_code", "expected"), [
    ("false", "nokia", "gemini", "judges-only", False),
    ("true", "nokia", "", "judges-only", False),
    ("true", "", "gemini", "judges-only", False),
    ("true", "nokia", "gemini", "", False),
    ("true", "nokia", "gemini", "short", False),
    ("true", "nokia", "gemini", "judges-only", True),
])
def test_live_mode_requires_flag_credentials_and_access_code(
    live_flag, nokia_key, gemini_key, access_code, expected,
):
    environment = {
        **os.environ,
        "SAFEPAY_ENABLE_LIVE": live_flag,
        "NOKIA_RAPIDAPI_KEY": nokia_key,
        "GEMINI_API_KEY": gemini_key,
        "SAFEPAY_JUDGE_ACCESS_CODE": access_code,
    }
    script = """
import json
from fastapi.testclient import TestClient
from app.main import LIVE_READY, app

with TestClient(app) as client:
    health = client.get('/api/v1/health').json()
print(json.dumps({'live_ready': LIVE_READY, 'health': health}))
"""
    completed = subprocess.run(
        [sys.executable, "-c", script],
        check=True,
        capture_output=True,
        text=True,
        env=environment,
    )
    result = json.loads(completed.stdout)

    assert result["live_ready"] is expected
    assert result["health"]["mode"] == ("SANDBOX_ENABLED" if expected else "FIXTURE_ONLY")
    assert result["health"]["production_networks"] is False
