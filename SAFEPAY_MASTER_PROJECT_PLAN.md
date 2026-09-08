# SafePay MENA - Master Project & Execution Plan

**Theme 4: Secure FinTech, Payments & Anti-Fraud Innovation**  
**GSMA MENA Ignite Hackathon - Phase 2 Final Blueprint**  
**Team Lead & Solo Developer:** Karim Mohamed Abdelnabi  

---

## 1. Executive Summary & Vision

SafePay MENA is an AI-orchestrated telecom-banking security middleware.  
It bridges the critical intelligence gap between mobile network operators and instant payment systems (InstaPay, stc pay, Aani).  
By leveraging standardized GSMA CAMARA network APIs and Gemini 2.0 Flash reasoning, SafePay stops SIM swap fraud, account takeovers, and social engineering in real-time before unauthorized money leaves an account.  

### Core Value Proposition & ROI:
- **For Banks & FinTechs:** Reduces fraud losses by over 45%, eliminates expensive SMS OTP delivery costs, and provides an auditable compliance trace for central banks (SAMA, CBE).  
- **For Telecom Operators (stc, Vodafone, e&):** Monetizes 5G network intelligence through high-margin Open Gateway API subscriptions.  
- **For Consumers:** Invisible, frictionless, 300ms verification without interceptable SMS codes.  

---

## 2. System Architecture & Technical Stack

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             SAFEPAY MENA ARCHITECTURE                       │
│                                                                             │
│  ┌───────────────────────────────┐     ┌─────────────────────────────────┐  │
│  │ FRONTEND: Next.js Dashboard   │     │ PAYMENT SIMULATOR (Demo UI)     │  │
│  │ • Live Risk Gauge (0-100)     │     │ • Mobile Wallet Interface       │  │
│  │ • Real-time AI Reasoning Log  │◄────┤ • Instant Transfer Flow         │  │
│  │ • CAMARA Signal Breakdown     │ WS  │ • Step-Up Biometric Modal       │  │
│  │ • Live Transaction Feed       │     │ • SIM Swap Attack Simulator     │  │
│  └───────────────▲───────────────┘     └────────────────▲────────────────┘  │
│                  │                                      │                   │
│                  └──────────────────┬───────────────────┘                   │
│                                     │ REST / WebSocket                      │
│                                     ▼                                       │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │ BACKEND GATEWAY: FastAPI (Python 3.11+)                               │  │
│  │ • In-Memory Cache (Redis / TTL 15m)                                   │  │
│  │ • Circuit Breaker & Fallback Engine                                   │  │
│  │ • Asynchronous Event Dispatcher (Background Worker)                   │  │
│  └──────────────────────────────────┬────────────────────────────────────┘  │
│                                     │                                       │
│         ┌───────────────────────────┴───────────────────────────┐           │
│         ▼                                                       ▼           │
│  ┌───────────────────────────────┐     ┌─────────────────────────────────┐  │
│  │ AI REASONING & RISK ENGINE    │     │ CAMARA NETWORK API CLIENT       │  │
│  │ • Gemini 2.0 Flash Agent      │     │ • Nokia Network-as-Code SDK     │  │
│  │ • Multi-Signal Risk Scoring   │     │ • SIM Swap API (v0)             │  │
│  │ • Natural Language Audit Log  │     │ • Number Verification API (v0)  │  │
│  │ • Velocity & Anomaly Scorer   │     │ • Device Status & Roaming (v0)  │  │
│  └───────────────┬───────────────┘     │ • Device Swap API (v0)          │  │
│                  │                     └────────────────┬────────────────┘  │
│                  ▼                                      ▼                   │
│  ┌───────────────────────────────┐     ┌─────────────────────────────────┐  │
│  │ SUPABASE (PostgreSQL)         │     │ TELECOM SANDBOX / MOCK LAYER    │  │
│  │ • Immutable Audit Logs        │     │ • Nokia NaC Live Sandbox        │  │
│  │ • User Device Profiles        │     │ • Offline Deterministic Mock    │  │
│  │ • Transaction History         │     │ • Fault-Injection Generator     │  │
│  └───────────────────────────────┘     └─────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Complete Technology Stack:
1. **AI Reasoning Layer:** Google Gemini 2.0 Flash + Google ADK / Function Calling for dynamic tool orchestration and regulatory reasoning traces.  
2. **Backend Engine:** FastAPI (Python 3.11+), Pydantic v2 for data validation, AsyncIO for parallel network queries.  
3. **Telecom Layer:** Nokia Network-as-Code Python SDK (`network_as_code`) with fallback mock server for zero-downtime offline demos.  
4. **Database & Audit:** Supabase (PostgreSQL) with Row-Level Security for tamper-proof audit trails.  
5. **Caching & Resilience:** Redis (or in-memory TTL store) + Circuit Breaker pattern to ensure sub-250ms latency.  
6. **Frontend UI:** Next.js 14 (App Router), Tailwind CSS, Lucide icons, Framer Motion for live visual feedback, WebSocket for real-time streaming.  

---

## 3. CAMARA API Integration & Risk Scoring Engine

### The 4 Standard CAMARA APIs:
1. **SIM Swap Check (`/sim-swap/v0/check`):**  
   Detects if the subscriber's SIM card was replaced in the last 24 to 48 hours.  
   Weight: **35%**  
2. **Number Verification (`/number-verification/v0/verify`):**  
   Performs silent, carrier-level data session authentication to confirm the device holds the claimed SIM.  
   Weight: **30%**  
3. **Device Status & Roaming (`/device-status/v0/roaming`):**  
   Checks if the handset is reachable and whether it is roaming in an unexpected country.  
   Weight: **15%**  
4. **Device Swap (`/device-swap/v0/check`):**  
   Checks if the SIM was transferred to an unrecognized hardware IMEI.  
   Weight: **10%**  
5. **Contextual Velocity & Recipient History:**  
   Evaluates transaction amount, hour of day, and recipient familiarity.  
   Weight: **10%**  

### The 4-Tier Decision Matrix:
- **Score 0 - 25 (LOW RISK):** `APPROVE`  
  Silent background approval in <100ms. Zero user friction.  
- **Score 26 - 55 (MODERATE RISK / AMBIGUOUS):** `STEP-UP CHALLENGE`  
  Prompts user for Face ID / Biometric verification or temporary 6-hour transfer cooling limit.  
- **Score 56 - 75 (ELEVATED RISK):** `STEP-UP + TELCO NOTIFICATION`  
  Requires multi-factor confirmation and alerts subscriber via registered secondary channel.  
- **Score 76 - 100 (CRITICAL FRAUD):** `BLOCK & LOG`  
  Instant transaction freeze, account security hold, and full compliance log generated.  

---

## 4. The 3 Core Demo Scenarios

The Phase 2 prototype will demonstrate three distinct live flows on a split-screen dashboard:

```
┌────────────────────────────────────────────────────────────────────────────┐
│                             DEMO SHOWCASE FLOWS                            │
├────────────────────────────────────────────────────────────────────────────┤
│ Scenario 1: Clean Everyday Payment                                         │
│ • Transfer: 200 EGP to saved contact                                       │
│ • Signals: SIM Swap=False, Number Verify=True, Roaming=False               │
│ • Outcome: Score 8/100 -> Instant Silent APPROVE (200ms)                  │
├────────────────────────────────────────────────────────────────────────────┤
│ Scenario 2: Active SIM-Swap Account Takeover Attack                        │
│ • Transfer: 35,000 SAR to new mule IBAN at 3:15 AM                         │
│ • Signals: SIM Swap=True (2h ago), Device Swap=True, Number Verify=Fail    │
│ • Outcome: Score 94/100 -> Immediate BLOCK + AI Audit Trace               │
├────────────────────────────────────────────────────────────────────────────┤
│ Scenario 3: Ambiguous Travel / New Phone Upgrade                           │
│ • Transfer: 2,500 EGP while roaming in UAE                                 │
│ • Signals: SIM Swap=False, Roaming=True, Device Swap=True                  │
│ • Outcome: Score 42/100 -> Prompt STEP-UP (Face ID Liveness Scan) -> Pass  │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Execution Roadmap & Timeline (Phase 2 Milestones)

| Phase & Date | Milestone | Key Deliverables |
| :--- | :--- | :--- |
| **Phase A**<br>Aug 31 - Sep 2 | **Mentor Alignment & Outreach** | • Send structured email to Eng. Abdullah Alkaoud (`mentor-contact-removed`).<br>• Conduct 30-min call using structured 4-question script.<br>• Validate STC Open Gateway parameters. |
| **Phase B**<br>Sep 3 - Sep 5 | **Backend & CAMARA Engine** | • FastAPI backend with parallel async API orchestration.<br>• Nokia NaC SDK integration + robust mock fallback server.<br>• Weighted 0-100 risk scoring algorithm.<br>• Supabase database schema for audit trails. |
| **Phase C**<br>Sep 6 - Sep 7 | **AI Reasoning & Agent Layer** | • Gemini 2.0 Flash dynamic tool-calling integration.<br>• Real-time natural language compliance trace generator.<br>• Velocity tracking and caching layer (Redis / in-memory). |
| **Phase D**<br>Sep 8 - Sep 9 | **Frontend Simulation Dashboard** | • Split-screen Next.js dashboard with live mobile wallet simulator.<br>• Animated 0-100 risk gauge and signal breakdown charts.<br>• Interactive scenario switcher (Clean, Attack, Step-Up).<br>• WebSocket event streaming. |
| **Phase E**<br>Sep 10 | **Final Polish & Submission** | • Record high-quality 3-minute E2E video demo.<br>• Polish GitHub repository README with architecture diagrams.<br>• Submit Phase 2 deliverables to HackerEarth before deadline. |

---

## 6. Mentor Session Blueprint (Eng. Abdullah Alkaoud - stc)

### 2.5-Minute Pitch Script:
> "Hello Eng. Abdullah. I am Karim Abdelnabi, solo developer of SafePay MENA.  
> SafePay solves the telecom-banking fraud gap by integrating GSMA CAMARA APIs (SIM Swap, Number Verification, Device Status, Device Swap) with Gemini 2.0 Flash reasoning.  
> It acts as a real-time risk scoring engine for MENA instant payment rails like InstaPay and stc pay.  
> SafePay protects users without friction by using silent carrier verification, while saving banks over $55,000 monthly in fraud and SMS costs.  
> Today, I would value your guidance on CAMARA trigger placement, production latency limits, and Phase 2 judging priorities."

### Top Questions for the Mentor:
1. *Trigger Points:* Does stc recommend placing SIM Swap checks at login/re-enrollment vs. transaction time?  
2. *Latency Budgets:* What is the acceptable end-to-end SLA for CAMARA API calls in commercial banking rails?  
3. *Commercial Packaging:* How does stc prefer to package Open Gateway APIs for financial aggregators?  
4. *Demo Expectations:* What technical depth do judges expect in the final Phase 2 prototype?  

---

## 7. Submission Deliverables Checklist

- [ ] **Working Source Code:** Clean GitHub repository with FastAPI backend, Next.js frontend, and Supabase config.  
- [ ] **CAMARA Integration:** Working Nokia Network-as-Code SDK implementation with deterministic mock fallback.  
- [ ] **AI Reasoning Engine:** Gemini 2.0 Flash agent generating real-time risk explanations.  
- [ ] **Demo Video (3-5 Mins):** Split-screen recording walking through all 3 fraud scenarios.  
- [ ] **Documentation:** Complete architecture diagrams, API specs, and unit economics summary.  
