# Payment Fraud Investigation

Status: Draft interview specification. Not ready for implementation; unresolved decisions below are not approved defaults.

## Agreed purpose and setting

Demonstrate SafePay as an AI fraud-investigation agent for payment applications in Egypt, Saudi Arabia, and the UAE. Scope includes scam-induced transfers, SIM-swap/account takeover, and attempted use of compromised card details. The existing PRD identifies online checkout and wallet cash-in as card-use contexts; their exact Phase 2 implementation remains to be specified. InstaPay is one regional reference, not the exclusive target.

The simulator represents the relevant payment application's backend integration. Selecting one lead presentation scenario does not remove other fraud use cases from the product scope.

The agent must select relevant available CAMARA tools and interpret their observations. The demonstration must make its tool-selection behavior visible. Preset buttons may establish test situations, but must not stand in for agent tool selection.

The simulator represents a prospective integration with a payment app or participating institution. It does not establish access to actual InstaPay/IPN, Saudi sarie channels, UAE Aani channels, bank ledgers, or production operator data.

## Regional scope

| Market | Reference transfer experience | Currency |
|---|---|---|
| Egypt | InstaPay and participating IPN channels | EGP |
| Saudi Arabia | Banking/payment applications using sarie where supported | SAR |
| UAE | Aani application and participating institutions' Aani-enabled channels | AED |

Use a shared agent investigation workflow. Country and channel context must select applicable policy and the actual supported provider tools, rather than assuming identical rules or coverage everywhere. Exact authentication, limits, consent requirements, and capabilities remain to be established for each demonstrated integration.

The product scope includes all three markets. The precise number and order of demo cases remain open. Multi-country support does not automatically imply cross-border payments; that is a separate unresolved scope decision.

Reference sources: [EBC IPN](https://www.egyptianbanks.com/instant-payment-network/), [SAMA sarie](https://www.sama.gov.sa/en-us/payment/pages/Sarie.aspx), [Al Etihad Payments Aani](https://aep.ae/en/services/aani/).

## Workflow boundary

- Starting event: the simulated payment backend receives a pending transfer or card-payment attempt. A mandatory-event gate precedes local screening. First-time setup and new-device enrollment follow [customer trust establishment](customer-trust-establishment.md); a low pre-call score cannot waive their required checks. Local screening selects other payments requiring agent investigation.
- Investigation: the agent gathers relevant network evidence through permitted tools and uses the observations to determine its next action.
- Completion: an explicit investigation outcome is returned to the payment experience. Available outcomes, execution authority, and completion conditions remain open.

## Agreed fraud families

| Fraud family | Initiating situation | Investigation purpose |
|---|---|---|
| Scam-induced transfer | A legitimate customer is manipulated into paying a new recipient | Assess contextual scam evidence and determine a meaningful intervention despite potentially valid identity credentials |
| SIM-swap/account takeover | A payment attempt may be associated with unauthorized account access and a recent SIM change | Examine SIM-change evidence with independent session/account context; distinguish legitimate replacement from takeover |
| Misuse of leaked card details | Compromised credentials are used for an online purchase or wallet funding attempt | Assess the authenticated session's relationship to the bank-bound customer identity and other available risk evidence |

These families can overlap. The agent must investigate observations rather than assume that each payment belongs to exactly one preset category. API capabilities and supported authentication flows still require verification per provider and market. A number match alone does not prove card ownership; an unavailable verification flow alone does not prove fraud.

The card-use workflow does not claim to detect the original data leak or prevent merchant database compromise. Additional cases mentioned in the existing plan, including physical coercion and fake receipts, require separate scope and evidence decisions. Legitimate device replacement, roaming, and unsupported verification are also important comparison/failure cases rather than automatic fraud classifications.

## Agreed scam-transfer example

A legitimate customer is persuaded by someone impersonating a bank representative to transfer money to a new recipient. This is an agreed demo scenario across Egypt, Saudi Arabia, and the UAE, not the product's sole fraud use case. The customer may possess the genuine device and valid credentials; successful identity verification alone does not establish safe payment intent.

The simulator may define the scam as scenario ground truth for evaluation, but the investigator must obtain evidence through its permitted inputs and tools. Merely selecting a scam preset must not supply a hidden fraud verdict to the agent. Exact evidence and the legitimate comparison case remain to be specified.

## Decisions still to resolve

- Observable evidence and legitimate-customer comparisons for each agreed fraud family across the regional scope.
- Exact checkout, wallet-funding, and transfer trigger contracts; additional fraud cases required for Phase 2.
- Bank/app context available at the trigger, and who supplies authoritative values.
- Actual available CAMARA tools, authentication requirements, and source modes.
- Agent discretion, mandatory checks, and permitted payment actions.
- Behavior for missing, stale, contradictory, or unavailable evidence.
- Customer intervention, cancellation, recovery, and any human review.
- Latency and call budgets, audit evidence, and workflow acceptance scenarios.
- Prospective production buyer and integration boundary.

## Current interview question

What authority should the agent have to intervene in a pending payment across the agreed fraud families?

Recommendation awaiting the user's decision: allow the agent to invoke policy-permitted protective actions automatically, with different actions available for different channels. A transfer might enter a temporary hold or customer intervention; a checkout might require issuer authentication or receive a decline recommendation. Exact authority, channel support, release criteria, escalation, and cancellation remain open. No permission for unrestricted funds release or account freezing has been inferred.

## Upgrade requirements derived from the current application

These are proposed implementation requirements from the September 8 code inspection. They make the pending design concrete; they do not mark unresolved product decisions as accepted.

| Existing component | Observed behavior | Required upgrade |
|---|---|---|
| `app/core/models.py` | Transfer-only request; no explicit jurisdiction, payment channel, bank-bound customer reference, or evidence availability | Represent transfer, card checkout, and wallet funding contexts with explicit country/channel and authoritative synthetic customer/session references. Use token references for card fixtures, not real PAN/CVV data. |
| `app/services/ai_agent.py` | Generates prose after scoring; no tool calling | Implement bounded model-selected tool execution, observations, follow-up choices, and a structured disposition linked to evidence. Keep optional narration independent. |
| `app/services/telecom_gateway.py` | Presets bypass provider requests; missing evidence becomes clean; telemetry is constructed | Expose individually callable provider tools with validated contracts, explicit availability/source/freshness, measured execution traces, and declared simulation adapters. Never silently substitute fixture evidence for failed live requests. |
| `app/core/risk_engine.py` | Static score mixes risk, routing limits, and legal claims | Enforce permitted actions and mandatory evidence independently of the model; configure jurisdiction/channel policy; preserve unknown states and remove unverified compliance conclusions. |
| `app/main.py` | Awaits narrative generation; biometric resolution trusts client success; no transaction state lookup | Orchestrate a stored investigation lifecycle, validate transitions, support cancellation and review, bind challenges to payment intent, reject replay, and publish correlated events. |
| `app/services/audit_store.py` and `app/config.py` | In-memory fallback; Supabase configuration fields absent | Provide durable local transaction/evidence history for the demo and correctly wire any optional Supabase deployment. Local persistence should not require a new cloud account. |
| `app/static/js/app.js` and `app/static/index.html` | Shared transfer form for all scenarios; hardcoded Saudi sender; scenario determines purported tool selection | Separate country selection from fraud scenarios; render appropriate transfer/checkout/funding journeys and show tool selection, evidence, limitations, and payment states. Preserve reusable dashboard/WebSocket components. |
| `tests/test_risk_engine.py` | Four preset scoring checks and one local performance check | Add workflow tests for each fraud family across country profiles, legitimate lookalikes, provider/model outages, missing evidence, cancellation, replay, and evidence-driven tool execution. |

### Proposed runtime contract

1. The backend accepts and stores a pending payment intent with country, channel, and customer/session context.
2. A mandatory-event gate checks server-held enrollment/device-trust state. Unresolved first-time setup or new-device registration cannot take the routine-payment fast path. Otherwise local screening evaluates bank/app context and applicable requirements. Eligible routine payments continue through normal payment authorization without optional CAMARA or LLM calls. Missing context is not a clean result.
3. For selected payments, the investigator sees redacted observable facts, local screening reasons, and permitted tool schemas, not the fixture's hidden fraud label or a precomputed fraud verdict.
4. The model selects a tool; a controlled executor checks capability, arguments, deadline, and call budget before executing it.
5. The returned observation is recorded with provenance. The agent decides whether another tool is needed or proposes a disposition.
6. The policy layer validates the proposed action and required evidence. The simulator executes only permitted state transitions and streams them to the UI.
7. Optional explanation generation for investigated cases follows the authoritative transition; it cannot rewrite the outcome or claim unsupported observations. Routine payments can receive deterministic local explanations without a model call.

Presets must not reveal fraud through synthetic payee names such as `Unknown Payee (Scammer)` in the agent's input. Ground truth belongs to the test harness. A combined SIM-swap and card-misuse case should be representable rather than forced into a single exclusive enum.

### Local pre-call screening and final risk assessment

User requirement: preserve a smooth payment experience and control cost through selective external checks. The local screening stage is distinct from the risk assessment updated after tool observations.

Current code gap: `app/main.py` invokes the telecom gateway before `DeterministicRiskEngine.evaluate`. The current score therefore cannot decide whether that gateway should be called. Beneficiary trust only contributes inside the active-call branch, and historical behavior/velocity are not implemented.

Proposed pre-call inputs, supplied by trusted simulated bank/app records rather than self-asserted production client fields:

- Established session authentication and known-device continuity.
- Beneficiary or merchant relationship and recency of addition.
- Amount relative to customer history, with a defined insufficient-history state.
- Recent payment attempts, aggregate value, failed authentication, and account-recovery events.
- Country/channel policy and any cached evidence that is valid for this context.

Pre-call processing must not claim knowledge of current SIM changes, bearer identity, roaming, or voice-call state unless valid evidence is already available. Fresh bank session information is not a substitute for a carrier Device Swap result; retain source distinctions.

Proposed routing:

| Local screening result | Next step |
|---|---|
| First-time setup or new-device enrollment is incomplete | Complete mandatory fresh verification through the trust-establishment workflow; neither a low score nor an old clean cache can waive it |
| Routine context and required authentication/evidence satisfied | Continue normal payment authorization, zero optional CAMARA calls and zero LLM calls |
| Anomaly or insufficient evidence requiring investigation | Invoke the agent with relevant context, capabilities, and budgets |
| Existing policy prohibition or known compromise | Enforce the applicable pending-payment restriction; do not spend on queries that cannot change the permitted action |

`pre_call_score` expresses local screening risk. `final_risk_score` expresses the assessment using the evidence actually available at completion. These are explainable heuristic scores until calibrated, not probabilities of fraud. Numeric weights and thresholds must be configured and validated against scenario outcomes, not presented as measured detection accuracy.

Do not simply sum two scores or count the same fact twice. A SIM change must not manufacture Number Verification failure and Device Swap failure. Preserve contributing factors, evidence coverage, missing observations, and decision source. Skipped tools stay `SKIPPED`; unsupported tools and failures stay explicit; a score of zero does not establish perfect safety.

Fast-path eligibility must not rely on a low amount or saved beneficiary alone. Cache reuse requires a matching subject, scope/window, source, freshness policy, and relevant session/context constraints. New account recovery, changed devices, or stale observations may invalidate eligibility; no universal 15-minute clean-result reuse is approved.

UX acceptance: no visible challenge on an eligible routine payment beyond the host application's normal authentication. Investigated payments show a concise pending status and any necessary intervention. Technical scores and tool traces belong to the SOC view. Measure extra latency, challenge frequency, completion/cancellation, calls per evaluated payment, and fraud cases missed by screening relative to a full-evidence test baseline. Lower call volume alone is not success.

### Reconciliation with existing project documents

The latest user decisions take precedence over conflicting older design descriptions. These are implementation intentions, not evidence that the current app implements them.

| Source | Existing description | Resolution for this workflow |
|---|---|---|
| `MENTOR_MEETING_READINESS_CHECKLIST.md`, Pillar 3 | Hardware-bound trust, 85% routine approvals, 95% zero-call strategy | Preserve established-device trust as a proposed fast-path input. Treat percentages as unmeasured targets. The browser simulator must not claim native Secure Enclave/Keystore attestation. |
| Readiness checklist versus `SAFEPAY_DEEP_ASSESSMENT_AND_IMPROVEMENTS.md` | Three-minute versus 15-minute SIM-status cache | No universal duration is agreed. Specify per-signal freshness and context invalidation; mandatory fresh checks cannot reuse old clean observations. |
| Readiness checklist | Transfers above EGP 5,000 force a live check | An earlier proposed policy threshold, not a verified legal rule or a threshold transferable to SAR/AED. Exact market/channel thresholds remain to be tested and settled. |
| `SafePay_MENA_Idea_Capture_Template.md` versus `PRD.md` | Agent-selected tools versus an AI audit narrator | User explicitly requires genuine tool selection. Proposed architecture: bounded agent investigation plus deterministic enforcement of mandatory checks and permitted actions. Narration is secondary. |
| `SAFEPAY_SECURITY_THREAT_MODEL_AND_TRACES.md` | Micro-transfers, delayed attacks, prompt injection, provider outages | Include adversarial and resilience tests alongside fraud-family demos. Small amounts and old SIM changes alone cannot establish safety. Do not claim all threats are solved. |
| Mentor debrief and Phase 2 dossier | Biometric completion resolves a scam/coercion warning | Authentication does not establish uncoerced intent. A scam intervention needs independent release conditions; client-reported biometric success cannot clear a hold. |

The locally authored Phase 2 dossier is pitch material, not independent verification of judging weights, production readiness, regulatory mandates, live integrations, or performance. Claims must be reconciled with the code inspection and primary sources before presentation.

### Build inputs and working assumptions

- Use September 10 and a three-minute recording as working planning assumptions from `SAFEPAY_MASTER_PROJECT_PLAN.md`, Phase E. The same plan also says three to five minutes elsewhere; neither establishes the official live-presentation allocation. Check organizer instructions before submission rather than asking the user to repeat the project plan.
- Working model access configured locally. The current settings inspection found no Gemini key. Model selection and availability can be verified during implementation.
- User confirmed Nokia access is key only. Discover documented sandbox identities, enabled products, and application/consent requirements from provider documentation and the account before requesting specific missing setup from the user. A key's presence does not verify entitlement or successful supported calls. The standalone Nokia probe does not establish payment-path integration. Never print credentials or test arbitrary real customer numbers.
- Desired demo execution authority: whether model-selected, policy-validated approve/challenge/hold/decline actions should automatically change the simulated payment state. Exact high-risk release/review conditions remain to be resolved.

Engineering details such as file organization, local persistence, event correlation, and test fixtures can be proposed from the existing application rather than delegated to the user. Foundational implementation and explicit simulation do not depend on production bank access or contracted supplier prices; claims of live integration do depend on verified provider access.

### Reinspection evidence

The existing four scenario checks plus the performance check passed under the installed Python 3.14 interpreter; 1,000 in-memory evaluations took 2.78 ms in this run. This does not validate network availability or complete workflows. Configuration presence was checked without printing credential values: Nokia configured, Gemini absent, Supabase environment values absent, and Supabase fields absent from Settings. Application code was read but not changed during this specification turn.

## Context

- [Interview notes](../NOTES.md)
- [Phase 2 review](../docs_and_presentations/PHASE2_DEEP_REVIEW.md)
- [Mentor debrief](../MENTOR_MEETING_DEBRIEF_AND_DECISIONS.md)
