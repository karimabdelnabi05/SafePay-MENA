# SafePay MENA Phase 2 Rubric Scorecard

Reviewed: 9 September 2026

## Scoring Method

GSMA supplied the criteria but no weights. This review therefore scores each of the 14 listed subcriteria equally on a 10-point scale.

- 9-10: judge-ready, differentiated, and supported by strong visible evidence
- 7-8.9: strong hackathon prototype with identifiable validation gaps
- 5-6.9: credible direction with material proof or readiness gaps
- Below 5: mostly proposed, unclear, or not yet demonstrated

The scores are deliberately conservative. Fixture tests establish repeatable software behavior; they do not prove fraud reduction, market demand, production operator coverage, or regulatory compliance.

## Executive Score

| Category | Score |
|---|---:|
| Innovation & Originality | 7.8 / 10 |
| Impact | 7.0 / 10 |
| Scalability & Commercial Viability | 5.5 / 10 |
| Technical Feasibility & Open Gateway API Usage | 8.5 / 10 |
| Agentic AI & Multi-API Orchestration | 8.0 / 10 |
| Presentation & Pitch | 8.3 / 10 |
| **Equal-weight overall** | **7.4 / 10** |

This is a strong technical Phase 2 prototype, not yet a commercially validated product. The fastest route above 8/10 is better proof, not more features: publish the fixture demo, show a clearly labeled recorded live-agent trace, define a credible pilot, and support the MENA need with sourced market evidence.

## 1. Innovation & Originality

### Creativity and uniqueness of the solution - 7.5 / 10

**Evidence:** SafePay combines local zero-call screening, network evidence, a bounded AI investigator, deterministic release policy, multiple payment channels, and explicit unknown/failure handling. The separation between evidence selection and consequence control is a thoughtful design.

**Why it is not higher:** Telecom-assisted payment fraud prevention already exists as a product category. The project cannot defensibly claim to be first or unique merely because it combines network signals with warnings or holds. Its differentiation needs to be stated more precisely.

**Raise the score:** Frame the novelty as the implemented control architecture: risk-gated API spending, context-dependent tool choice, mandatory new-device trust, intent-aware holds even after identity verifies, and deterministic limits on agent authority. Compare that architecture against one or two adjacent approaches without claiming a world first.

### Innovative application of Open Gateway APIs - 8.0 / 10

**Evidence:** Five Nokia Network as Code capabilities are implemented behind a restricted adapter: SIM Swap, Number Verification, Device Swap, Roaming, and Reachability. SafePay uses them selectively and preserves their semantic limits rather than treating each boolean as a fraud verdict.

**Why it is not higher:** The repeatable public flow uses fixtures, Reachability is available to the live agent but is not central to a judged scenario, and production MENA operator availability is unverified.

**Raise the score:** Demonstrate two contrasting agent trajectories in one visible trace, such as SIM/device checks for takeover and roaming for planned travel. Explain why each unused API was deliberately skipped.

## 2. Impact

### Ability to solve real-world challenges in MENA - 7.0 / 10

**Evidence:** The prototype addresses SIM takeover, card leakage, suspicious instant transfers, new-device enrollment, velocity, identity mismatch, travel, and provider outages across Egypt, Saudi Arabia, and the UAE. Those are recognizable payment and identity risks.

**Why it is not higher:** Country selection currently changes currency and rail context, not operator behavior, consent, policy, language, or verified market controls. No bank, wallet, operator, or user has validated the workflow.

**Raise the score:** Add one sourced problem fact and one validated workflow need per target market. Secure even a short written confirmation or interview insight from a payment-provider or operator stakeholder, and distinguish common regional logic from market-specific configuration.

### Value delivered to users, businesses, or society - 7.0 / 10

**Evidence:** Users retain instant routine payments; suspicious payments remain held instead of silently released; providers receive explainable evidence and a bounded trace; operators gain a credible API consumption use case.

**Why it is not higher:** Prevented losses, reduced false positives, lower support cost, and customer-trust gains have not been measured. The current UI represents a decision workspace rather than the final consumer banking experience.

**Raise the score:** Define pilot KPIs before quoting benefits: fraud-loss rate, false-positive rate, investigation rate, completion latency, CAMARA calls per transaction, cost per investigated transaction, and customer abandonment.

## 3. Scalability & Commercial Viability

### Potential for large-scale adoption - 6.5 / 10

**Evidence:** SafePay exposes a small HTTP decision API, keeps routine traffic on a zero-external-call path, separates market configuration, restricts costly investigations, and demonstrates isolated concurrent reviews.

**Why it is not higher:** The store is in-memory SQLite, the service is single-instance, and there is no production authentication, tenant isolation, queueing, observability, operator routing, or contracted API access. Sixty local requests are a correctness check, not a load benchmark.

**Raise the score:** Publish an integration contract and production architecture covering durable storage, tenant isolation, idempotency, rate limits, provider retries, circuit breaking, audit retention, data residency, and per-operator routing.

### Sustainable business model - 5.5 / 10

**Evidence:** The current deck names plausible buyers and proposes a platform fee plus usage pricing only for investigated transactions. Risk-gated calls align the technical design with cost control.

**Why it is not higher:** Pricing, wholesale API cost, willingness to pay, sales cycle, gross margin, and avoided-loss value are all unvalidated. Earlier detailed financial figures were removed because their assumptions were not defensible.

**Raise the score:** Present a hypothesis, not a forecast: buyer, budget owner, unit of billing, included allowance, expected calls per investigated transaction, unknown/retry cost, and a sensitivity range using provider-confirmed quotes when available.

### Commercial readiness beyond the hackathon - 4.5 / 10

**Evidence:** There is a deployable fixture service, documented API, security boundaries, test suite, pitch, demo script, and a concrete request for a one-operator/one-provider pilot.

**Why it is not higher:** There is no deployed judge URL yet, production payment integration, pilot commitment, legal/consent design, durable audit store, service-level objective, support plan, or production Open Gateway access.

**Raise the score:** Deliver a stable public fixture URL and a six-week pilot plan with named roles, entry criteria, synthetic-to-shadow-to-controlled phases, KPIs, data responsibilities, security review, and exit decision.

## 4. Technical Feasibility & Open Gateway API Usage

### Quality and depth of CAMARA API integration - 8.5 / 10

**Evidence:** The adapter uses real Nokia endpoints, simulator-only subjects, validated booleans, bounded timeouts, explicit UNKNOWN states, Number Verification OAuth discovery, redirect allowlisting, and bound state. Successful live enrollment and agent-assisted suspicious-transfer runs were recorded before the free plan returned HTTP 429.

**Why it is not higher:** Evidence is sandbox-only; later live probes were rate-limited; production operator/consent behavior is unknown; and current live reliability cannot be guaranteed during judging.

**Raise the score:** Obtain refreshed quota or sponsor-approved access, capture a sanitized timestamped trace for every claimed capability, and prepare a recorded fallback that is unmistakably labeled as a prior live sandbox run.

### Functionality and stability of the prototype - 9.0 / 10

**Evidence:** The final gate covers 75 backend/adapter tests and 19 Chromium tests. Core policy coverage is 100%; the API is 96%; the Nokia adapter is 91%; the investigator is 90%. The in-product gate passes 36/36 cases, and ten repeated runs passed 360/360 cases. Failures, cancellation, expiration, concurrency, invalid model calls, and rate limits have explicit tests.

**Why it is not higher:** External live availability is outside the prototype's control, persistence is not production-grade, and there is no full deployment/CI load test.

**Raise the score:** Add CI, a deployed smoke test, structured observability, and one controlled soak/load profile against a production-shaped database and worker configuration.

### Smooth end-to-end user experience - 8.0 / 10

**Evidence:** The interface guides the tester from market and scenario selection to one primary action, then presents disposition, separate risk scores, evidence, reasons, and trace progressively. It includes loading, retry, cancellation, session recovery, state clearing, desktop/mobile/landscape overflow checks, visible labels, native controls, and `aria-busy` feedback.

**Why it is not higher:** There is no automated accessibility audit, Arabic/RTL experience, screen-reader walkthrough, or actual consumer-app step-up flow. The interface is optimized for judges/analysts rather than bank customers.

**Raise the score:** Run keyboard, contrast, and screen-reader QA; add an Arabic/RTL demo mode; and prototype one short consumer warning/confirmation journey without pretending a browser can provide hardware attestation.

## 5. Agentic AI & Multi-API Orchestration

### Intelligent orchestration of one or more CAMARA APIs - 8.5 / 10

**Evidence:** Gemini receives observable transaction context and pre-screen reasons, selects among five allowlisted tools, inspects function responses, and decides whether another observation is useful. Phone subjects, URLs, tool names, schemas, repeats, budgets, and cancellation are enforced outside the model.

**Why it is not higher:** The public fixture demo uses a deterministic tool plan, and only limited live trajectories completed before sandbox rate limiting. There is no scored tool-selection evaluation across a large adversarial prompt set.

**Raise the score:** Add a trajectory evaluation that scores required-tool recall, irrelevant-call rate, repeat/invalid-call rejection, average CAMARA calls, completion rate, and policy agreement across at least 50 controlled agent cases.

### Effective use of AI agents for automation and decision-making - 7.5 / 10

**Evidence:** The agent automates evidence selection and iteration while deterministic policy owns release consequences. Unsafe approval cannot weaken a supported block; unsupported BLOCK proposals cannot manufacture network certainty; malformed or incomplete work fails recoverably.

**Why it is not higher:** The agent's incremental value over a deterministic router has not been measured. Live success rate, latency distribution, cost, tool-choice accuracy, and behavior under prompt injection are not quantified beyond focused tests.

**Raise the score:** Compare the agent with a rule-router baseline and show where it reduces calls or handles novel combinations better. Report tool-trajectory metrics and include adversarial context tests.

## 6. Presentation & Pitch

### Clarity and structure of the presentation - 8.5 / 10

**Evidence:** The 10-slide deck follows a clean sequence: decision gap, workflow, working product, scenarios, APIs, agent controls, QA, commercial path, and pilot ask. The PDF is 16:9, has zero measured slide overflow, and avoids unsupported statistics.

**Why it is not higher:** Ten slides can still exceed a short live-demo window if narrated fully. The technical proof is stronger than the emotional user story.

**Raise the score:** Use only the essential slides during the live demo, open with one concrete victim/payment moment, and move detailed API and QA material to backup slides.

### Communicating problem, solution, technical approach, and business value - 8.0 / 10

**Evidence:** The current deck communicates the bank/network visibility gap, zero-call path, bounded agent, five APIs, deterministic policy, three target markets, buyer, commercial hypothesis, and pilot ask.

**Why it is not higher:** Business value remains qualitative, market proof is thin, and the judged agent experience is vulnerable if the live sandbox is still rate-limited. A public URL has not yet been added.

**Raise the score:** Rehearse a three-minute primary path and a two-minute Q&A proof path. Publish the fixture demo, prepare a 30-60 second recorded live-sandbox trace, and end with a measurable pilot request rather than a broad partnership request.

## Highest-Value Next Actions

1. **Publish the fixture demo.** Add the stable URL and verify it on desktop and mobile from a clean device.
2. **Make real agent evidence judge-visible.** Use refreshed sponsor quota or a clearly labeled recording of the successful live sandbox trajectory; never present fixture evidence as live.
3. **Create a pilot one-pager.** Name the buyer, operator partner, six-week stages, required data, KPIs, decision threshold, and responsibilities.
4. **Strengthen the MENA proof.** Use primary sources and stakeholder validation for one concrete problem/need in Egypt, Saudi Arabia, and the UAE.
5. **Quantify orchestration quality.** Add a controlled agent trajectory evaluation and a deterministic-router comparison.
6. **Rehearse failure handling.** Demonstrate routine zero-call, one escalated case, and provider-unavailable RETRY; keep the 36-case gate and live trace as proof.
7. **Close accessibility gaps.** Verify keyboard order, focus visibility, contrast, screen-reader output, and Arabic/RTL layout.

Completing the first four actions credibly could move the overall evaluation from approximately 7.4 to the low-to-mid 8s without expanding the feature set.
