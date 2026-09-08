"""SafePay MENA web entry point."""

import os
from pathlib import Path

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api import create_app
from app.config import settings


STATIC_DIR = Path(__file__).parent / "static"
DATABASE = os.getenv("SAFEPAY_DATABASE", ":memory:")
LIVE_REQUESTED = os.getenv("SAFEPAY_ENABLE_LIVE", "false").lower() in {"1", "true", "yes"}
LIVE_READY = LIVE_REQUESTED and bool(settings.NOKIA_RAPIDAPI_KEY and settings.GEMINI_API_KEY)

app = create_app(
    database=DATABASE,
    allow_live=LIVE_READY,
    nokia_key=settings.NOKIA_RAPIDAPI_KEY,
    gemini_key=settings.GEMINI_API_KEY,
)


@app.get("/", include_in_schema=False)
async def index():
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
