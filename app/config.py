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

settings = Settings()
