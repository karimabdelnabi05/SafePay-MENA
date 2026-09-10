# SafePay MENA: Submission Deck and Speaker Notes

Prepared 10 September 2026. Submit **SafePay_MENA_Phase2_Pitch_Deck.pdf** only as the presentation. It contains 13 main slides plus 4 appendix slides; the technical summary is the final slide. This document is internal preparation, not a second presentation.

The HTML file is the presentation source. Export with `py -3.14 build_phase2_pitch_deck.py`; use `--capture` to refresh app screenshots and the 36-case acceptance check. The build checks slide boundaries, footer clearance, loaded images, PDF page count and aspect ratio, and renders every PDF page for visual inspection. Development dependencies are Playwright (with Chromium), pypdf, pypdfium2 and Pillow; they are not application runtime dependencies.

## Story and Audience

The mentor debrief recommends a business-first narrative for a panel covering business, IT, cybersecurity and fintech, with numbers, reliability and user experience up front and technical architecture at the end. This deck follows that direction without treating mentor statements as verified financial or regulatory facts.

| Judge perspective | Main evidence | Slides |
|---|---|---|
| Business | Cost of fraud, bank benefit, pricing, gross margin, scale, pilot ask | 4, 10-14 |
| Fintech / regional impact | Payment adoption in Egypt, Saudi Arabia and UAE; existing bank/wallet distribution | 2-3, 5, 12 |
| Customer experience | Routine zero-call path, mandatory setup checks, clear actions and cancellation | 5-6 |
| AI / innovation | Adaptive tool choice, observation-dependent investigation, external category precedent | 7, 9 |
| IT / cybersecurity | Repeatable tests, recorded Nokia integration, enforced policy, missing-data behavior | 8, 17 |

## Speaker Track

Timing below is a rehearsal suggestion, not a verified hackathon time allowance. The main script is approximately five minutes at conversational pace. Leave additional time for a hands-on demo if the official slot permits it. Use the appendix for questions rather than narrating all 17 slides.

### 1. SafePay MENA

"SafePay helps banks make safer payment decisions without adding unnecessary checks to everyday payments. It looks at the payment context, asks the mobile network for evidence when risk changes, and gives the bank a clear action. We have a working prototype covering three market contexts and 36 repeatable acceptance cases."

### 2. Why now

"The adoption is already here. Egypt reported nearly 1.5 billion IPN transactions for 2024. Electronic payments made up 85% of Saudi retail payments in 2025. Aani reported more than 12.5 million registered users in April 2026. These measure different things, but all show that digital payments are becoming everyday infrastructure. We sell to the bank or wallet, so customers can stay in their existing app."

### 3. Regional scam prevalence

"Visa's study makes the customer exposure clear: 43% of respondents in Egypt, 43% in Saudi Arabia and 49% in the UAE said they had ever been scam victims. This is lifetime, self-reported experience, not a percentage of payments that are fraudulent. It shows why customers across our three target markets need more protection."

### 4. The cost and the problem

"The damage extends beyond the stolen payment. A published UAE financial-services survey found that every dirham lost to fraud cost 4.99 dirhams in total. The bank also faces associated investigation and operational costs. Our scenarios cover a deceived customer, an account takeover, and stolen card details. The key insight is that confirming someone's identity does not necessarily confirm safe payment intent."

### 5. What SafePay does

"We return three understandable payment outcomes. A routine transfer can proceed without extra calls. A customer reporting a suspicious request gets a hold, even when the mobile identity matches. An unusual session combined with SIM and device changes can trigger a block. First setup and a new phone always require number verification and a SIM-change check. Missing required evidence leads to a retry."

### 6. Show the product

"This is the actual connected prototype. The decision is visible first, while the timeline shows local screening, Gemini choosing each relevant check, Nokia returning sandbox evidence, and deterministic policy making the final decision. The capture used synthetic payment facts and Nokia simulator identities, so it proves the integration without claiming a production customer or money movement."

### 7. Why an agent

"The agent's job is to decide which question is worth asking next. A SIM change in an unusual session can justify checking a device change. Travel may justify a roaming check. It observes the answer before choosing the next tool, and stops when enough evidence is available. This is bounded by policy: the AI cannot grant itself authority to release an unsafe payment."

### 8. What is proved

"We passed 36 synthetic acceptance cases and 103 automated tests: 79 backend and adapter tests plus 24 browser tests. Five integrated network capabilities have recorded successful Nokia sandbox responses. Our latest takeover investigation used three context-eligible Nokia tools and four Gemini turns. These numbers prove software behavior and integration. They do not yet prove a real-world fraud reduction percentage. That is the purpose of the pilot."

### 9. Why this category

"There is external evidence that network-informed intervention can help. FICO and Jersey Telecom reported 44% lower scam losses and 55% fewer false positives at their first UK pilot bank. Those are their results, using a different product. Our implementation focuses on selective investigations, multiple customer journeys, and policy-controlled decisions. We would add this evidence to a bank's existing fraud workflow and measure the incremental benefit."

### 10. Bank economics

"Here is a transparent example, not a claimed customer result. If the covered portfolio loses eighty thousand dollars a month and SafePay helps reduce those losses by 25%, twenty thousand dollars is avoided. Subtract an eight-thousand-dollar fee and twelve thousand remains, before the bank's implementation and added operating costs. A ten-percent reduction covers the fee. We have excluded speculative SMS and conversion savings."

### 11. Our business model

"Our pricing proposal is three thousand dollars per month plus five cents per investigation. At one hundred thousand investigations that is eight thousand dollars in revenue. With two and a half network checks on average, one cent per check, and budgets for AI, hosting and support, direct cost is four thousand dollars. That means a modeled 50% gross margin. The pilot must validate those prices and volumes."

### 12. Distribution and scale

"We start with one bank or wallet and a network partner. We focus the first integration on new-device trust and suspicious payment review, then expand with the same decision interface. At the example pricing and volume, ten customers represent 960 thousand dollars in annual recurring revenue. That is a scale scenario, not a sales forecast. Each customer also creates demand for paid network checks."

### 13. Close and ask

"We are seeking one bank or wallet and one operator or API partner for a proposed ninety-day pilot. We will measure loss reduction, legitimate-customer abandonment, provider availability, latency and cost. We want everyday payments to stay easy, while risky payments receive the evidence they need."

## Demo Cue

Start in fixture mode with a routine payment to demonstrate zero external calls. Then unlock **Connected: Nokia + Gemini** and run SIM-swap takeover so the judges can follow actual tool selection and Nokia simulator responses. If provider quota is unavailable, state that clearly and use the actual connected capture on slide 6 before continuing with the explicit fixture fallback. Run the 36-case evaluation as a software-quality proof point, not a fraud-accuracy result.

Demo URL: https://safepay-mena-demo.onrender.com/. Hosted connected activation must be verified separately; the PDF identifies its connected screenshot as a local run.

## Fraud Statistics Added in This Revision

Slide 3 now establishes regional prevalence using the same Visa/Wakefield survey and question across all three markets. Slide 15 gives a separate global merchant exposure benchmark: real-time payment fraud 45%, phishing/pharming/whaling 42%, card testing 33%, account takeover 26%. All four figures were checked against the original chart, not inferred from PDF text order.

These percentages are not shares of fraud incidents or losses, are not MENA rates, and do not add to 100%. Card testing is not all card leakage/CNP fraud; account takeover is not equivalent to SIM swapping. No credible common-denominator MENA split for the prototype's fraud categories was verified. A phishing attack can steal card details or enable an account takeover, so the mechanisms overlap.

The older local research's 65-75% social engineering, 15-20% card fraud, 5-10% eSIM and 3-5% physical SIM swap ranges are unsupported. Do not present them to judges. No SIM-swap percentage is assigned in this deck.

Final order: 1-13 main narrative; 14 commercial sensitivity; 15 fraud-type benchmark; 16 sources; 17 technical summary. Present the close on slide 13; use the remaining slides for questions.

## Evidence Ledger

| Figure | Type | Exact meaning and boundary |
|---|---|---|
| 43% / 43% / 49% | Consumer survey | Egypt / Saudi Arabia / UAE respondents saying they had ever been scam victims. Visa Stay Secure 2025, page 5. Weighted online survey, 4-15 Dec 2024; n=600 / 300 / 300 respectively. Not annual financial-loss rates. |
| 45% / 42% / 33% / 26% | Global merchant survey | Merchants reporting real-time payment fraud / phishing-pharming-whaling / card testing / account takeover in the previous 12 months. 2025 Global eCommerce Payments & Fraud Report, page 23, Figure 21; fraud-professional sample n=576. Multiple-response exposure rates, not MENA loss shares. |
| SIM-swap share | Unverified | GSMA documents the mechanism, but a defensible share of MENA fraud was not verified. Not estimated as zero or equated with the 26% account-takeover exposure figure. |
| Nearly 1.5bn / EGP 2.9tn | Published fact | Egypt IPN transactions / value reported for 2024; not SafePay volume or revenue. CBE's own indexed search excerpt confirms the numbers, but its linked article rejected automated access. |
| 85% / 14.6bn | Published fact | Saudi retail electronic-payment share / electronic transaction count in 2025. Not sarie-only transactions. |
| 12.5m+ / 74 / 3 seconds | Published fact | Aani registered users / connected institutions / average transfer completion reported April 2026. Users are not SafePay customers and institutions are not prospective signed accounts. |
| 4.99x | Published survey | UAE financial-services total fraud cost divided by original loss. It includes the original loss; 3.99 is the arithmetic remainder. EMEA sample 541, UAE subset not stated. July 2023 fieldwork, published 2024. |
| 44% / 55% | External pilot | FICO/JT vendor-reported scam-loss / false-positive reductions at the first UK pilot bank. Different signals and intervention. Not SafePay results or a transferable efficacy estimate. |
| 0 calls | Implemented behavior | Local routine-payment path requests no model or network evidence. Does not establish what fraction of real payments will qualify. |
| 2 required checks | Implemented behavior | Fresh Number Verification and SIM Swap for setup/new phone. These are logical capabilities, not exactly two HTTP requests. |
| Up to 5 tools | Implemented bound | Maximum evidence tools in one live investigation. A budget exhaustion triggers recoverable failure rather than more calls. |
| 36/36 | Acceptance result | 12 journeys times 3 synthetic markets. Exact expected decisions, tool plans and evidence status. Not detection accuracy. Rerun during deck generation. |
| 103/103 | Recorded QA result | 79 backend/adapter and 24 browser tests rerun on 10 Sep. |
| 5 APIs | Recorded sandbox evidence | Integrated SIM Swap, Number Verification, Device Swap, Roaming, Reachability each have historical successful simulator responses. Not a current uptime promise or production operator coverage. |
| 3 tools / 4 turns | Recorded live case | Latest local Nokia/Gemini takeover investigation; completed in under 10 seconds end to end. Not representative production latency. |
| 25% loss reduction | Hypothesis | Scenario to validate on a defined portfolio; not derived from the FICO percentage. |
| $80k / month losses | Assumption | One hypothetical customer's covered payment portfolio, not a measured MENA bank average. |
| $3k + $0.05 | Pricing proposal | Monthly platform fee plus a billable investigation fee; not contracted or market-validated. |
| 1m events / 100k investigations | Volume assumption | Includes mandatory enrollment and new-device workflows in the investigation bucket. The 90/10 mix is not a product measurement. |
| 2.5 checks / $0.01 | Cost assumption | Average logical checks per investigation / blended cost per check. Provider quotes, paid retries and OAuth tariffs remain unknown. |
| $0.005 AI | Cost budget | Average aggregate model expense per investigation, covering all turns. Not price per turn; zero-LLM enrollment may lower the average. |
| $1k infrastructure/support | Cost assumption | Monthly direct delivery allocation per modeled customer. Needs load/support validation. |
| 1 / 5 / 10 clients | Scale scenario | $96k / $480k / $960k ARR at the same per-customer volume and pricing, not customer acquisition or a forecast. |
| 90 days | Proposed plan | Pilot window after agreement and access. Labeled sample sufficiency, not the calendar alone, controls efficacy conclusions. |

## Reconciled Arithmetic

- Investigations: 100,000; checks: 100,000 x 2.5 = 250,000.
- Revenue: $3,000 + 100,000 x $0.05 = $8,000/month.
- Direct costs: 250,000 x $0.01 + 100,000 x $0.005 + $1,000 = $4,000/month.
- Gross profit: $8,000 - $4,000 = $4,000; margin: $4,000 / $8,000 = 50%.
- Bank avoided loss: $80,000 x 25% = $20,000; benefit after fees: $20,000 - $8,000 = $12,000/month, or $144,000 annualized.
- Fee-only break-even reduction: $8,000 / $80,000 = 10%; actual break-even includes the bank's added costs.
- At network-check costs $0.005 / $0.010 / $0.020 / $0.030, direct costs are $2,750 / $4,000 / $6,500 / $9,000, with margins 65.625% / 50% / 18.75% / -12.5% (display rounded to one decimal).
- At 4 checks/investigation and $0.01/check: total direct cost $5,500; margin 31.25%.
- Provider spend: $2,500/month per modeled customer, not pure operator revenue or operator profit.

## Questions to Prepare For

**Why would a bank use this if it has an existing fraud engine?**
SafePay proposes an additional evidence and orchestration layer, with selective calls and an explainable decision record. The bank pilot must compare its existing workflow against the augmented workflow at matched customer-friction levels.

**Why use AI instead of rules alone?**
The implemented agent chooses and revises tool use from observations under fixed safety rules. Superiority over a rules-only planner has not been established. A pilot should compare the two on outcome quality, cost, latency and unnecessary calls.

**Does a SIM swap always mean fraud?**
No. The implemented policy considers combined evidence and context. Legitimate travel and unavailable provider evidence also have distinct tested outcomes.

**Do you detect someone speaking to a scammer?**
No active-call or Scam Signal API is implemented. The demo includes customer-reported suspicious-call context. Number Verification does not reveal payment intent.

**Have you eliminated SMS OTP or bank liability?**
No. Number Verification supplies an identity association in a supported authorization flow. Payment authorization, production consent, device binding and bank security requirements still apply. The deck makes no regulatory certification or liability-elimination claim.

**What does a 90-day pilot actually test?**
Begin with integration and retrospective baselines; run shadow decisions on labeled events; advance to a bank-approved controlled intervention only when access and safety gates are met. Compare losses per settled value, false-positive holds on legitimate events, abandonment, measured p95 latency, provider success rate and cost per investigation. Separate enrollment from payment decisions. Agree tolerances and sample requirements before the pilot; extend observation if labels are sparse.

**Are the old financial forecasts still current?**
No. This deck supersedes the earlier commercial narrative. Do not use claims such as certified 693% ROI, 62% fraud reduction, $7.8m ARR, or named wholesale tariffs as established facts. The model here is internally consistent and explicitly hypothetical.

## Primary References

1. [Central Bank of Egypt, IPN/InstaPay announcement, 30 Dec 2024](https://www.cbe.org.eg/en/news-publications/news/2024/12/30/12/31/cbe-extending-the-exemption-of-individuals-from-instapay-for-a-renewable-period-of-3-months).
2. [SAMA, electronic payments in 2025, 12 Apr 2026](https://sama.gov.sa/en-US/MediaCenter/News/Pages/news-1139.aspx).
3. [Al Etihad Payments, Aani operational update, 10 Apr 2026](https://aep.ae/en/news-media/press-releasesarticles/aani-delivers-a-transformational-leap-in-the-uae-s-digital-payments-landscape-125-million-users-and-instant-transfers-in-3-seconds/).
4. [LexisNexis Risk Solutions, 2024 EMEA fraud-cost infographic](https://risk.lexisnexis.com/global/-/media/files/financial%20services/infographics/lnrs_emea_fraud_infographic_v2-nxr16395-00-0324-en-us.pdf).
5. [FICO/JT, original announcement, 18 Sep 2024](https://investors.fico.com/news-releases/news-release-details/fico-and-jersey-telecom-collaborate-tackle-authorised-push/).
6. [SafePay QA report](PHASE2_QA_REPORT.md).
7. [Nokia sandbox verification](NOKIA_SANDBOX_VERIFICATION.md).
8. Commercial scenarios are internal assumptions, with arithmetic on slides 10-12 and 14.
9. [Visa Stay Secure 2025, pages 5 and 13](https://km.visamiddleeast.com/content/dam/VCOM/regional/cemea/genericmena/pay-with-visa/security-and-assistance/stay-secure-2024/stay-secure-report.pdf).
10. [2025 Global eCommerce Payments & Fraud Report, page 23, Figure 21](https://www.visaacceptance.com/content/dam/documents/campaign/fraud-report/global-fraud-report-2025.pdf).
11. [GSMA, Scam Advice: Fraudulent SIM Swap](https://www.gsma.com/solutions-and-impact/technologies/security/scams/scam-advice-fraudulent-sim-swap/).
