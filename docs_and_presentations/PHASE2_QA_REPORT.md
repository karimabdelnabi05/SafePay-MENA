# SafePay MENA Phase 2 QA Report

Reviewed: 10 September 2026

## Release Assessment

The current prototype is ready for a controlled Phase 2 demonstration with protected connected-sandbox mode and an explicit fixture fallback. The connected path is verified locally and still requires hosted activation and verification. Its supported claims are software behavior, bounded agent orchestration, and sandbox integration evidence. It is not a production payment system, a calibrated fraud model, or proof of operator coverage.

## Automated Results

| Gate | Result | What it establishes |
|---|---:|---|
| Backend and adapter suite | 79 passed | HTTP workflows, policy, idempotency, session isolation, Nokia adapter, startup controls, access and quotas, detached progress, concurrency, and agent guardrails |
| Browser suite | 24 passed | Desktop/mobile journeys, first-load gating, protected connected workflow, all major outcomes, cancellation, session recovery, state reset, and visible evaluation output |
| Application coverage | 84% | Core deterministic policy 100%; HTTP API 91%; Nokia adapter 91%; investigator 87%. Startup modules are exercised in subprocess tests and appear as 0% in this process-level report. |
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

The browser suite also verifies held-payment cancellation, session continuity after enrollment, country-specific currency and rail labels, stale-result clearing, safe text rendering, delayed/failed catalog loading, connected unlock and progress, outcome focus, and layout overflow at desktop, mobile, and landscape sizes.

## Live Sandbox Evidence

Controlled Nokia Network as Code calls used only Nokia simulator subjects. A live first-setup run returned successful Number Verification and SIM Swap evidence. A live suspicious-transfer run completed Gemini orchestration with two successful Nokia tool observations and returned HOLD.

On 10 September, the protected asynchronous judge path completed multiple genuine takeover reviews. In the final recorded run, Gemini selected SIM Swap, Number Verification and Device Swap from the contextually eligible tool set; all three Nokia observations returned SUCCESS and deterministic policy returned BLOCK. The timeline exposed local screening, each agent selection, each Nokia result and final policy while the run was active.

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
- Public connected mode now requires a private judge code, an HttpOnly two-hour grant, per-session and shared hourly limits, and dedicated asynchronous endpoints; legacy endpoints cannot bypass those limits.
- The browser previously submitted before the scenario catalog loaded; the form now remains unavailable until initialization succeeds.
- Gemini was initially offered irrelevant network tools during takeover review; tool declarations are now restricted by observable context and removed after use while the agent retains ordering and finish decisions.

## Remaining Boundaries

- Public deployment remains on the earlier fixture-only release until the new code and three private Render environment values are deployed and verified.
- RapidAPI free-plan access has previously rate-limited the project. The connected mode therefore has strict hourly limits and preserves fixture mode as an explicit fallback; availability is not guaranteed.
- Storage is an in-memory SQLite demonstration store. It is not durable, multi-instance, or an audit system.
- Bank transaction context, payment execution, customer consent, operator production access, and hardware-bound device attestation are simulated or absent.
- Risk weights and scenarios are deterministic demonstration rules, not trained, calibrated, independently validated, or regulator-approved controls.
- SafePay does not implement or claim an active-call or Scam Signal API.

## Demo Recommendation

Begin with one routine fixture payment to prove the zero-call path. Then use protected connected mode for one SIM-takeover review so judges can watch Gemini choose context-eligible tools and Nokia return simulator evidence. If provider quota is unavailable, state it plainly, show the recorded connected capture, and continue with the explicit fixture fallback. Use the 36-case gate to demonstrate repeatability, not fraud accuracy.
