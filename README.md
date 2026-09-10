# SafePay MENA

SafePay MENA is a GSMA MENA Ignite Phase 2 working prototype for adding telecom evidence to payment-release decisions.

Routine payments stay on a local zero-call path. In live sandbox mode, elevated-risk payments trigger a bounded Gemini function-calling agent that selects relevant CAMARA APIs through Nokia Network as Code. Fixture mode provides the same repeatable policy paths without calling external services. Deterministic policy owns the final disposition in both modes.

> This is a hackathon prototype. Bank context is synthetic, Nokia calls use sandbox simulator subjects, and no production payment or mobile network is connected.

![SafePay MENA payment review](artifacts/safepay-desktop.png)

## Working Flows

- Everyday payment: immediate local approval with zero agent/API calls.
- First setup and new phone: mandatory fresh Number Verification and SIM Swap checks.
- Suspicious transfer: hold even when identity verifies, because identity does not prove safe intent.
- SIM-swap takeover: combine SIM, device, and session evidence.
- Card leakage: model checkout and registered-number mismatch separately from bank transfer.
- Planned travel: roaming is context, never fraud by itself.
- Provider outage: unknown evidence returns retry and never becomes a clean signal.
- Velocity: repeated payments remain in one session and leave the zero-call path.

Markets are represented as configurable demo contexts:

| Market | Currency | Instant-payment context |
|---|---|---|
| Egypt | EGP | InstaPay / IPN |
| Saudi Arabia | SAR | sarie |
| United Arab Emirates | AED | Aani |

This does not claim production operator coverage or regulatory certification in those markets.

## Architecture

    Payment context
          |
          v
    Local pre-screen -- routine --> APPROVE (zero external calls)
          |
          | elevated risk
          v
    Fixture tool plan or bounded Gemini agent
                   |
                   v
          Nokia/CAMARA observations
          |
          v
    Deterministic release policy --> APPROVE | HOLD | BLOCK | RETRY

The model receives amount, recipient relationship, country, payment channel, anomaly facts, and pre-screen reasons. It never receives the canned scenario label. Tool names, endpoints, simulator subjects, redirect hosts, repeat calls, and call budgets are enforced outside the model.

Implemented Nokia sandbox tools:

- SIM Swap
- Number Verification with bound OAuth state
- Device Swap
- Roaming
- Reachability

SafePay does not claim an active-call API. Provider errors and malformed responses are recorded as UNKNOWN.

## Run Locally

Use Python 3.11 or newer.

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements-dev.txt
    python -m uvicorn app.main:app --reload

Open http://127.0.0.1:8000.

Fixture mode works without credentials and remains available on every deployment.

## Optional Live Sandbox

Create .env from .env.example, then set:

    SAFEPAY_ENABLE_LIVE=true
    NOKIA_RAPIDAPI_KEY=your_key
    GEMINI_API_KEY=your_key
    SAFEPAY_JUDGE_ACCESS_CODE=choose_a_private_code

Connected mode is restricted to Nokia's documented +99999991000 and +99999991001 simulator subjects. It uses an HttpOnly judge-access grant and defaults to four runs per unlocked browser and twelve shared runs per hour. Override those limits with `SAFEPAY_LIVE_RUN_LIMIT` and `SAFEPAY_LIVE_GLOBAL_LIMIT`.

## Test

    python -m pytest -q --ignore=tests/test_browser.py

The in-product acceptance evaluation is also available from the web interface or:

    curl -X POST http://127.0.0.1:8000/api/v1/evaluations

It runs 36 synthetic cases across Egypt, Saudi Arabia, and the UAE. These results verify software behavior, not real-world fraud-detection accuracy.

Browser acceptance can be run against a local server:

    playwright install chromium
    $env:SAFEPAY_BROWSER_URL="http://127.0.0.1:8000"
    python -m pytest tests/test_browser.py -q

## API

| Endpoint | Purpose |
|---|---|
| POST /api/v1/sessions | Start an isolated one-hour demo session |
| POST /api/v1/enrollments | Establish fresh device trust |
| POST /api/v1/payments | Screen a payment with independent recipient relationship and channel fields |
| GET, POST, DELETE /api/v1/live-access | Read, unlock, or lock protected connected access |
| POST /api/v1/live-enrollments | Start a quota-controlled connected enrollment run |
| POST /api/v1/live-payments | Start a quota-controlled connected payment run |
| GET /api/v1/runs/{id} | Retrieve the stored result |
| POST /api/v1/runs/{id}/cancel | Cancel a pending or held run |
| POST /api/v1/evaluations | Run the synthetic acceptance suite |
| GET /api/v1/health | Deployment health check |

## Deploy

The included render.yaml declares protected connected mode. New Blueprints prompt for the Nokia key, Gemini key, and judge access code (at least eight characters). Existing services need these values entered manually in Environment. See [Render setup](docs_and_presentations/RENDER_CONNECTED_SETUP.md). If any required value is absent, startup safely exposes fixture mode only.

[Deploy to Render](https://render.com/deploy?repo=https://github.com/karimabdelnabi05/SafePay-MENA)

Render's official FastAPI instructions use pip install -r requirements.txt and Uvicorn bound to PORT: [Render FastAPI guide](https://render.com/docs/deploy-fastapi).

## Phase 2 Material

Build the required source upload from the committed release with `python build_submission.py` after installing development dependencies. It exports tracked files only, checks for accidental secrets, and runs the backend suite from the extracted ZIP. The output is `dist/SafePay_MENA_Source.zip` with a commit and SHA-256 manifest.

- [Prototype submission checklist](docs_and_presentations/PROTOTYPE_SUBMISSION_CHECKLIST.md): all form fields, required uploads, draft text and remaining release work.
- [Single submission presentation](docs_and_presentations/SafePay_MENA_Phase2_Pitch_Deck.pdf): 13 main slides plus financial, fraud-type and source evidence, ending with a technical summary in the same PDF.
- [Presentation source](docs_and_presentations/SafePay_MENA_Phase2_Slides.html) and [speaker notes / evidence ledger](docs_and_presentations/PHASE2_PITCH_NOTES.md).
- [Nokia sandbox verification](docs_and_presentations/NOKIA_SANDBOX_VERIFICATION.md)
- [Phase 2 QA report](docs_and_presentations/PHASE2_QA_REPORT.md)
- [Phase 2 rubric scorecard](docs_and_presentations/PHASE2_RUBRIC_SCORECARD.md)
- [Claim verification](docs_and_presentations/PHASE2_CLAIM_VERIFICATION.md)
- [Security threat model](SAFEPAY_SECURITY_THREAT_MODEL_AND_TRACES.md)
- [TDD build log](docs_and_presentations/TDD_BUILD_LOG.md)
