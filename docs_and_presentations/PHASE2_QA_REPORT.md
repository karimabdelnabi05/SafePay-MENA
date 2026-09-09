# SafePay MENA Phase 2 QA Report

Reviewed: 9 September 2026

## Release Assessment

The current prototype is ready for a controlled Phase 2 demonstration in fixture mode. Its supported claims are software behavior, bounded agent orchestration, and sandbox integration evidence. It is not a production payment system, a calibrated fraud model, or proof of operator coverage.

## Automated Results

| Gate | Result | What it establishes |
|---|---:|---|
| Backend and adapter suite | 75 passed | HTTP workflows, policy, idempotency, session isolation, Nokia adapter, startup controls, concurrency, and agent guardrails |
| Browser suite | 19 passed | Desktop/mobile journeys, all major outcomes, cancellation, session recovery, state reset, and visible evaluation output |
| Application coverage | 86% | Core deterministic policy 100%; HTTP API 96%; Nokia adapter 91%; investigator 87% |
| In-product evaluation | 36/36 | Expected decision, exact tool plan, evidence status, and zero external calls in fixture mode |
| Repeated evaluation | 360/360 | Ten consecutive 36-case runs; 102.63-130.85 ms per run, 120.17 ms mean locally |
| Concurrency check | 60/60 | Isolated routine reviews completed locally in 160 ms with zero external calls |
| Ruff | Pass | No lint findings |
| Bandit | Pass | No reported Python security findings |
| pip-audit | Pass | No known vulnerabilities in runtime requirements |

Timings are single-machine development observations, not production latency or capacity guarantees. Synthetic case results validate expected control flow, not real-world fraud-detection accuracy.

## Scenario Coverage

The repeatable fixture gate covers Egypt, Saudi Arabia, and the UAE for each of these flows:

| Scenario | Expected action | Evidence behavior |
|---|---|---|
| Routine payment | APPROVE | Local screen; no agent or CAMARA call |
| First setup | TRUST_ESTABLISHED | Mandatory Number Verification and SIM Swap |
| New device | TRUST_ESTABLISHED | Mandatory Number Verification and SIM Swap |
| Suspicious transfer | HOLD | Identity checks cannot prove safe payment intent |
| Recent SIM swap | BLOCK | SIM and device/session evidence combine under deterministic policy |
| Card misuse | BLOCK | Checkout channel and identity mismatch remain independent inputs |
| Combined takeover | BLOCK | Multiple network observations support the decision |
| Legitimate travel | APPROVE | Roaming is context and is not treated as fraud by itself |
| Payment velocity | HOLD | Repeated attempts leave the zero-call path |
| Provider outage | RETRY | UNKNOWN evidence never becomes a clean result |
| Enrollment outage | RETRY | Device trust is not created without successful evidence |
| Number mismatch | HOLD | Identity mismatch prevents automatic release |

The browser suite also verifies held-payment cancellation, session continuity after enrollment, country-specific currency and rail labels, stale-result clearing, safe text rendering, and layout overflow at desktop and mobile sizes.

## Live Sandbox Evidence

Controlled Nokia Network as Code calls used only Nokia simulator subjects. A live first-setup run returned successful Number Verification and SIM Swap evidence. A live suspicious-transfer run completed Gemini orchestration with two successful Nokia tool observations and returned HOLD.

Later SIM Swap, Device Swap, Roaming, and Reachability probes returned HTTP 429 from the RapidAPI free plan. Testing stopped to avoid consuming more quota. The adapter records 429 as UNKNOWN, and a regression test proves that a Gemini BLOCK proposal cannot convert rate-limited evidence into a network-supported block; the result is RETRY.

Live evidence is documented in [NOKIA_SANDBOX_VERIFICATION.md](NOKIA_SANDBOX_VERIFICATION.md). No real subscriber number, real payment, or production operator network was used.

## Defects Corrected

- Clean telecom evidence previously erased high-value/new-payee context; final policy now preserves relevant pre-call risk and reasons.
- A model BLOCK proposal could previously create a block without sufficient deterministic evidence; policy now caps unsupported proposals at HOLD or RETRY.
- RapidAPI rate limiting could combine with the same model override defect; HTTP 429 now remains explicit UNKNOWN evidence and fails recoverably.
- Recipient relationship was used to infer payment channel; channel is now an independent validated request field.
- A failed enrollment offered a misleading payment-review action; the UI now offers device-verification retry.
- An expired server session left the browser reusing a stale local signature; HTTP 401 now clears local session trust so retry creates a fresh session.
- A delayed cancellation response could overwrite a newer review; browser operations now ignore responses from superseded generations.
- Concurrent enrollment could overwrite payment-attempt history read before provider calls; enrollment now merges trust into the latest session state.
- Cancelling an in-flight live review allowed later agent/provider calls; the bounded investigator now checks cancellation before every new external call.
- SQLite connections created by app instances were not closed; FastAPI lifespan shutdown now closes them and the suite runs without resource warnings.
- A misspelled legacy environment-variable fallback could enable live mode unexpectedly; only the documented Nokia variable is accepted.
- The Nokia probe could encourage broad live calls; it now defaults to one bounded simulator check and requires `--all` for the five-tool set.
- Unused prototype modules containing stale product and infrastructure claims were removed from the active repository.
- Pitch and demo materials were rebuilt to distinguish implemented behavior, sandbox evidence, and future commercial work.

## Remaining Boundaries

- Public deployment is fixture-only. Enabling live mode publicly still requires authentication, per-user quotas, rate limiting, and secret management.
- RapidAPI free-plan access was rate-limited during this review; current live availability is therefore not a release gate for the fixture demo.
- Storage is an in-memory SQLite demonstration store. It is not durable, multi-instance, or an audit system.
- Bank transaction context, payment execution, customer consent, operator production access, and hardware-bound device attestation are simulated or absent.
- Risk weights and scenarios are deterministic demonstration rules, not trained, calibrated, independently validated, or regulator-approved controls.
- SafePay does not implement or claim an active-call or Scam Signal API.

## Demo Recommendation

Use fixture mode for the judged end-to-end walkthrough because it is deterministic and quota-independent. Show the recorded live Nokia evidence separately, explain that the Gemini agent chooses tools only after local escalation, and use the 36-case gate to demonstrate repeatability. Do not enable live sandbox mode on an unauthenticated public URL.
