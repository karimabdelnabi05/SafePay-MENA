"""
SafePay MENA - Application Configuration
Supports local deterministic development and live carrier/Gemini integrations.
"""

import os
from pathlib import Path

from pydantic import BaseModel


def _load_env_file():
    """Robust .env loader supporting both 'KEY=VALUE' and 'KEY: VALUE' format."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        k, v = line.split("=", 1)
                    elif ":" in line:
                        k, v = line.split(":", 1)
                    else:
                        continue
                    k = k.strip()
                    v = v.strip().strip("\"'")
                    if k and v and k not in os.environ:
                        os.environ[k] = v
        except OSError:
            return

_load_env_file()

class Settings(BaseModel):
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    NOKIA_RAPIDAPI_KEY: str = os.getenv("NOKIA_RAPIDAPI_KEY", "")
    SAFEPAY_JUDGE_ACCESS_CODE: str = os.getenv("SAFEPAY_JUDGE_ACCESS_CODE", "")

    @property
    def live_run_limit(self):
        return _positive_int("SAFEPAY_LIVE_RUN_LIMIT", 4)

    @property
    def live_global_limit(self):
        return _positive_int("SAFEPAY_LIVE_GLOBAL_LIMIT", 12)


def _positive_int(name, default):
    try:
        return max(1, int(os.getenv(name, str(default))))
    except ValueError:
        return default

settings = Settings()
