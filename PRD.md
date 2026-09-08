# Product Requirements Document (PRD)

# Project: SafePay MENA
## Real-Time AI Telecom Fraud Shield for Instant Payments

---

## Problem Statement

Digital payments across the Middle East and North Africa (MENA) have expanded at an unprecedented pace.
Egypt's InstaPay processed 1.5 billion transactions worth EGP 2.9 trillion in 2024 alone.
Saudi Arabia's Sarie and the UAE's Aani process tens of thousands of instant push payments every day.
However, this instant payment revolution has exposed a critical structural vulnerability: instant transfers are immediate and irreversible.
Once a fraudulent transaction is authorized, the funds leave the account in under three seconds, leaving zero window for traditional post-clearing fraud analysis.

At the same time, regional fraud syndicates have weaponized this settlement velocity across two primary attack vectors:

### Vector 1: Spam Calls, Vishing, and Active Social Engineering Coercion
Over 85% of successful digital payment fraud across Saudi Arabia, the UAE, and Egypt stems from social engineering, vishing (fraudulent phone calls), and One-Time Password (OTP) interception.
Fraudsters actively call victims while impersonating bank fraud departments, law enforcement, or national portals (such as Sadad, Musaned, or Ejar in Saudi Arabia).
Using psychological pressure and urgency ("Your account is suspended, transfer your balance to this protected custody account immediately"), fraudsters keep victims on the phone for 15 to 30 minutes while guiding them step-by-step through an instant transfer.
Because the payment is "authorized" by the victim themselves (Authorized Push Payment - APP fraud), traditional bank rule engines approve it as legitimate traffic.

### Vector 2: Online Card Leakage & E-Commerce Card-Not-Present (CNP) Fraud
Millions of debit and credit card credentials leak annually through compromised online merchant databases, dark web syndicates, and credential-stuffing attacks.
When fraudsters obtain leaked card details (PAN, CVV, expiry date), they initiate high-velocity online purchases or wallet top-ups.
Currently, banks attempt to protect e-commerce checkouts using 3D Secure (3DS) SMS OTPs.
However, if the fraudster has compromised the user's phone via malware or a SIM swap, or if the fraudster tricks the user into disclosing the 3DS code over the phone, the stolen card is drained instantly.

Banks and national switches operate completely blind to cellular network state.
Banks can observe IP addresses and device fingerprints, but they cannot tell whether a customer's SIM card was replaced two hours ago, whether the user is currently on an active scam phone call while draining their life savings, or whether an online card purchase is originating from a rogue device that does not possess the cardholder's cellular connection.
This blind spot has triggered an urgent regulatory reaction.
The Central Bank of the UAE (CBUAE) issued Notice 2025/3057, mandating the complete retirement of SMS and email OTPs for high-value transactions by March 31, 2026.
Crucially, CBUAE enacted a structural liability shift: if a customer falls victim to fraud where an SMS OTP was utilized, the financial institution is held 100% financially liable and must immediately reimburse the victim.
Similarly, the Saudi Central Bank (SAMA) and the Central Bank of Egypt (CBE) are strictly enforcing transaction limits and requiring real-time, explainable fraud prevention mechanisms.
Financial institutions urgently require an intelligent middleware that bridges the telecom-banking divide in real time before payments are committed to instant rails.

---

## Solution

SafePay MENA is an AI-orchestrated telecom-banking security middleware that stops instant payment fraud before money moves.
It integrates banking payment rails (InstaPay Egypt, Sarie / STC Bank Saudi Arabia, and Aani UAE) with telecom operator intelligence (stc, e&, Vodafone) via standardized GSMA Open Gateway / CAMARA network APIs.

### 1. How SafePay Solves Spam Calls & Vishing (Coercion Defense)
SafePay dismantles phone scams at the network layer through a 3-part shield:
- **Active Call Detection (Scam Signal API):** When a transfer is initiated, SafePay queries the carrier mobile core in real time. If the customer's phone is engaged in an active, unverified voice call, SafePay immediately raises the transaction risk score.
- **Eliminating the OTP Attack Surface (Number Verification API):** Scammers on the phone rely on asking victims: "Read me the 6-digit code sent to your phone." SafePay completely replaces SMS OTPs with silent cellular bearer authentication. Because no code is ever generated or displayed on the handset, the scammer has literally nothing to steal.
- **Biometric Anti-Coercion Interruption:** If a transfer is attempted during an active call, SafePay forces an on-device biometric challenge (Face ID) accompanied by a mandatory anti-coercion modal: *"Warning: You are currently on an active phone call. Legitimate banks and government agencies will NEVER instruct you to transfer money to another account."* This breaks the fraudster's psychological hold on the victim.

### 2. How SafePay Solves Online Card Leakage & CNP E-Commerce Fraud
SafePay neutralizes stolen card data before online checkout settles:
- **Silent Cellular Possession Verification:** When an online transaction or digital wallet top-up is attempted using a credit/debit card, SafePay triggers a 3-legged Number Verification check against the mobile network. If the checkout session originates from a scammer's computer or rogue phone, the mobile network confirms that the device does not possess the registered SIM card associated with the cardholder account. The payment is declined instantly, rendering leaked card numbers useless to the attacker.
- **Device Swap & SIM Swap Cross-Check:** If a stolen card is used shortly after a SIM swap or on an unrecognized IMEI hardware identifier, SafePay immediately blocks the transaction, protecting the cardholder even if their CVV and card numbers were exposed in a merchant data breach.

### 3. The Real-Time Evaluation Engine
When a payment or checkout is initiated, SafePay MENA evaluates the transaction through a dual-engine architecture:
First, a deterministic mathematical risk matrix executes in under 10 milliseconds.
It ingests real-time cellular signals directly from carrier registries:
1. Number Verification: Silently authenticates the customer's active cellular data connection directly against the registered SIM without transmitting any readable SMS code to the screen.
2. SIM Swap Verification: Queries carrier registries to determine if the SIM card was swapped within the prior 24 to 240 hours.
3. Scam Signal: Checks whether the device is currently engaged in an active, unverified voice call, directly intercepting vishing and social engineering coercion in real time.
4. Device Status: Detects unexpected international roaming anomalies and unreachable handsets.

Second, SafePay MENA enforces a friction-optimized 3-tier outcome architecture:
- Tier 1 (Happy Flow - Score < 25): Silent approval in under 200ms with zero user friction, completely replacing vulnerable SMS OTPs.
- Tier 2 (Flagged Flow - Score 25 to 69): Triggered by roaming or unverified active calls; prompts an instant 1-second on-device biometric challenge (Face ID or FIDO2 passkey) to break fraudster coercion.
- Tier 3 (Block-It-Now Flow - Score >= 70): Triggered by recent SIM swaps, rogue devices, or known syndicate mule patterns; immediately freezes the transaction and generates an auditable, explainable compliance trace.

Third, an asynchronous AI agent powered by Google Gemini 2.0 Flash ingests the decision metadata to produce natural-language, regulatory-compliant audit traces mapped directly to SAMA Counter-Fraud controls and CBUAE Notice 2025/3057 requirements.
This eliminates bank liability, protects customers from devastating losses, and preserves sub-second payment performance.

---

## User Stories

1. As a retail banking customer, I want my routine instant transfers to approve in under 200 milliseconds without waiting for an SMS OTP, so that I enjoy a seamless and fast payment experience.
2. As a retail banking customer, I want my bank to verify my identity silently over my cellular connection, so that fraudsters cannot intercept or steal my verification codes.
3. As a bank fraud operations officer, I want incoming instant transfers to be cross-checked against telecom SIM swap records, so that account takeover attacks using stolen numbers are blocked before funds settle.
4. As a bank compliance director, I want all blocked transactions to generate explainable audit records referencing specific SAMA and CBUAE regulatory guidelines, so that the bank satisfies regulatory reporting requirements.
5. As a bank risk manager, I want the system to detect if a customer is executing a transfer while on an active voice call, so that social engineering vishing attacks can be flagged before completion.
6. As a customer experiencing a phone call scam, I want my banking app to prompt a biometric face scan when an anomaly is detected, so that the scammer on the phone cannot force me to complete the unauthorized transfer.
7. As a corporate payments controller in Saudi Arabia, I want transactions exceeding 20,000 SAR to be checked against high-security telecom and device parameters, so that large corporate accounts are protected from business email compromise.
8. As an IT architect at a national payment switch, I want the risk decision engine to execute deterministically in under 10 milliseconds, so that overall payment rail latency remains well within regional SLAs.
9. As a mobile wallet developer, I want a single unified REST API endpoint to evaluate transaction safety across multiple telecom operators (stc, e&, Vodafone), so that I do not have to write custom integrations for each carrier.
10. As a security operations analyst, I want to view a real-time visual dashboard showing live transactions, risk gauge scores, and telecom signal breakdowns, so that I can monitor active threats across the network.
11. As a bank customer traveling abroad, I want my payments to trigger an intuitive biometric step-up rather than being outright declined, so that I am not stranded without access to my money.
12. As a bank executive, I want our payment infrastructure to comply with CBUAE Notice 2025/3057 before the March 31, 2026 deadline, so that our institution avoids 100% liability for customer fraud losses.
13. As a telecom operator product manager, I want our CAMARA Open Gateway APIs to be consumed by financial institutions, so that we monetize our network data assets through sustainable API call revenue.
14. As an auditor reviewing financial fraud incidents, I want an immutable, tamper-evident record of all telecom signals queried and risk weights applied, so that investigations have complete evidentiary integrity.
15. As an engineer evaluating the platform, I want a deterministic mock telecom provider mode, so that I can reliably test edge cases and attack scenarios without relying on physical cellular hardware.
16. As an anti-fraud team lead, I want configurable risk thresholds and weights, so that risk appetites can be adjusted dynamically during peak fraud seasons such as Ramadan or Black Friday.
17. As a mobile banking customer, I want my personally identifiable information (PII) to remain completely confidential, so that telecom providers never receive my bank account numbers or financial balances.
18. As an instant payment operator, I want automated circuit breakers that fall back gracefully if carrier networks experience latency, so that payment processing never hangs or crashes.
19. As a hackathon judge, I want to test three distinct preset scenarios with a single click, so that I can verify clean approvals, step-up challenges, and hard blocks in real time.
20. As a hackathon judge, I want to inspect the AI agent's natural-language reasoning trace, so that I can verify that decisions are explainable and grounded in regional regulations.
21. As an online cardholder whose card details were leaked in an e-commerce merchant breach, I want unauthorized checkout attempts on rogue devices to be declined automatically via silent carrier verification, so that criminals cannot spend my money even if they possess my card number and CVV.
22. As an e-commerce merchant or payment gateway, I want to verify that an online card checkout is authorized by the true SIM holder without introducing SMS OTP drop-offs, so that I eliminate chargeback fraud while maintaining high conversion rates.

---

## Implementation Decisions

### Architectural Topology
SafePay MENA operates as a zero-trust security middleware situated between payment initiation channels and instant payment settlement rails.
The platform is organized into three distinct execution tiers:
1. Edge Pre-Screening: Receives payment intent, normalizes phone numbers to standard E.164 formats, and checks local in-memory caches.
2. Deterministic Risk Engine: Executes sub-10ms multi-variable matrix scoring combining transaction context and real-time CAMARA telecom signals.
3. Asynchronous AI Audit Engine: Employs Google Gemini 2.0 Flash to convert raw decision vectors into structured, human-readable compliance audit records without blocking the financial authorization path.

### Core Modules and Interfaces

#### Module 1: Telecom Signal Gateway (Deep Module)
Encapsulates all communication with mobile network operators via GSMA Open Gateway / CAMARA standards.
Provides a unified, clean interface that hides the complexity of token management, OAuth 2-legged and 3-legged handshakes, and carrier routing.
Includes a fully deterministic simulation adapter alongside the production Nokia Network-as-Code client.
Exposes methods for Number Verification, SIM Swap verification, Scam Signal checking, and Device Status inspection.
Standardizes all phone numbers into international E.164 format (+966 for Saudi Arabia, +20 for Egypt, +971 for UAE) before dispatching network requests.

#### Module 2: Combinatorial Risk & Decision Engine (Deep Module)
Implements a non-linear scoring matrix that evaluates both banking variables (amount, recipient history, velocity, time of day) and telecom signals (carrier match, swap age, active call state, roaming country).
Produces a normalized risk score between 0 and 100 alongside an authoritative decision enum: APPROVE, STEP_UP, or BLOCK.
Enforces statutory constraints, including SAMA 20,000 SAR high-value transfer safeguards and CBUAE OTP liability rules.
Executes entirely in memory with zero external I/O dependencies during the critical path to guarantee sub-10ms processing latency.

#### Module 3: AI Compliance & Explainability Agent (Deep Module)
Runs asynchronously alongside or immediately following the deterministic decision.
Ingests the complete signal vector and decision rationale.
Utilizes Gemini 2.0 Flash to synthesize structured audit records mapped to SAMA Cybersecurity Framework domains and CBUAE Notice 2025/3057 mandates.
Formats outputs into structured JSON logs containing plain-language summaries, regulatory citations, and recommended security operations actions.

#### Module 4: API Gateway & Orchestration Core
Built with FastAPI to support high-concurrency asynchronous request handling.
Exposes REST endpoints for payment evaluation, step-up verification confirmation, and health monitoring.
Maintains a WebSocket broadcaster that streams live transaction evaluations, risk breakdown graphs, and AI audit logs to connected client dashboards.
Implements a circuit-breaker pattern: if an external telecom carrier endpoint exceeds 250ms or returns an error, the system falls back to secondary banking risk factors without stalling the payment flow.

#### Module 5: Interactive Simulation UI & SOC Dashboard
Built as a responsive web application providing a dual-screen visualization:
- Left Panel: Mobile Banking Simulation mimicking an instant payment wallet (InstaPay/Sarie/Aani style) with sender profiles, recipient inputs, transfer amounts, and one-click preset attack buttons.
- Right Panel: Security Operations Center (SOC) view featuring an animated 0-100 Risk Gauge, dynamic CAMARA signal badges, and a streaming terminal showing the real-time AI reasoning trace.
Provides full interactive step-up simulation, displaying an on-device biometric modal when a transaction is flagged.

### Zero PII Exposure Standard
No bank account numbers, IBANs, customer account balances, or transaction memos are ever sent to telecom carrier endpoints.
Telecom APIs are queried exclusively with E.164 phone numbers, IP addresses, and time window parameters.
Telecom responses are restricted to booleans, timestamps, and country codes, ensuring strict compliance with Saudi Personal Data Protection Law (PDPL) and UAE Data Protection laws.

---

## Testing Decisions

### Definition of a Good Test
Tests must evaluate external behavior, contracts, and decision accuracy rather than internal implementation details.
A test should verify that given a specific combination of transaction parameters and telecom signals, the engine reliably returns the correct decision tier, risk score boundary, and standardized error codes.
Tests should execute rapidly and deterministically without requiring live third-party telecom connections.

### Modules to be Tested

1. Deterministic Risk Engine:
   - Verify that clean transactions with valid Number Verification and no SIM swap always yield an APPROVE decision with score < 25.
   - Verify that a SIM swap within 24 hours immediately forces a BLOCK decision with score >= 70 regardless of transaction amount.
   - Verify that an active phone call (Scam Signal positive) during an instant transfer triggers a STEP_UP decision with score between 25 and 69.
   - Verify that cross-border roaming anomalies properly increment risk weights without automatically blocking clean users.
   - Verify that the engine computes decisions in under 15 milliseconds under simulated high concurrency.

2. Telecom Signal Gateway & Mock Adapter:
   - Verify that E.164 normalization correctly formats local Egyptian (01x...), Saudi (05x...), and UAE (05x...) numbers.
   - Verify that the mock adapter accurately replicates CAMARA JSON response contracts for all four supported APIs.
   - Verify that circuit breakers trigger gracefully upon simulated telecom timeout.

3. End-to-End API Pipeline:
   - Verify that POST /api/v1/transfer/evaluate accepts valid transfer payloads and returns correct decision schemas.
   - Verify that the WebSocket broadcaster pushes real-time event payloads matching the UI schema.
   - Verify that the biometric step-up endpoint successfully validates simulated face authentication and upgrades transaction state from STEP_UP to APPROVED.

### Prior Art in Codebase
The repository contains standalone verification scripts and ReportLab builders demonstrating structured data generation.
Unit and integration tests will utilize `pytest` and `httpx` async test clients following standard FastAPI testing practices.

---

## Out of Scope

1. Direct integration with live SAMA Sarie or CBE InstaPay production core banking rails (mocked via standard ISO 20022 / REST payment payloads).
2. Live telecommunications carrier production billing integration (monetization modeled on documented $0.50/call industry benchmarks).
3. Physical hardware SIM reprogramming or live cellular tower hardware interception.
4. Long-term multi-year cold storage archiving systems for audit logs (mocked via local storage and Supabase schema definitions).
5. Native iOS / Android Swift or Kotlin application builds (demonstrated via responsive high-fidelity web simulator).

---

## Further Notes

### Key Operational Benchmarks to Demonstrate in Hackathon Deliverables:
- Latency SLA: Sub-200ms end-to-end response for Tier 1 clean payments.
- Evaluation Speed: Sub-10ms deterministic matrix computation before trace generation.
- Economic Impact: Articulation of the AED 4.99 fraud cost multiplier and how SafePay delivers an estimated 44% reduction in scam losses and 55% reduction in false-positive declines.
- Regulatory Compliance: Direct references to CBUAE Notice 2025/3057 (March 2026 OTP retirement) and SAMA Electronic Banking Supervision Rules.
