# Phase 2 Claim Verification

Reviewed 2026-09-08 against README.md, PRD.md, MENTOR_MEETING_DEBRIEF_AND_DECISIONS.md, SAFEPAY_FINANCIAL_AND_UNIT_ECONOMICS_DEEP_DIVE.md, and associated pitch materials. This is a claims review, not a legal opinion or proof of implementation. Missing public evidence is classified as unverified, not automatically false.

## Highest-Priority Corrections

### 1. UAE OTP deadline and liability: exact notice remains unverified

The public original of Notice CBUAE/FCMCP/2025/3057 was not located in this research. Its reported existence and March 31, 2026 deadline should not be called fabricated, but the pitch's exact scope cannot be confirmed from the regulator's original text. Third-party summaries distinguish restrictions on OTP as sole authentication from stronger restrictions for 3DS transactions. Obtain the notice through a participating bank or official regulatory source before putting its precise obligations in a compliance claim.

The accessible official Retail Payment Services and Card Schemes rules establish provider liability with exceptions for payer fraud and gross negligence. Article 14 paragraphs 25-26 require reimbursement as soon as practicable and no later than the following business day; paragraph 27 provides a fraud-suspicion exception. These general rules do not establish the pitch's universal rule that every OTP fraud requires an immediate refund, and do not disprove a later special rule for 3DS. [CBUAE Article 14](https://rulebook.centralbank.ae/en/rulebook/article-14-obligations-towards-retail-payment-service-users)

Remove "eliminates 100% bank liability", "court-admissible", and "fully compliant" from prototype claims. A generated explanation is not evidence of certification, complete regulatory coverage, or legal immunity. As of this review, March 31, 2026 is already past; slides describing it as an upcoming deadline are stale.

A defensible adjacent fact is that Emirates NBD offers Smart Pass to replace SMS authorization codes for its online/mobile banking transactions. This supports market movement toward app authentication, not proof that CAMARA Number Verification alone satisfies every authentication obligation. [Emirates NBD Smart Pass](https://www.emiratesnbd.com/en/help-and-support/activate-smart-pass)

### 2. SAR 20,000 is a payment-rail boundary, not a universal fraud prohibition

SAMA's current sarie page explicitly includes transfers equal to or below SAR 20,000 and describes instant, round-the-clock processing. Therefore a predicate for exceeding this ceiling is `amount > 20000`, not `amount >= 20000`. The older 2021 launch announcement uses less-than wording, so cite the current system page when defining the boundary. [SAMA sarie](https://www.sama.gov.sa/en-us/payment/pages/Sarie.aspx)

No reviewed primary source establishes a universal mandatory 24-48-hour fraud hold for every transfer above that amount. Larger transfers can follow other rails and processing schedules. Keep payment routing separate from a bank-configurable high-risk threshold: a SAR 35,000 payment is not inherently unlawful, fraudulent, or made sarie-eligible by adding a biometric check. The mentor debrief can preserve what was said, but its interpretation should not become statutory policy without the actual rule.

### 3. The 85% MENA fraud statistic is unsupported

No primary evidence was found for the claim that 85% of successful payment fraud or regional losses in Saudi Arabia, UAE, and Egypt arise from vishing/social engineering, or that the product intercepts 85% of those scams. Remove the percentage unless a source specifies population, geography, time period, and denominator.

GSMA does publish an 85% number for Scam Signal: coverage of UK mobile users across major UK networks. That is a coverage statistic, not a MENA fraud-loss statistic. It may be a source of confusion, but the origin of the repository's number is unknown. [GSMA Scam Signal case study](https://www.gsma.com/solutions-and-impact/technologies/security/scams/gsma_study/scam-signal/)

### 4. The 44% and 55% results are real external pilot results

FICO's September 18, 2024 release attributes a 44% decline in scam losses and 55% decline in false positives to the first UK bank piloting its FICO/JT solution. These are vendor-reported results from that deployment, not SafePay measurements, MENA benchmarks, or guaranteed effects of any CAMARA integration. Label them "external UK pilot evidence" and separately state SafePay's pilot targets. [FICO/JT original announcement](https://investors.fico.com/news-releases/news-release-details/fico-and-jersey-telecom-collaborate-tackle-authorised-push/)

The same announcement describes contextual warnings, adaptive conversation flows, suggested payment delays, and referral to fraud specialists. Consequently, combining a network scam signal with customer warnings does not establish a first-of-its-kind invention. SafePay needs a more specific differentiation claim, supported by implemented behavior.

### 5. AED 4.99 is total cost, not additional recovery expense

LexisNexis' 2024 EMEA infographic reports a UAE financial-services fraud-cost multiplier of 4.99. Its survey was conducted in July 2023. Use "AED 4.99 in total cost per AED 1 lost to fraud" rather than "AED 4.99 in recovery, legal, and operational expenses" in addition to the stolen dirham. Do not apply this institutional survey average automatically to every MENA bank or assume all of it is avoidable. [LexisNexis original infographic](https://risk.lexisnexis.com/global/-/media/files/financial%20services/infographics/lnrs_emea_fraud_infographic_v2-nxr16395-00-0324-en-us.pdf)

## API Claims and Commercial Availability

### 6. Scam Signal exists, but generic call state is not the complete product

Telefónica describes Scam Signal as correlating network signals with high-risk actions to identify potential scams. Its technical overview says the specification follows CAMARA standards but resides in a private GSMA repository with controlled access. Public documentation does not validate an invented endpoint, response schema, or the assumption that it merely returns an active-call boolean. [Telefónica developer documentation](https://developers.opengateway.telefonica.com/docs/scamsignal), [Telefónica technical overview](https://bxbucket.blob.core.windows.net/bxbucket/opengateway-web/uploads/2025/5/api-overview-scam-signal-20250520.pdf)

Do not imply that an ordinary call is verified malicious, that no call means no scam, or that this checks every messaging-app voice call. Those are implementation/provider questions requiring documented capability and test evidence.

### 7. Regional membership is not per-API production availability

GSMA's 2025 MENA report describes STC OTP SMS and UAE du/e& SIM Swap deployments and broader operator membership. It does not substantiate the README's specific stc/e& Scam Signal availability matrix or direct production access through SafePay's selected aggregator. [GSMA Mobile Economy MENA 2025](https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-economy/wp-content/uploads/2025/11/241125-The-Mobile-Economy-MENA-2025.pdf)

Classify unconfirmed combinations as planned or awaiting provider confirmation. A credible matrix should distinguish API name/version, operator/country, sandbox availability, approved production access, consent requirements, and date last verified. Lack of a public listing is not proof the service is unavailable through private agreements.

### 8. Number Verification proves a number association, not payment intent

The CAMARA definition verifies whether the supplied phone number matches the number associated with the authenticated device/SIM. It requires a three-legged token. Authentication without a TS.43 temporary token uses an authorization-code flow requiring mobile-network connectivity. TS.43 token flows can also work over Wi-Fi. Thus "always cellular-only" is an overgeneralization; support depends on the selected provider and flow. [CAMARA Number Verification specification](https://github.com/camaraproject/NumberVerification/blob/main/code/API_definitions/number-verification.yaml)

Engineering implication: a successful result alone does not prove card ownership, freedom from coercion, an uncompromised handset, or authorization of the particular payment. A failure to establish a supported bearer is not proof of an attacker. "Leaked card numbers become useless" and "all OTP attack surface eliminated" exceed this API's contract. Use a payment-bound bank authentication flow, explicit unknown/error states, and appropriate fallback. A 300ms target also needs provider measurements; it is not established by the API definition.

## Financial Plan Consistency

These are arithmetic and evidentiary findings from the local financial plan, not externally established market forecasts:

- The sample $8,000 monthly contract costs $96,000 annually. Two avoided cases at the plan's $4,000 average cover one month, not its stated entire annual contract.
- The sample monthly net savings of $55,500 and 693.75% net ROI are arithmetically consistent with $63,500 gross modeled savings and $8,000 fees. Their inputs remain unvalidated assumptions.
- A SAM of $45M ARR from 150M annual calls implies $0.30 per call. Reconcile this with $0.025-$0.035/check pricing and distinguish transactions, carrier calls, billable checks, included allowances, and SaaS subscriptions.
- Thirty million checks are 20% of 150 million, not the cited 12% penetration. The denominator needs clarification.
- Per-check COGS budgets only one $0.01 carrier call. Multi-API orchestration needs expected calls per evaluated transaction, retries, unavailable signals, cache misses, and explicit bundled pricing.
- A 62% fraud reduction, 15% churn reduction, 92% telecom margin, and named operator wholesale prices have no demonstrated source or contracted quote in the reviewed plan. Present scenario assumptions with sensitivity ranges, not operating results.

## Recommended Evidence Before Pitch Freeze

Obtain the original UAE notice and control scope; obtain a provider-confirmed operator/API matrix and actual schema; label every performance number as local measurement, target, or external reference; and replace the mixed pricing units with one auditable transaction-level model. The strongest supported pitch is a prototype for adding network risk evidence to payment decisions, with external evidence that this category can reduce APP fraud. SafePay's own effectiveness and legal compliance still require validation.
