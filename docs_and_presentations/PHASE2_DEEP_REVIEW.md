# SafePay MENA: Phase 2 Plan, Mentor Feedback, and Prototype Review

Reviewed September 8, 2026. Verdict: the project has a usable simulation foundation and a relevant problem, but the current pitch materially overstates what the implementation proves. The highest-return work is real evidence, safe failure handling, and a visible agent tool workflow. Another feature or more polished claims will not close those gaps.

This is a review, not an implementation change. Application files were not edited by the reviewer. Findings reflect inspected working files and local probes; `app/main.py` gained a separate Nokia probe endpoint concurrently during the review. That addition was inspected and does not change the payment-path findings below.

## 1. Findings That Could Cost the Most Points

### P0: The demo presents constructed telecom evidence as live integration

Evidence: [telecom_gateway.py](../app/services/telecom_gateway.py), especially `_build_wire_trace`, `_resolve_signals`, and `_query_nokia_rapidapi_sim_swap`; [app.js](../app/static/js/app.js), `executeTransfer`.

All four scenario branches return fixtures before the live provider path. The frontend always sends a scenario parameter. Consequently, changing an API key does not make those demonstration transactions live carrier queries. The inspector constructs response headers, carrier-node identifiers, timestamps, successful statuses, and latencies; its default mode is `RAPIDAPI_CAMARA_GATEWAY` even for fixtures.

The only payment-path external telecom request implemented is SIM Swap. Number Verification, Device Swap, call status, and roaming are preset or derived values. On the ordinary path, `number_verified` and `device_match` are inferred from the SIM Swap result, which does not measure either property. A no-swap result cannot establish device possession or hardware continuity.

Controlled verification: all four presets made zero additional provider calls. A cold-cache ordinary evaluation invoked the SIM Swap adapter once while reporting Number Verification as invoked and SIM Swap as cached. The telemetry therefore cannot substantiate the claimed adaptive orchestration or 75% measured cost reduction.

Required correction: distinguish `LIVE_SANDBOX`, `RECORDED`, `SIMULATED`, `CACHED`, `UNAVAILABLE`, and `SKIPPED` at signal level. Generate wire records and billable-call counters from executed adapter calls. Show provider-returned data and measured times. A separate connectivity probe is useful diagnostics, but only an actual result consumed by the decision demonstrates integration. A gateway response or HTTP 403 is not a successful CAMARA transaction.

### P0: Carrier uncertainty becomes positive authentication

Evidence: [telecom_gateway.py](../app/services/telecom_gateway.py), `evaluate_carrier_signals` timeout handler and `_resolve_signals` failure fallback.

The timeout handler sets number verification and device match to true, and SIM swap, roaming, and active call to false. A local timeout probe produced `APPROVE` and a CBUAE-compliant flag. Other provider failures silently switch to phone-suffix simulation and may cache that fabricated result.

This contradicts both the product's security purpose and the earlier assessment's proposed fallback to a challenge. Unknown is not clean. A recent SIM change can also occur during a cached clean result's 15-minute lifetime; increasing that lifetime to protect margins increases the unobserved interval.

Required correction: preserve unknown/error states, source, observation time, and expiry. Apply an explicit bank policy for unavailable evidence, normally hold or independent authentication for the selected high-risk flow. Keep simulation an explicit demo mode. Do not infer a successful Number Verification result from a cache, SIM Swap response, or outage. The existing timeout is not a complete circuit breaker with open/half-open recovery state.

### P0: The current AI does not perform the orchestration the rubric asks for

Evidence: [ai_agent.py](../app/services/ai_agent.py), `generate_compliance_trace`; [telecom_gateway.py](../app/services/telecom_gateway.py), `_resolve_signals`; [official resource guide](GSMA%20MENA%20Resource%20Guidea254feb.pdf), section 11.

The official guide says: "Treat each CAMARA API as a tool the agent decides when to call, not a button the user presses." Current Gemini use is a text-generation request after deterministic scoring. There is no model tool selection, observation loop, or action execution. The gateway does not even receive the amount, beneficiary history, or transaction context that the advertised adaptive routing supposedly uses.

Presets are useful for selecting synthetic customer situations. They should not select the alleged agent's tool plan. Likewise, changing a rule's branch is not evidence that Gemini orchestrated the APIs.

Required correction: implement one bounded investigation workflow with real tool execution, capability checks, a deadline, and a maximum call budget. The agent can decide which permitted missing signal to obtain; deterministic policy remains responsible for final financial disposition. Demonstrate two transactions producing different tool choices because their context or observations differ. The user's rubric allows one or more CAMARA APIs, so one demonstrated integration in a real agent workflow is preferable to unsupported breadth.

There is a separate model-readiness risk: code hardcodes `gemini-2.0-flash`. Google's current lifecycle table lists June 1, 2026 as its shutdown date, with a note that listed dates are earliest possible retirement dates. Do not assume this model works in September. Select and smoke-test a supported model, configure its identifier, and expose model failure/template fallback in telemetry. No authenticated model request was made during this review. [Google model lifecycle](https://ai.google.dev/gemini-api/docs/deprecations)

### P0: Face ID does not establish freedom from coercion, and the endpoint verifies no credential

Evidence: [main.py](../app/main.py), `verify_step_up`; [app.js](../app/static/js/app.js), `confirmBiometricStepUp` and `cancelTransfer`.

A fabricated token and a transaction ID that was never evaluated returned HTTP 200 and `APPROVED_POST_BIOMETRIC`. The endpoint only tests client-supplied `success`; there is no challenge, signature validation, pending transaction lookup, expiry, or replay protection. Cancellation merely hides the modal and displays a message. No payment state is cancelled on the server.

Even a correctly implemented biometric check would prove authentication, not that the legitimate customer is free from manipulation or physical duress. The scammer can instruct the actual victim to pass Face ID. Number Verification has the same limitation concerning payment intent.

Required correction: call the current control a simulated challenge. Bind any real authentication result to the immutable transaction and an expiring, single-use server challenge. For the vishing story, demonstrate a warning plus cancellation, delayed review, or another bank-defined intervention; do not demonstrate Face ID automatically releasing a still-suspicious payment as proof that the scam was defeated. Avoid claiming account freeze or actual settlement, because this prototype has no connected bank ledger.

### P1: AI generation is on the payment response path despite the stated architecture

Evidence: [main.py](../app/main.py), `evaluate_transaction`, and [ai_agent.py](../app/services/ai_agent.py), `run_in_executor` call.

`evaluate_transaction` awaits `generate_compliance_trace` before returning. Moving the synchronous SDK request to a worker thread frees the event loop but does not let this HTTP request finish. A controlled 100 ms AI delay caused an approximately 115 ms response. This proves the dependency; it is not a live model-latency measurement. There is no explicit application deadline around generation.

Required correction: return the authoritative risk outcome before optional narrative generation, then publish the explanation separately. If the agent investigates an uncertain transaction, show that as a distinct pending flow with a realistic deadline. Measure API acquisition, decision computation, end-to-end response, and later explanation latency separately. The local scoring benchmark is not national payment throughput, and the wire inspector's fixed numbers are not measured network medians.

### P1: The pitch relies on unsupported legal, fraud, and originality claims

Evidence: [pitch content](../SafePay_MENA_Pitch_Deck_Content.md), slides 3, 4, 7, 9, 11, 12, 13; [claim verification](PHASE2_CLAIM_VERIFICATION.md).

Remove or qualify: "85% of MENA losses", "world-first", "zero liability", "court-admissible", "zero PII", "100% enforced", and universal replacement of 3DS/SMS authentication. Phone numbers and linkable identifiers are still personal data. The AI prompt also includes sender phone and recipient identifiers; the wider data flow is not covered by saying bank balances are not sent to telcos.

The original UAE Notice 3057 was not located. That does not prove it is fictitious. It means its exact scope must not be inferred from secondary summaries, and a generated citation cannot certify compliance. The deck repeatedly treats March 31, 2026 as a future deadline despite the September review date. UAE compliance flags are also applied to clean Saudi and Egyptian transactions without jurisdiction selection.

The 44% scam-loss and 55% false-positive reductions have an identifiable FICO/JT UK-pilot source, but they are not SafePay outcomes. That existing solution already uses telecom signals and contextual customer interventions, weakening the current competitor table and "first" claim. Cite it as evidence for the category and articulate a narrower product difference. [FICO/JT announcement](https://investors.fico.com/news-releases/news-release-details/fico-and-jersey-telecom-collaborate-tackle-authorised-push/)

### P1: Commercial arithmetic and pricing units do not agree

Evidence: [pitch content](../SafePay_MENA_Pitch_Deck_Content.md), slide 10; [financial plan](../SAFEPAY_FINANCIAL_AND_UNIT_ECONOMICS_DEEP_DIVE.md), sections 3, 5, and 7.

- Five million transactions/month at $0.20/evaluation costs $12M/year if every transaction is evaluated. The slide's $1.2M/year requires 500,000 evaluations/month, or 10% selection.
- $8.5M fraud savings plus $1.8M SMS savings against $1.2M fees implies 758.3% net ROI, not 693%. Excluding SMS yields 608.3%.
- The older 693.75% model is arithmetically correct for its different assumptions: $63,500 monthly gross savings and $8,000 fees. It cannot be transferred to the new slide's inputs.
- Two prevented $4,000 fraud cases cover the older model's monthly $8,000 contract, not its $96,000 annual contract.
- The documents alternate between $0.01/carrier call, $0.03/carrier call, $0.07/query or bundle, and $0.025-$0.20/billable check. Actual negotiated quotes are not demonstrated.

Required correction: define a transaction, selected evaluation, carrier call, cached lookup, and billable bundle. Use one model throughout the deck, with explicit assumptions and a range of supplier prices. Savings from eliminating SMS apply only where an SMS was actually replaced; the materials already recognize that routine InstaPay transfers use a PIN.

### P1: Audit and production claims exceed the implementation

Evidence: [audit_store.py](../app/services/audit_store.py), [migration.sql](../app/database/migration.sql), and [app.js](../app/static/js/app.js), `renderBankRailPayload`.

There is a useful audit record structure and a Supabase REST adapter. There is no decision hash, signature, cryptographic timestamp, external integrity anchor, or proven immutable storage. Settings do not declare `SUPABASE_URL` or `SUPABASE_KEY`; the store obtains them via `getattr(settings, ..., "")`, so ordinary environment configuration does not populate the documented persistence path. In-memory records disappear on process exit, and fire-and-forget persistence does not guarantee delivery.

The migration gives all authenticated users unrestricted table-wide SELECT and INSERT policies; it does not distinguish auditors, tenants, and backend identities. This is not sufficient for the claimed enterprise audit boundary. The browser's ISO-inspired JSON has no demonstrated schema validation or bank submission; it is an illustrative payload, not proof of a working `pacs.008` integration.

Required correction: present the system as a prototype. For hackathon evidence, a durable local append-only event history with transaction transitions and policy versions is sufficient if honestly described. Production deployment needs authenticated bank clients, authorization boundaries, idempotency, delivery guarantees, retention controls, and validated partner integration.

## 2. Assessment Against the Six Criteria

These are evidence-readiness judgments, not predicted judge scores. The user supplied no official percentage weights; the dossier's 20/20/15/15/15/15 split has no established authority in the reviewed guidance.

| Criterion | What is already useful | Current weakness | Best next proof |
|---|---|---|---|
| Innovation and originality | Combining payment context and telecom signals is relevant | Existing vendors already operate here; regional branding and a weighted score are not a moat | Show constrained, cost-aware investigation with explicit evidence freshness and regional integration policies |
| Impact | Recognizable customer harm and understandable interventions | No own efficacy data; ATO, APP coercion, card fraud, and physical duress are conflated | Select one attack mechanism; compare decisions with and without the network signal, including legitimate lookalikes |
| Scalability and commercial viability | A bank-facing API and usage-based model are plausible | Buyer scope is too broad, coverage unproven, pricing inconsistent | One design-partner profile, one provider capability matrix, and a coherent selection-rate model |
| Technical feasibility and API use | FastAPI, schemas, deterministic engine, working fixtures, WebSocket code | Preset bypass, fabricated wire records, unsafe fallback, and unverified authentication | One real provider response driving a decision plus a transparent outage demonstration |
| Agentic AI and orchestration | Existing AI adapter and signal interfaces provide starting points | Narrative generation is the only model behavior; no tool loop | Model selects and executes an allowed CAMARA tool, observes it, then stops under enforced policy |
| Presentation and pitch | Concrete scenarios and a business-value narrative | Fifteen slides, repeated absolutes, mixed jurisdictions, and stale numbers | Short pitch, one main market, three outcomes, and a technical appendix with honest evidence |

The greatest current judging risk is technical credibility and agentic behavior. The opportunity is to make the visible experience match the actual execution and narrow the commercial promise to something testable.

## 3. What the Mentor Meeting Should Change

Source: [September 7 debrief](../MENTOR_MEETING_DEBRIEF_AND_DECISIONS.md). This is a summary, not a transcript or recording. The review cannot establish exact words, omitted qualifications, or whether a statement was the mentor's view versus a later interpretation. "stc mentorship completed" is supported by the team's record; "validated by stc leadership" or commercial endorsement is not established by it.

| Recorded mentor feedback | Assessment | Concrete decision |
|---|---|---|
| Judges include business, IT, cybersecurity, and fintech perspectives | Keep | Lead with customer harm and intervention; reserve exact protocols and controls for an appendix |
| Numbers communicate value | Keep, with evidence discipline | Use one primary-source market fact, one measured prototype result, and one clearly labeled pilot assumption |
| OTP theft and vishing deserve attention | Keep the distinction between fraud mechanisms | Number Verification addresses number association/possession; it does not stop a deceived legitimate payer from authorizing a transfer |
| eSIM, dual-SIM, and legitimate SIM issuance matter | High-value edge-case guidance | Add a legitimate replacement and unsupported-session scenario; never equate all SIM changes with proven fraud |
| Banks, wallets, and national switches are distinct customers | Treat as segmentation, not simultaneous launch scope | Choose a digital bank or wallet as the first buyer; a bank-channel integration has access to session and beneficiary context |
| Approve, challenge, and block should be clear | Keep | Implement server-side transaction states; do not make challenge success synonymous with fraud resolved |
| One to two seconds may be acceptable for flagged cases | Use as a design hypothesis, not universal regulatory SLA | Preserve a fast deterministic clean flow and allow a visibly pending investigation with a bounded budget |
| SAR 20,000 changes the relevant transfer pathway | Separate routing and fraud policy | Current SAMA sarie guidance includes amounts equal to SAR 20,000; exceeding a rail limit is not an automatic fraud determination |
| Fake receipts and physical coercion are possible future problems | Defer | They require additional evidence and controls beyond the demonstrated network signals |

The strongest mentor-driven change is a more precise user journey, not a broader list of threats claimed solved. The original pre-mentor plan has four tiers, different APIs, different prices, and a different role for AI; the later PRD and deck do not consistently supersede it. Select one current specification and mark older assessments as historical.

Unresolved questions from the debrief include the exact available operator/API combinations, subscription and consent flow, allowable data fields, real p95 latency, and wholesale pricing. These are dependencies, not validated facts. The [official mentorship guide](GSMA_MENA_Ignite_Hackathon_Mentorship_Guide.pdf) permits one session and explicitly rules out follow-ups or a second session. Resolve evidence through official documentation, the provider's ordinary support, or an existing bank contact rather than assuming another mentor review. September 10 is stated as the mentorship deadline; the reviewed official guide does not establish it as the final submission deadline.

## 4. Recommended Product Focus

Suggested positioning:

> SafePay MENA helps digital banks investigate risky transfers before releasing funds, combining payment context with Open Gateway network signals and a bounded AI workflow.

Start with one Saudi digital-bank or wallet journey: a transfer to a newly added beneficiary. Treat the provider and bank as prospective partners until access is actually granted. This is a product-focus recommendation, not evidence of a commercial commitment.

The first customer is the bank or wallet controlling authentication and payment initiation. The fraud/risk lead owns the problem, the engineering team integrates it, and the end user receives the intervention. National switches are a later expansion: the current browser experience and session-level authentication require context a switch-only integration does not automatically possess.

Choose the main attack demonstration according to actual API access. SIM Swap is the only currently wired provider call, so takeover screening is the most direct first integration proof. If a documented Scam Signal sandbox becomes available, make APP investigation a supported extension. Keep the mentor's social-engineering insight in the product direction without asserting live call detection before it exists. CNP checkout, nationwide routing, physical-duress protection, and fake-receipt detection should remain secondary or future scope.

### A minimal agent workflow worth showing

1. The bank submits an authenticated transaction intent with beneficiary trust and channel context. The server stores an immutable transaction identifier and initial state.
2. Deterministic policy checks mandatory requirements and identifies missing evidence. It never treats skipped, unavailable, or expired checks as successful authentication.
3. For uncertain transactions, the agent receives a redacted case and the actual available tools. It selects a permitted signal query and explains its purpose in a short action summary.
4. The adapter executes the call. The observation includes the provider, version, source mode, measured time, freshness, and exact supported fields.
5. The agent may request an additional allowed check or recommend review, within a fixed call budget and deadline. It cannot bypass mandatory checks, alter thresholds, or release funds.
6. Deterministic policy produces approve, challenge, or block/hold. Optional narrative generation follows; the structured evidence remains authoritative.

Display tool name, reason for selection, observed result, and policy outcome. There is no need to present hidden chain-of-thought. With Gemini unavailable, disclose fallback and apply the deterministic policy. With telecom evidence unavailable, preserve uncertainty. These are different failure modes and deserve different treatment.

### Threat boundaries to make explicit

| Situation | What the signal can establish | What it cannot establish |
|---|---|---|
| Recent SIM change | A provider reports a change within a requested window | That the change was malicious, or its exact age from a boolean-only response |
| Number Verification succeeds | Number association for the authenticated SIM/device flow | Card ownership, payment intent, or freedom from coercion |
| Supported scam signal indicates risk | A provider-specific fraud risk observation | That every ordinary call is a scam, or that every app-based call is covered |
| Verification is unavailable | The selected provider/flow did not establish the fact | That the customer is an attacker or that the fact is safe |
| Biometric authentication succeeds | A verified authentication ceremony succeeded, if implemented | That an authenticated customer is not being deceived |

Source for Number Verification semantics and provider-dependent Wi-Fi support: [CAMARA specification](https://github.com/camaraproject/NumberVerification/blob/main/code/API_definitions/number-verification.yaml). A SIM Swap check returning `swapped=true` over 240 hours must not be converted into the current code's invented `hours=2.0`; obtain supported recency data or retain a time range.

## 5. Make the Business Case Auditable

Use these variables once and reuse them across the plan, deck, and dashboard:

```text
N = monthly bank transactions
f = fraction selected for SafePay evaluation
E = N * f
q = average billable carrier calls per evaluation, including retries
c = average supplier price per call, or an explicitly contracted bundle cost
p = SafePay price per evaluation
a = variable AI/infrastructure cost per evaluation

Monthly revenue = subscription + E * p
Monthly variable cost = E * (q * c + a)
Bank net benefit = avoided fraud cost + measured operating/SMS savings - bank fees
Bank ROI = bank net benefit / bank fees
```

Treat wholesale prices, fraud reduction, and willingness to pay as assumptions until measured or quoted. Do not count the same fraud loss again inside a total-cost multiplier. SMS savings cannot exceed the cost of the authentication events actually replaced. Included usage and subscription pricing must not double-count the same evaluations.

For the current $0.20 pitch, five million monthly bank transfers with 10% selection yields 500,000 billable evaluations/month and $1.2M annual usage fees. This reconciles volume only; it does not validate the chosen selection rate, supplier costs, or benefit estimates. A supplier cost described as a bundle must specify which APIs and retries it includes.

A credible next commercial milestone is a shadow-mode pilot with one prospective bank: return risk recommendations without changing settlements, compare with existing controls, then calibrate interventions on labeled outcomes. Measure incremental fraud capture, legitimate-customer challenge/decline rate, completion rate, signal availability, calls per evaluation, latency distribution, and analyst review time. Synthetic demo scenarios prove execution, not percentage reduction in real fraud.

## 6. Revised Live Demo and Pitch

Use the time limit actually confirmed by the organizer. If the slot is three minutes, a workable structure is:

| Time | What to show | What it proves |
|---|---|---|
| 0:00-0:20 | One user initiating a transfer; explain the selected fraud mechanism | The problem and target user are clear |
| 0:20-0:35 | One sentence about the bank buyer and network evidence | The role of Open Gateway is essential |
| 0:35-1:00 | Legitimate transaction with known provenance | Baseline behavior and low unnecessary friction |
| 1:00-1:40 | Ambiguous case; agent chooses a tool, observes it, and recommends intervention | Agentic automation and end-to-end workflow |
| 1:40-2:10 | High-risk case with independent signal evidence | Multi-signal value and deterministic enforcement |
| 2:10-2:30 | Inject unavailable telecom evidence; show explicit pending/review outcome | Stability and responsible failure handling |
| 2:30-2:50 | One pricing equation and proposed bank pilot | Commercial viability without invented traction |
| 2:50-3:00 | Request a design partner and supported sandbox access | A concrete next milestone |

For vishing, the intervention should visibly stop or postpone the suspicious transfer rather than end with an unverified Face ID success banner. Include a legitimate lookalike during Q&A so judges can see that an active call or recent SIM change is not treated as proof of criminal intent.

Use five or six main slides: problem/customer, product journey, live demo, measured evidence, business/pilot, and next milestone. Put architecture, provider capability matrix, limitations, and policy details in the appendix. The current 15-page PDF gives the architecture its own early slide despite the mentor's advice to put detailed technical material near the end.

Make scores consistent: local preset probes yielded 0, 55, 100, and 75 for clean, scam-call, SIM-swap, and CNP respectively, using a SAR 15,000 unsaved-beneficiary test intent. The three corresponding pitch examples advertise 8, 52, and 94. The live values should come from the engine, and the script should not promise obsolete exact scores.

Keep the main demo in one jurisdiction. The current script calls a SAR 35,000 transaction an Aani UAE example and repeatedly combines Saudi routing with UAE legal conclusions. Confirming a real sandbox call on a supported test identity also matters more than putting three operator logos beside synthetic phone numbers.

### Questions judges are likely to ask

- Which exact API responses came from the provider during this demo, and which were simulated?
- What decision did the agent make that a preset button did not make for it?
- What happens on timeout, missing consent, an unsupported SIM, or a cached result that is too old?
- How does authenticating a legitimate victim stop that victim from paying a scammer?
- Why would a bank buy this in addition to its existing fraud engine or the FICO/JT offering?
- What do you mean by one billable evaluation, and what fraction of transactions needs it?
- Which metrics are measured by your prototype, external pilot results, or future targets?
- What changed because of the mentor discussion, and what remains unvalidated?

## 7. Implementation Priorities Before Pitch Freeze

Ordered by judging and correctness impact; these are acceptance conditions, not changes already made:

1. Correct evidence labels and remove fabricated live telemetry. Acceptance: every displayed API status matches an actual executed, cached, recorded, or simulated observation.
2. Repair uncertainty and transaction state. Acceptance: timeout cannot manufacture authentication; unknown/replayed biometric resolution is rejected; cancellation is stored.
3. Establish one supported CAMARA request in the actual decision flow. Acceptance: validated provider response, request correlation, documented schema/version, and explicit consent/auth assumptions.
4. Implement the bounded agent tool workflow on uncertain cases. Acceptance: model selects an allowed tool, consumes its result, and cannot bypass policy; fallback is visible.
5. Remove optional narrative generation from the fast payment response path. Acceptance: a slow/failing narrator does not delay a completed deterministic outcome.
6. Add a small adversarial scenario set. Cover legitimate SIM replacement, verified number with recent SIM change, unsupported verification, telecom timeout/error, stale cache, ordinary call, scenario-override isolation, replay, and failed/cancelled challenge. Test policies and external behavior, not only predetermined scores.
7. Reconcile the canonical plan, deck, and script. Acceptance: one market, one pricing model, current model identifier, correct temporal framing, no unsupported percentages, and clear prototype boundaries.
8. Rehearse from a cold start with the actual interpreter and dependency environment, including a network interruption and a disclosed recorded fallback. Bundle necessary browser assets for offline demo reliability; the current HTML loads Tailwind and Lucide from remote CDNs.

Do not spend the remaining build window migrating to Next.js, adding more unsupported API names, or expanding into every fraud vector. Static HTML/JavaScript served by FastAPI is adequate for this prototype; the documentation should describe that actual stack.

## 8. Verification Performed and Limits

- Read the master plan, PRD, README, mentor debrief and mentor-related sections of the master plan, previous assessment and threat-model excerpts, economics, pitch source, evaluation dossier, walkthrough script, and progress records. Read both official guide PDFs and extracted the 15-page pitch PDF's outline.
- Inspected all application Python modules, the audit migration, frontend transaction/telemetry/challenge paths, and the existing risk tests. Checked relevant local CAMARA specifications and primary online sources in the companion claim review.
- Ran `python tests/test_risk_engine.py`: four scenario checks plus the performance check passed. The 1,000 local in-memory evaluations took 5.19 ms in this run. This is neither a network benchmark nor an end-to-end load test.
- Ran controlled local ASGI and gateway probes with Python 3.14, synthetic identities, mocked persistence, disabled live Gemini, and a mocked provider adapter. Confirmed fixture scores, fake biometric acceptance, timeout approval, incorrect invocation telemetry, blocked-on-AI response, and invalid input accepted as `+966notaphone`.
- A roaming-only profile produced score 20 and `APPROVE`, despite newer PRD language implying a challenge. Decide the intended policy explicitly; roaming by itself need not indicate fraud.
- The default `python` executable points to a separate environment missing `cachetools` and the PDF packages. The installed Python 3.14 environment had the needed dependencies for the deeper probes and PDF extraction. This is a reproducibility concern for demo launch instructions, not a failure of the scoring test itself.
- No authenticated telecom/model requests, external messages, account changes, or financial transactions were performed. No browser interaction or screenshot review was performed. Supabase persistence, production operator coverage, bank integration, and live cellular authentication remain unverified.
- The meeting assessment is based on the written debrief, not original audio or a verbatim transcript. Local existing app changes were preserved.

Detailed external evidence and source limitations: [Phase 2 Claim Verification](PHASE2_CLAIM_VERIFICATION.md).
