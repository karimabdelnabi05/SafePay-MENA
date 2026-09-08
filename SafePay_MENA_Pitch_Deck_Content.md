# SafePay MENA - Master Pitch Deck Content
### GSMA MENA Ignite Hackathon (Phase 2 Submission) | Karim Mohamed Abdelnabi
### Theme 4: Secure FinTech, Payments & Anti-Fraud Innovation

---

> **Format Guidelines:** 16:9 widescreen presentation deck.
> Put each full sentence on its own line.
> Color Palette: Cyber Dark Navy (`#070C18`), Electric Cyan Accent (`#00F2FE`), Indigo Accent (`#818CF8`), Emerald Success (`#10B981`), Amber Warning (`#F59E0B`), Crimson Danger (`#EF4444`).

---

## Slide 1: TITLE & COVER

**SafePay MENA**
*Real-Time AI Telecom Fraud Shield for Instant Payments*

- **Theme 4:** Secure FinTech, Payments & Anti-Fraud Innovation
- **Platform:** GSMA Open Gateway • Nokia Network-as-Code • Google Gemini 2.0 Flash
- **Developer:** Karim Mohamed Abdelnabi (Solo Full-Stack & AI Engineer)
- **Assigned Mentor:** Eng. Abdullah A. Alkaoud (stc)

**Visual Layout:**
- Dark background (`#070C18`) with glowing cyan shield icon and telecommunications circuit trace.
- Official GSMA Open Gateway, Nokia Network as Code, and Google Cloud badges in the footer.

**Speaker Notes:**
SafePay MENA is an AI-orchestrated telecom-banking security middleware that stops instant payment fraud before money moves.
It integrates banking payment rails with telecom operator intelligence through standardized GSMA CAMARA network APIs.
Our dual-engine architecture delivers sub-10ms deterministic authorization alongside explainable Gemini 2.0 Flash regulatory traces.

---

## Slide 2: THE EXECUTIVE HOOK

**Headline:**
The Instant Payment Boom Has a 3-Second Settlement Vulnerability.

**Key Highlight:**
> "Egypt's InstaPay processed 1.5 billion transactions worth EGP 2.9 trillion in 2024.
> Saudi Arabia's Sarie and the UAE's Aani settle instant transfers in under 3 seconds.
> Every transaction is irreversible.
> Once fraudulent money moves, recovery drops to near zero."

**The Regional Cost:**
- **AED 4.99 Lost per AED 1 Stolen:** LexisNexis 2024 research confirms UAE financial institutions lose AED 4.99 for every single dirham stolen due to legal, investigatory, and reimbursement costs.
- **42% of MENA institutions** reported year-over-year increases in fraud volume.

**Speaker Notes:**
Instant payments have revolutionized financial inclusion across Egypt, Saudi Arabia, and the UAE.
However, their greatest feature, instant irreversible settlement, has become their greatest vulnerability.
When a victim is tricked into authorizing a transfer, the funds vanish across mule accounts in three seconds.
Financial institutions do not just lose the stolen amount; they lose five times that amount in total operational costs.

---

## Slide 3: THE TWO ATTACK VECTORS MENA FACES

**Headline:**
Understanding the Real Fraud Landscape in Egypt, Saudi Arabia, and the UAE.

| Attack Vector | Payment Channel | Fraud Mechanism | Why Traditional Security Fails |
|---|---|---|---|
| **Vector 1: Active Vishing & Coercion (85% of Losses)** | Instant Push Rails (InstaPay, Sarie, Aani) | Scammers impersonate bank or government portals (Musaned, Sadad) and keep victims on active phone calls for 20+ minutes. | The victim authorizes the transfer using their internal PIN. Bank rule engines see legitimate credentials. |
| **Vector 2: Online Card Leakage & 3DS Takeover** | E-Commerce Checkouts & Wallet Cash-In | Compromised card details (PAN/CVV) drained via leaked SMS OTP codes or rogue handsets. | Scammers intercept or socially engineer the 6-digit SMS code displayed on the handset screen. |

**The Telecom Blind Spot:**
Banks can see IP addresses and device cookies.
Banks cannot see whether a user is currently on an active scam phone call or whether their SIM card was swapped two hours ago.

**Speaker Notes:**
We must be clear about how fraud actually happens in our region.
On InstaPay Egypt, there is no SMS OTP during routine transfers; users enter an IPN PIN.
The fraud here is social engineering and vishing, where scammers keep victims on active phone calls and manipulate them into sending funds.
Meanwhile, in online e-commerce checkouts, banks still rely on vulnerable SMS OTPs that get stolen or intercepted.
Banks are operating blind because they have zero visibility into mobile network state.

---

## Slide 4: THE REGULATORY TSUNAMI

**Headline:**
Central Banks Are Enforcing Immediate Liability Shifts.

**CBUAE Notice 2025/3057 (United Arab Emirates):**
- **Mandate:** Complete retirement of SMS and email OTPs for high-value transactions by March 31, 2026.
- **Liability Shift:** If a customer falls victim to fraud where an SMS OTP was utilized, the financial institution is held 100% financially liable.

**SAMA Counter-Fraud Framework & CST SIM Caps (Saudi Arabia):**
- Strict Sarie 20,000 SAR instant threshold and RTGS holding controls.
- Mandated biometric SIM ownership limits and explainable fraud reporting for all high-risk automated blocks.

**The Urgent Need:**
Financial institutions must replace SMS OTPs with silent possession verification and active scam call detection before the March 2026 deadline.

**Speaker Notes:**
Regulators across MENA have stopped asking politely.
The Central Bank of the UAE issued Notice 2025/3057, mandating the complete retirement of SMS OTPs by March 31, 2026.
Crucially, if a bank authenticates a payment using SMS OTP and the user is defrauded, the bank is held 100% liable for reimbursement.
In Saudi Arabia, SAMA requires strict real-time fraud monitoring and explainable automated decisions.
SafePay MENA gives banks the exact compliance shield they need to eliminate liability.

---

## Slide 5: THE SOLUTION - SAFEPAY MENA

**Headline:**
The Real-Time Telecom-Banking Security Middleware.

**Core Philosophy:**
SafePay MENA bridges the fraud gap between banking rails and telecom operator networks before money leaves an account.

**The Three Shields:**
1. **Silent Carrier Possession (Number Verification API):** Verifies the active cellular connection against the registered SIM in 300ms without sending any SMS code to the screen.
2. **Active Call Detection (Scam Signal API):** Queries the mobile core to detect if the sender is currently engaged in an active phone call during a transfer, neutralizing vishing coercion.
3. **Account Takeover Defense (SIM Swap & Device Swap APIs):** Instantly blocks transactions originating from SIM cards swapped within 24 to 240 hours.

**Visual Layout:**
Visual schematic showing Bank Rails on the left, SafePay AI Middleware in the center, and GSMA CAMARA Network Core on the right.

**Speaker Notes:**
SafePay MENA is the bridge between the banking world and the telecom world.
Instead of sending an SMS code that can be read over the phone, SafePay queries the telecom network directly over the cellular bearer.
If a customer is making a payment while on an active call with an unknown caller, SafePay flags the transaction instantly.
And if the SIM card was swapped two hours ago, the payment is hard-blocked before a single piastre or halala leaves the account.

---

## Slide 6: THE DUAL-ENGINE ARCHITECTURE

**Headline:**
Engineered for Sub-10ms Latency and Enterprise Reliability.

**Why Dual-Engine?**
Payment networks cannot tolerate multi-second LLM inference delays on the critical path.
SafePay decouples deterministic authorization from regulatory trace generation:

```
                  ┌────────────────────────────────────────┐
                  │ 1. DETERMINISTIC RISK MATRIX (<10ms)  │
                  │ • Google libphonenumber E.164 parsing  │
TRANSACTION ─────►│ • Multi-signal combinatorial formula   │─────► FAST PATH: APPROVE / BLOCK
                  │ • SAMA 20k SAR & CBE 70k EGP limits    │       (Benchmark: 0.0024ms)
                  └──────────────────┬─────────────────────┘
                                     │ Async Metadata
                                     ▼
                  ┌────────────────────────────────────────┐
                  │ 2. GEMINI 2.0 FLASH AGENT (<500ms)     │
                  │ • Natural language explainability      │─────► AUDIT PATH: SAMA / CBUAE TRACE
                  │ • Regulatory citation and audit log    │       (Stored in Supabase)
                  └────────────────────────────────────────┘
```

**Key Performance Metrics:**
- **Risk Engine Benchmark:** 0.0024 ms per evaluation (>400,000 evaluations per second).
- **Circuit Breaker SLA:** 250 ms timeout guarantee.
- **In-Memory Cache:** 15-minute TTL on SIM swap queries to prevent redundant carrier API charges.

**Speaker Notes:**
Many developers make the fatal mistake of putting an LLM directly in the synchronous payment flow.
In instant payments, you cannot wait two seconds for an LLM to generate tokens while funds hang in limbo.
SafePay solves this through a dual-engine design.
Our mathematical risk engine evaluates carrier signals deterministically in under 10 milliseconds.
Our unit test benchmarks prove it runs in 0.0024 milliseconds per transaction.
Simultaneously, Google Gemini 2.0 Flash generates an explainable compliance trace in the background for banking regulators.

---

## Slide 7: STANDARDIZED GSMA CAMARA NETWORK APIS

**Headline:**
Powered by Nokia Network as Code and Global Open Gateway Standards.

| CAMARA API | Protocol Type | Telecom Provider | Role in SafePay MENA |
|---|---|---|---|
| **Number Verification** | 3-Legged OAuth (Cellular Bearer) | stc, e&, Vodafone | Silently authenticates the SIM on the data session in 300ms. Replaces SMS OTPs completely. |
| **SIM Swap Check** | 2-Legged Server-to-Server | stc, e&, Vodafone | Queries carrier HLR/HSS for SIM replacements within the last 24 to 240 hours. |
| **Scam Signal** | 2-Legged Server-to-Server | stc, e& | Checks real-time voice call status to intercept active vishing and phone scam coercion. |
| **Device Status & Roaming** | 2-Legged Server-to-Server | stc, e& | Detects international roaming anomalies and unreachable handsets. |

**Zero PII Exchange:**
SafePay never transmits bank account numbers, customer names, or balances to the carrier.
The gateway exchanges only cryptographic hashes, MSISDN identifiers, and boolean verification flags.

**Speaker Notes:**
We utilize four official GSMA CAMARA APIs through the Nokia Network as Code platform.
Number Verification is 3-legged; it verifies the data connection itself, making SIM impersonation impossible.
SIM Swap, Scam Signal, and Device Status are 2-legged server-to-server calls that run concurrently.
Crucially, our architecture respects strict zero-PII privacy standards.
The telecom operator never sees bank account balances, payee names, or financial history.

---

## Slide 8: THREE LIVE DEMONSTRATION SCENARIOS

**Headline:**
Live Interactive Simulation Across Everyday MENA Use Cases.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ SCENARIO 1: CLEAN INSTANT TRANSFER (InstaPay Egypt)                             │
│ • Transfer: 200 EGP to saved contact (Mother)                                    │
│ • Network Signals: Number Verified=True, SIM Swapped=False, Active Call=False   │
│ • Outcome: Score 8/100 -> Instant Silent APPROVE in 200ms                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│ SCENARIO 2: VISHING & SOCIAL ENGINEERING SCAM (Sarie KSA)                       │
│ • Transfer: 15,000 SAR to unknown payee at 3:00 AM while on active voice call    │
│ • Network Signals: Scam Signal=ACTIVE_CALL, Number Verified=True                 │
│ • Outcome: Score 52/100 -> STEP-UP Biometric Challenge with Anti-Coercion Banner │
├─────────────────────────────────────────────────────────────────────────────────┤
│ SCENARIO 3: SIM SWAP ACCOUNT TAKEOVER ATTACK (stc pay / Aani)                   │
│ • Transfer: 35,000 SAR to unknown mule account                                  │
│ • Network Signals: SIM Swapped 2.1h ago, Device Match=FAIL                       │
│ • Outcome: Score 94/100 -> Immediate HARD BLOCK + Gemini Compliance Trace       │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Speaker Notes:**
In our live prototype, we demonstrate three distinct real-world flows.
Scenario 1 is an everyday 200 EGP transfer on InstaPay.
Carrier verification passes silently, and the payment clears in 200ms with zero SMS OTP friction.
Scenario 2 simulates a scam call where a victim is being coerced into sending 15,000 SAR.
SafePay detects the active phone call via Scam Signal and interrupts the coercion with a biometric challenge and warning modal.
Scenario 3 is a hostile SIM swap takeover attempting to drain 35,000 SAR; SafePay instantly freezes the transfer.

---

## Slide 9: REAL-TIME AUDIT TRACES & COMPLIANCE SHIELD

**Headline:**
Gemini 2.0 Flash Turns Raw Telemetry into Regulatory Protection.

**Example Compliance Output for Scenario 3:**
> **Regulatory Trace:** `SAMA-AML-2023-SEC4.2` & `CBUAE-NOTICE-2025-3057`
> **Primary Vector:** `SIM_SWAP_ACCOUNT_TAKEOVER`
> **Risk Score:** `94 / 100` (Tier 3 Critical Block)
> **AI Explainability Log:**
> *"Transaction of 35,000 SAR blocked. SAMA Sarie 20k threshold exceeded without secondary factor.*
> *Telecom intelligence confirms physical SIM card was reissued 2.1 hours ago on carrier stc Saudi.*
> *Hardware IMEI check returned device mismatch.*
> *Automated block shields financial institution from 100% reimbursement liability under CBUAE Notice 2025/3057."*

**Why Banks Care:**
Central banks require auditability for all automated blocks.
SafePay provides instant, court-admissible evidence that the transaction was intercepted due to verified carrier compromise.

**Speaker Notes:**
When a bank blocks a high-value transfer, it must be able to justify that action to customers and regulators.
Our Gemini 2.0 Flash agent produces detailed, auditable records citing specific SAMA and CBUAE regulatory controls.
If a customer calls customer service or files a complaint, the bank has immediate, plain-language proof of the SIM swap and device mismatch.
This shields the financial institution from fines and protects customer relationships.

---

## Slide 10: BUSINESS MODEL & UNIT ECONOMICS

**Headline:**
High-Margin Monetization for Telecoms and Massive ROI for Banks.

**1. The Cost of Doing Nothing:**
- Financial institutions lose **AED 4.99 per AED 1 stolen** in operational recovery costs.
- Banks pay **$0.03 to $0.05 per SMS OTP** regardless of whether the transaction succeeds.

**2. The SafePay Unit Economics:**
- **Metered Carrier Cost:** $0.07 per CAMARA API bundle query (paid to stc, e&, or Vodafone).
- **SafePay Transaction Fee:** $0.20 per evaluated transaction (billed to the bank).
- **Gross Margin:** **65%** for SafePay middleware.
- **Telecom Benefit:** Converts passive 5G infrastructure into recurring, high-margin software revenue.

**3. Bank Cost-Benefit Analysis (Tier-1 Bank Processing 5M Monthly Transfers):**
- SafePay Annual Cost: $1.2 million.
- Estimated Fraud Losses Prevented: $8.5 million.
- SMS OTP Infrastructure Savings: $1.8 million.
- **Net Bank ROI:** **693% in Year 1**.

**Speaker Notes:**
SafePay aligns the commercial incentives of both banks and telecom operators.
Telecoms have invested billions into 5G networks; SafePay gives them a recurring revenue stream by monetizing Open Gateway queries at $0.07 each.
Banks pay SafePay $0.20 per high-risk evaluation.
When you consider that banks save $0.04 on SMS OTPs and avoid losing five times the fraud volume, the ROI is an astonishing 693%.
This is an easy commercial sell to any chief risk officer in the GCC.

---

## Slide 11: COMPETITIVE ADVANTAGE & MOAT

**Headline:**
Why SafePay MENA Wins Against Incumbents.

| Feature | Legacy Bank Fraud Engines (FICO, SAS) | Individual Telco Portals (stc, e& alone) | SafePay MENA Middleware |
|---|---|---|---|
| **Data Scope** | Internal bank transactions only (blind to SIM state) | Single-carrier records only (no cross-border roaming) | Unified cross-carrier MENA intelligence (+20, +966, +971) |
| **Vishing Defense** | Zero visibility into active phone calls | Raw API output without fraud reasoning | Real-time Scam Signal + Biometric Anti-Coercion modal |
| **Authentication** | Vulnerable SMS OTPs | Basic Number Verification endpoint | Seamless 300ms silent cellular bearer authentication |
| **Regulatory Fit** | Generic global rules | Raw technical specs | Built specifically for SAMA 2026 & CBUAE Notice 2025/3057 |
| **Decision Speed** | Batch / Post-settlement | N/A (Data provider only) | **Sub-10ms deterministic matrix (0.0024ms actual)** |

**Speaker Notes:**
Legacy fraud systems like FICO and SAS are blind to telecom data; they only analyze past transactions.
Individual telcos have APIs, but a Saudi bank cannot integrate separately with Vodafone Egypt, stc, Mobily, and e& UAE.
SafePay acts as the unified regional aggregator.
We normalize regional phone numbers, orchestrate multiple carrier APIs, and execute decisions in microseconds.
Nobody else offers this combined pre-auth middleware tailored to MENA regulations.

---

## Slide 12: TRACTION, VALIDATION & MENTORSHIP

**Headline:**
Validated by stc Leadership and 299 Empirical Industry Sources.

**Key Milestones Achieved:**
- **Top 80 Hackathon Shortlist:** Selected from hundreds of regional applicants for Phase 2.
- **stc Mentorship Completed:** Deep technical alignment session conducted with Eng. Abdullah A. Alkaoud (stc Open Gateway Lead).
- **Empirical Research Database:** Synthesized 299 sources spanning SAMA regulatory guidelines, CBE payment rules, and GSMA pilot metrics.
- **Working Prototype Running:** Full FastAPI backend, live WebSocket feed, responsive phone simulator, and passing test suite.

**Key Mentorship Pivot:**
Based on mentor feedback, we prioritized active vishing call detection over simple SIM swap checks, directly addressing the true 85% scam volume on instant rails.

**Speaker Notes:**
SafePay MENA is not an abstract concept; it is a fully functioning, research-backed system.
We completed a comprehensive mentorship session with Eng. Abdullah from stc, validating our architecture against carrier production constraints.
We synthesized 299 research sources into our technical specifications.
And our live prototype is running right now, handling real-time simulated transactions across Egypt, Saudi Arabia, and the UAE.

---

## Slide 13: REGULATORY COMPLIANCE & PRIVACY ROADMAP

**Headline:**
Zero PII Exposure, SAMA Cybersecurity Compliance, and ISO 27001 Readiness.

**Privacy-First Design Principles:**
1. **No Financial Data to Telcos:** Carrier APIs only receive E.164 phone numbers and timestamp parameters.
2. **Ephemeral Caching:** SIM swap records are cached in memory for 15 minutes and automatically flushed.
3. **Immutable Supabase Audit Trail:** Every decision hash is recorded with cryptographic timestamps for central bank inspections.
4. **Local Data Residency:** Dockerized architecture ready for deployment within Saudi Arabia (stc Cloud / Oracle Cloud Riyadh) and Egypt.

**Regulatory Alignment Matrix:**
- **Saudi Arabia:** SAMA Cybersecurity Framework (4 domains, 96 controls) & CST SIM ownership regulations.
- **United Arab Emirates:** CBUAE Notice 2025/3057 (Liability Shift & OTP Elimination).
- **Egypt:** Central Bank of Egypt IPN / InstaPay Transaction Security Rules.

**Speaker Notes:**
Security and data sovereignty are paramount in financial services.
SafePay is architected with strict zero-knowledge principles.
We never expose bank account numbers, balances, or recipient identities to telecom operators.
Our solution is designed to deploy within local sovereign cloud environments to comply with SAMA data residency requirements.
Every automated block is cryptographically logged for effortless central bank audits.

---

## Slide 14: COMMERCIAL GO-TO-MARKET STRATEGY

**Headline:**
Phased Expansion Across National Switches, Digital Banks, and Wallets.

```
PHASE 1: PILOT (Months 1 - 4)          PHASE 2: COMMERCIAL (Months 5 - 12)    PHASE 3: SCALE (Year 2+)
──────────────────────────────────     ───────────────────────────────────    ───────────────────────────────
• Sandboxed pilot with stc & 1 bank    • Commercial launch on Sarie & Aani    • Integrate with InstaPay Egypt
• Pre-auth check for transfers >10k    • Onboard 5 top GCC retail banks       • Expand to Jordan, Qatar & Oman
• Focus on high-risk vishing vectors   • Target online 3DS e-commerce checkouts• Enterprise telco revenue share
```

**Target Customer Segments:**
1. **National Payment Switches:** Saudi Payments (Sarie), Al Etihad Payments (Aani), EBC (InstaPay).
2. **Digital Challenger Banks:** STC Bank, D360, Wio Bank, Liv.
3. **Large Retail Commercial Banks:** Al Rajhi, SNB, CIB Egypt, Emirates NBD.

**Speaker Notes:**
Our go-to-market begins with sandboxed pilots alongside stc and forward-thinking digital banks like STC Bank.
In Phase 2, we expand commercially across Saudi Arabia and the UAE to capture high-value transfers and 3DS e-commerce checkouts before the March 2026 CBUAE deadline.
In Phase 3, we scale into Egypt's massive 1.5-billion transaction market and expand across the broader Arab region.
Our revenue model is purely usage-based, making adoption frictionless for banking partners.

---

## Slide 15: CONCLUSION & CALL TO ACTION

**SafePay MENA**
*Protecting MENA's Instant Payment Revolution*

> "The telecom networks have the intelligence.
> The payment rails have the urgency.
> Central banks have set the deadline: March 31, 2026.
> SafePay MENA is the bridge that unites them."

**Developer:** Karim Mohamed Abdelnabi  
**Hackathon:** GSMA MENA Ignite Hackathon (Phase 2)  
**Live Demo:** `http://127.0.0.1:8000` (FastAPI + Next.js Simulation Dashboard)  
**Codebase:** Production-grade Python 3.11+, Nokia NaC SDK, Gemini 2.0 Flash  

**Speaker Notes:**
The technology exists today.
The market is demanding it.
And central bank regulations have made it mandatory.
SafePay MENA stops fraud before money moves, protects consumers from devastating losses, and turns telecom networks into the security backbone of modern digital finance.
Thank you, and I look forward to your questions.
