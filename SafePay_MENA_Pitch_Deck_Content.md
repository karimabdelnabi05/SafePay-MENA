# SafePay MENA - Phase 2 Pitch Deck

This is the source narrative for the 10-slide working-prototype deck. Claims describe implemented behavior or explicitly labeled external context. The prototype does not execute payments or contact production mobile networks.

## 1. SafePay MENA

**Offer:** Adaptive telecom evidence before instant payments move.

Routine payments stay on a zero-call path. Elevated-risk payments trigger a bounded Gemini agent that selects relevant CAMARA tools. A deterministic policy owns the final release decision.

## 2. One Decision Point, Multiple Fraud Paths

- Coerced transfer: identity may verify while payment intent remains unsafe.
- SIM takeover: an unusual session combined with recent SIM/device changes can justify a protective block.
- Card leakage: a checkout may fail number verification and show independent device anomalies.
- First setup: a new installation must establish fresh number and SIM evidence before becoming trusted.

No single telecom signal is presented as proof of fraud.

## 3. Evidence Only When Context Earns It

1. Local pre-screen evaluates amount, recipient relationship, session anomaly, customer-reported transfer request, travel context, and velocity.
2. Routine context can approve with zero Gemini and zero telecom calls.
3. Elevated context invokes the agent and only the tools it selects.
4. Policy returns APPROVE, HOLD, BLOCK, RETRY, or VERIFY_DEVICE.

## 4. Agentic Orchestration With Boundaries

The model receives observable payment facts, not scenario labels. It chooses one tool at a time and may use at most five evidence calls. Repeated, unsupported, malformed, or over-budget requests fail closed.

The Nokia adapter restricts tools, endpoints, redirects, and simulator subjects. Provider failures become UNKNOWN. Policy validates the final disposition and never weakens a protective BLOCK.

## 5. Verified Open Gateway Integration

Verified against Nokia Network as Code sandbox on 8 September 2026:

| Capability | Implemented role |
|---|---|
| SIM Swap | Recent SIM-change evidence within a requested window |
| Number Verification | OAuth-bound number match |
| Device Swap | Independent network device-change evidence |
| Roaming | Travel context, never fraud by itself |
| Reachability | Targeted supporting evidence, never fraud by itself |

The prototype does not claim an active-call API. It does not claim production operator availability.

## 6. Working Demo

The interface guides judges through market, evidence mode, scenario, amount, and recipient relationship. The result leads with the decision and reason. Network evidence and the agent/policy trace remain collapsed until requested.

Demo sequence:

1. Everyday payment: APPROVE, pre-call score 0, agent/API calls 0.
2. First setup: mandatory enrollment, then continue to payment in the same session.
3. Suspicious transfer: HOLD despite clean identity evidence because verification does not prove safe intent.
4. SIM takeover: protective BLOCK from combined evidence.
5. Nokia sandbox: show live adapter evidence with explicit simulator provenance.
6. Acceptance evaluation: 36 synthetic cases across three markets.

## 7. Three Market Contexts

- Egypt: InstaPay / IPN context.
- Saudi Arabia: sarie context.
- United Arab Emirates: Aani context.

The same decision interface can be configured per rail and jurisdiction. The demo localizes currency and rail context; it does not claim regulatory certification or live operator coverage.

## 8. Quality Assurance

The in-product evaluation runs 12 scenarios in Egypt, Saudi Arabia, and the UAE: 36 expected outcomes.

Additional automated checks cover provider failures, malformed OAuth and model responses, tool-budget exhaustion, idempotency, session isolation and expiry, cancellation, enrollment, velocity, policy override, model-markup safety, mobile layout, and zero-call routine behavior.

These are software acceptance tests, not real-world fraud-detection accuracy.

## 9. Commercial Path

**Buyer:** banks, wallets, payment providers, and fraud platforms.

**Model hypothesis:** platform subscription plus metered orchestrated checks, with carrier and model costs shown explicitly.

**Pilot scorecard:** fraud loss, false positives, abandonment, availability, latency, and cost per reviewed transaction. Pricing and ROI remain hypotheses until measured with a bank/operator pilot.

## 10. The Ask

1. Confirm target-country operator/API coverage for SIM Swap and Number Verification.
2. Connect a non-production bank release workflow and agree fallback actions.
3. Run a measured pilot with safety, friction, reliability, latency, and unit-economics baselines.

Primary references:

- CAMARA Number Verification: https://github.com/camaraproject/NumberVerification
- CAMARA SIM Swap: https://github.com/camaraproject/SimSwap
- Nokia Network as Code: https://networkascode.nokia.io/
- SAMA sarie: https://www.sama.gov.sa/en-us/payment/pages/Sarie.aspx
- CBUAE retail payment rules: https://rulebook.centralbank.ae/

## Demo Disclaimer

SafePay MENA is a working hackathon prototype. Bank context is synthetic. Nokia evidence comes from documented sandbox simulator subjects. No production subscriber or payment rail is connected.
