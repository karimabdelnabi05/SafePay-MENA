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
        except Exception:
            pass

_load_env_file()

class Settings(BaseModel):
    PROJECT_NAME: str = "SafePay MENA"
    PROJECT_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # Execution mode (defaults to False if an API key is provided, actively attempting live carrier connection)
    USE_MOCK_TELECOM: bool = os.getenv("USE_MOCK_TELECOM", "false").lower() in ("true", "1", "yes")
    
    # External API Keys (supports both NOKIA_RAPIDAPI_KEY and Netwrok_as_code_api_key)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    NOKIA_RAPIDAPI_KEY: str = os.getenv("NOKIA_RAPIDAPI_KEY") or os.getenv("Netwrok_as_code_api_key") or ""
    NOKIA_API_BASE_URL: str = os.getenv("NOKIA_API_BASE_URL", "https://network-as-code.p.rapidapi.com")
    
    # Regional Thresholds
    SAMA_INSTANT_LIMIT_SAR: float = 20000.0  # SAMA Sarie 20k SAR Instant Threshold
    INSTAPAY_DAILY_LIMIT_EGP: float = 70000.0 # CBE InstaPay Transaction Limit
    AANI_INSTANT_LIMIT_AED: float = 50000.0  # CBUAE Aani Instant Limit
    
    # Caching
    SIM_SWAP_CACHE_TTL_SECONDS: int = 900  # 15 minutes TTL for SIM swap checks

settings = Settings()

