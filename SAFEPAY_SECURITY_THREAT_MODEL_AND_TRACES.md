# SafePay MENA Security Model

This document describes controls implemented by the Phase 2 prototype. It does not claim production certification, fraud-model accuracy, or regulatory compliance.

## Trust Boundaries

1. The browser submits synthetic payment context to the SafePay FastAPI service.
2. Local screening decides whether the request needs external evidence.
3. In explicitly enabled live mode, Gemini can select only declared CAMARA tools.
4. The Nokia adapter selects fixed simulator subjects and fixed endpoint paths.
5. Deterministic policy evaluates returned observations and owns the final disposition.

No payment rail, production bank, production operator, or real subscriber is connected.

## Implemented Controls

| Risk | Implemented control |
|---|---|
| Unnecessary API use | Routine payments remain on a zero-external-call path. |
| First-install bypass | First setup and new-device sessions require fresh Number Verification and SIM Swap observations before device trust is established. |
| Model tool abuse | Tool names and schemas are allowlisted; repeated, malformed, or unsupported calls stop the investigation. |
| Model-controlled routing | Phone subjects, hosts, URLs, and endpoint paths are selected outside the model. |
| Model-controlled release | Gemini proposals cannot weaken a deterministic block or directly create one. It can request additional review. |
| Missing provider evidence | Timeouts, non-boolean responses, authorization errors, and rate limits become `UNKNOWN`; required unknown evidence produces `RETRY`. |
| OAuth redirect abuse | Number Verification uses fresh state and nonce values, validates callback state, limits redirects, and allowlists Nokia HTTPS hosts. |
| Scenario leakage | The scenario identifier is not included in Gemini context. The model receives observable transaction and risk context only. |
| Duplicate submission | A request ID is idempotent inside a session; reuse for a different payload returns HTTP 409. |
| Cross-session access | Runs are keyed by the random HTTP-only session cookie and are unavailable from another session. |
| Browser injection | Dynamic reasons, evidence, and trace values are HTML-escaped before insertion. |
| Public key spending | Live mode is disabled by default and requires `SAFEPAY_ENABLE_LIVE=true` plus both provider keys. |

## Decision Trace

Each completed result records the fields the UI and quality gate use:

```json
{
  "id": "payment-identifier",
  "decision": "APPROVE | HOLD | BLOCK | RETRY",
  "decision_source": "LOCAL_SCREENING | DETERMINISTIC_FIXTURE | GEMINI_WITH_POLICY | POLICY_FAIL_CLOSED",
  "pre_call_score": 45,
  "final_risk_score": 55,
  "telecom_calls": 2,
  "model_calls": 3,
  "evidence": [
    {
      "tool": "sim_swap",
      "source": "NOKIA_SANDBOX",
      "status": "SUCCESS | UNKNOWN",
      "data": {"swapped": false},
      "http_status": 200,
      "endpoint": "/passthrough/camara/v1/sim-swap/sim-swap/v0/check"
    }
  ],
  "agent_trace": [
    {
      "actor": "GEMINI",
      "tool": "sim_swap",
      "reason": "Check recent SIM state",
      "status": "SUCCESS"
    }
  ]
}
```

Provider keys, OAuth client secrets, authorization codes, and response bodies from failed requests are not stored in evidence.

## Known Prototype Limits

- SQLite state is in memory by default. It is not durable, shared across instances, or an immutable audit ledger.
- Fixture deployments are anonymous and suitable only for demonstration traffic.
- Enabling live mode on a public service would require authentication, quotas, concurrency controls, monitoring, and a persistent datastore.
- Nokia simulator subjects encode predetermined results and do not represent coherent real customers.
- Number Verification establishes a number association, not payment intent, card ownership, or freedom from coercion.
- Device Swap reports a network-observed change; it does not prove the app's registered-device identity.
- Roaming and reachability are context, not proof of fraud.
- SafePay does not implement an active-call or Scam Signal API.
- Policy scores are explainable demonstration heuristics, not calibrated fraud probabilities.

## Deployment Boundary

The public judging deployment must remain fixture-only:

```text
SAFEPAY_ENABLE_LIVE=false
SAFEPAY_DATABASE=:memory:
```

Live Nokia and Gemini checks should run locally with documented simulator subjects and controlled API quotas.
