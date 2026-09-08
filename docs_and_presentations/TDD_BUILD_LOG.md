# SafePay Phase 2 Build and QA

The user confirmed these public test boundaries on September 8, 2026:

1. SafePay HTTP API: enrollment, device changes, payment decisions and recovery.
2. Nokia adapter public API: provider evidence, authorization, failures and freshness.
3. Browser UI: complete desktop/mobile tester journeys.

Work proceeds one failing behavior test, minimal implementation, then verification at a time. External HTTP services may be replaced with controlled transports; internal collaborators are not mocked. An independent QA agent reviews security, behavior, and UI risks. A deterministic evaluation runner will report scenario outcomes separately from optional model-assisted evaluations.

Demo decisions: no real funds, account-wide freeze, real subscriber queries, or production compliance certification. Routine eligible payments make zero optional external calls. Enrollment requires fresh verification. Unknown evidence prevents automatic release. Gemini selects tools within a bounded executor; deterministic rules enforce minimum safety requirements. Explicit fixture mode is not a silent fallback for live failures.

Deployment must keep provider keys server-side, cap public API usage, and restrict all subjects to simulated identities. Stable hosting credentials may require an external account; do not claim a temporary preview is durable production hosting.

## Completed Red-Green Slices

- Routine payment approves with separate pre-call/final scores and zero external calls.
- First setup and new device require fresh enrollment before payment.
- Provider failures and malformed OAuth/model responses become UNKNOWN or RETRY.
- Fraud scenarios produce expected APPROVE/HOLD/BLOCK/RETRY outcomes across EG, SA and AE.
- Request IDs are idempotent and conflicting intents are rejected.
- Held runs can be cancelled; client-claimed biometric success cannot release funds.
- Gemini selects bounded tools while deterministic policy prevents unsafe approval.
- A Gemini BLOCK cannot be weakened, and tool-budget exhaustion fails closed.
- Agent input includes amount, relationship, country, channel and pre-screen reasons, never scenario labels.
- Nokia evidence records its approved simulator subject and never exposes credentials.
- Sessions are isolated and expire after one hour.
- Browser acceptance covers desktop/mobile routine approval, zero calls, hidden invalid actions, enrollment-to-payment continuation, and literal rendering of model-supplied markup.
- The in-product evaluation reports 36/36 synthetic acceptance cases and labels its scope accurately.
