# SafePay MENA - Idea Capture Template

### MENA Ignite Open Gateway Hackathon - Phase 1 Submission

---

## 1. Submitter Details

| Field               | Details                         |
| ------------------- | ------------------------------- |
| **Team Name**       | SafePay MENA                    |
| **Team Lead**       | Karim Mohamed Abdelnabi         |
| **Contact Email**   | karim.abdelnabi2005@gmail.com   |
| **Contact Phone**   | +201159821098                   |
| **Country**         | Egypt                           |
| **Submission Date** | July 2026                       |

---

## 2. Idea Summary

### 2.1 Problem Statement

The MENA region's digital payment infrastructure is growing faster than the security systems protecting it.

**The scale of the problem:**

- Egypt's InstaPay processed **1.1 billion transactions** in H1 2025, serving 16 million users. All transfers are instant and irreversible.
- UAE's Aani instant payment platform handles 25,000 P2P transfers daily across 12.5 million users.
- Saudi Arabia invested **$469.9 million** in fraud detection in 2025 alone.
- The MENA digital payments market is projected to reach **$275.47 billion by 2026**.

**The attack:** SIM swap fraud is the primary vector. Fraudsters social-engineer telecom staff into transferring a victim's phone number to a new SIM card, then intercept SMS OTP codes to authorize fraudulent bank transfers. Individual losses range from **$270 to $160,000+** per incident. A documented UAE case involved $1.5 million stolen through SIM swap combined with insider collusion. INTERPOL's Operation Ramz (2025-2026) arrested 200+ suspects across 13 MENA countries.

**The root cause:** Banks and telecom operators operate in completely separate data silos. When a SIM swap happens at Vodafone Egypt, no Egyptian bank receives that signal. The telecom network has the intelligence to flag fraud - but that intelligence has never been connected to payment systems in real-time. PwC's 2025 GCC fraud report identified this as the critical "fraud gap."

**The human cost:** 64% of adults in the Arab region (~200 million people) remain unbanked. The #1 barrier to financial inclusion is lack of trust. Every high-profile fraud case pushes millions further from formal financial systems.

### 2.2 Proposed Solution

**SafePay MENA** is an AI-powered fraud detection agent that acts as a real-time security layer between instant payment systems and the mobile network. Before any high-risk payment is authorized, the agent queries the telecom network using GSMA Open Gateway CAMARA APIs to verify the sender's identity and device integrity at the carrier level.

**How it works:**

1. A user initiates a payment via InstaPay, Aani, or stc pay.
2. SafePay's AI agent receives the transaction context (amount, sender phone number, recipient, timestamp).
3. The agent autonomously decides which CAMARA APIs to query based on the risk profile - a low-value transfer to a known contact requires minimal checks, while a high-value transfer to a new recipient at an unusual hour triggers all available checks.
4. The agent queries SIM Swap status, performs silent Number Verification, checks Device Reachability/Roaming status, and detects Device Swaps - all via Nokia Network-as-Code.
5. Signals are aggregated through a weighted risk scoring engine producing a score from 0-100.
6. The agent makes an autonomous decision: APPROVE (silent), request STEP-UP authentication, or BLOCK with an alert.
7. Every decision includes a natural-language reasoning trace for regulatory audit compliance.

**The key differentiator:** SafePay does not call APIs in a fixed pipeline. It is a genuinely agentic system that reasons about which tools to use, weighs multiple signals together, and explains its decisions - the intelligence layer that bridges banks and telecoms.

### 2.3 Expected Benefits

| Stakeholder           | Benefit                                                                                                                                |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **Consumers**         | Transactions protected by carrier-level security without behavior change. Eliminates reliance on interceptable SMS OTPs.               |
| **Banks & Fintechs**  | Access to telecom network fraud signals for the first time. Reduced false positives. Regulatory-compliant audit trail.                 |
| **Telecom Operators** | New API monetization revenue stream. Strengthened financial sector partnerships. Demonstrated Open Gateway ROI.                        |
| **MENA Region**       | Accelerated financial inclusion through increased payment trust. Reduced regional fraud losses. MENA innovation showcase for MWC Doha. |

**Quantified impact from early pilots:** CAMARA API integrations have demonstrated a **44% reduction in scam losses** and **55% fewer false-positive payment declines** in initial global deployments.

---

## 3. Alignment

### 3.1 Challenge Theme

**Theme 4: Secure Fintech, Payments & Anti-Fraud Innovation**

SafePay directly addresses this theme by building the missing security infrastructure for MENA's booming instant payment ecosystem, using CAMARA APIs as the telecom intelligence backbone.

### 3.2 GSMA Pillar Alignment

**Industry Services and Solutions - Open Gateway**

SafePay is a direct implementation of the GSMA Open Gateway vision: standardized, carrier-agnostic network APIs enabling third-party applications (in this case, payment fraud prevention) to leverage telecom network intelligence. It demonstrates the commercial value of Open Gateway by creating a new revenue stream for operators while solving a critical market need.

### 3.3 Regional Context

- **Egypt:** InstaPay is the fastest-growing instant payment system in Africa. Vodafone Cash holds 62.7% mobile wallet market share. Yet fraud infrastructure lags behind adoption.
- **Saudi Arabia:** SAMA's instant payment mandate and Vision 2030 digital economy goals make fraud prevention critical. stc has joined Open Gateway.
- **UAE:** Aani and Jaywan digital identity create a mature digital payments ecosystem, but e&'s CAMARA certification (Aug 2025) is not yet integrated with banking fraud systems.
- **Qatar & GCC:** Ooredoo + Vodafone Qatar deployed Number Verification + SIM Swap APIs. Pan-GCC payment interoperability makes cross-border fraud a growing concern.

---

## 4. API Usage

### Nokia Network-as-Code / CAMARA API Integration

SafePay integrates **4 CAMARA APIs** from the Nokia NaC platform, each serving a distinct role:

| #   | API                     | CAMARA Standard                                    | NaC Endpoint                                                  | Role in SafePay                                                                            | Risk Weight                |
| --- | ----------------------- | -------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | -------------------------- |
| 1   | **SIM Swap**            | sim-swap v0                                        | `POST /sim-swap/v0/check` + `POST /sim-swap/v0/retrieve-date` | Detects if sender's SIM was recently swapped - #1 fraud indicator                          | **35%**                    |
| 2   | **Number Verification** | number-verification v0                             | `POST /number-verification/v0/verify`                         | Silent carrier-level auth - verifies the device IS the registered phone. Replaces SMS OTP. | **30%**                    |
| 3   | **Device Status**       | device-reachability-status + device-roaming-status | `POST /device-status/v0/roaming` + reachability check         | Detects roaming anomalies and unreachable devices during active transactions               | **15%**                    |
| 4   | **Device Swap**         | device-swap v0                                     | `POST /device-swap/v0/check`                                  | Detects if SIM moved to new handset (different IMEI)                                       | Part of 20% context weight |

### API Integration Flow

```
Payment Platform (InstaPay/Aani/stc pay)
    │
    │ POST /api/v1/check-transaction
    │ {amount, sender_phone, recipient, timestamp, channel}
    │
    ▼
SafePay Backend (FastAPI)
    │
    │ Fetch sender profile from Supabase
    │ Pass context to AI Agent
    │
    ▼
SafePay AI Agent (Google ADK + Gemini 2.0 Flash)
    │
    │ Agent REASONS about risk level:
    │ "High-value transfer to new recipient at 3AM.
    │  Running all security checks."
    │
    ├──→ Nokia NaC: SIM Swap Check ──→ {swapped: true, date: "2h ago"}
    ├──→ Nokia NaC: Number Verify ───→ {verified: false}
    ├──→ Nokia NaC: Device Status ───→ {roaming: true, country: "NG"}
    ├──→ Nokia NaC: Device Swap ────→ {swapped: true}
    │
    ▼
Risk Scoring Engine
    │
    │ sim_swap: 1.0 × 0.35 = 0.35
    │ num_verify: 1.0 × 0.30 = 0.30
    │ dev_status: 0.7 × 0.15 = 0.105
    │ context: 0.9 × 0.20 = 0.18
    │ TOTAL: 0.935 → Score: 94/100
    │
    ▼
Decision: BLOCK
    │
    ├──→ Response to Payment Platform: {decision: "BLOCK", score: 94, reasoning: "..."}
    ├──→ Audit Log to Supabase: full decision trace with timestamps
    └──→ WebSocket to Dashboard: live visualization update
```

---

## 5. AI Agent Design

### 5.1 Agent Orchestration Approach

SafePay's AI agent is built using **Google Agent Development Kit (ADK)** with **Gemini 2.0 Flash** as the reasoning model, following the approved tooling guidelines from the AI Resource and Tooling Guide.

**Why Google ADK:**

- Native integration with Gemini models for fast inference (<500ms reasoning)
- Built-in workflow orchestration (sequential, parallel, conditional tool calling)
- Structured tool definition with typed inputs/outputs
- Agent trace/observability for debugging and audit compliance

### 5.2 Agent Definition

```python
from google.adk import Agent, Tool

safepay_agent = Agent(
    name="SafePay Fraud Analyst",
    model="gemini-2.0-flash",
    instructions="""
    You are a real-time fraud analyst for MENA instant payments.
    When you receive a transaction, assess its risk by querying
    telecom network signals. Choose which tools to call based on
    the transaction's risk profile. Produce a risk score and
    explain your reasoning.
    """,
    tools=[
        check_sim_swap,      # SIM Swap API wrapper
        verify_number,       # Number Verification API wrapper
        check_device_status, # Device Status API wrapper
        check_device_swap,   # Device Swap API wrapper
        calculate_risk_score # Scoring engine
    ]
)
```

### 5.3 What Makes This Agent Genuinely "Agentic"

| Agentic Capability         | How SafePay Implements It                                                                                                                                                                   |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Planning**               | Agent receives transaction context and plans which tools to call based on amount, recipient history, and time signals                                                                       |
| **Reasoning**              | Agent weighs multiple API responses together - a SIM swap alone is suspicious, but SIM swap + failed number verification + unexpected roaming = near-certain fraud                          |
| **Dynamic tool selection** | Low-risk transactions trigger 1 API check. High-risk transactions trigger all 4. The agent decides, not a hardcoded rule.                                                                   |
| **Explainability**         | Every decision includes a natural-language reasoning trace: "BLOCKED: SIM swapped 2 hours ago, device does not match registered number, roaming in unusual country. Combined risk: 94/100." |
| **Autonomy**               | Agent operates without human intervention for clear-cut cases (score <30 or >70). Only ambiguous cases (30-70) are escalated for step-up authentication.                                    |

---

## 6. Technical Architecture

### 6.1 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    SAFEPAY MENA SYSTEM                       │
│                                                             │
│  ┌─────────────┐  ┌───────────────────────────────────┐    │
│  │ FRONTEND    │  │ BACKEND (FastAPI + Python)         │    │
│  │ Next.js     │  │                                   │    │
│  │             │  │  ┌─────────────────────────────┐  │    │
│  │ - Risk      │  │  │ GOOGLE ADK AGENT            │  │    │
│  │   Gauge     │◄─┤  │ (Gemini 2.0 Flash)          │  │    │
│  │ - Agent     │WS│  │                             │  │    │
│  │   Trace     │  │  │ Tools:                      │  │    │
│  │ - Signal    │  │  │ ┌─────────┐ ┌────────────┐  │  │    │
│  │   Breakdown │  │  │ │SIM Swap │ │Num Verify  │  │  │    │
│  │ - Tx List   │  │  │ └────┬────┘ └─────┬──────┘  │  │    │
│  └─────────────┘  │  │ ┌────┴────┐ ┌─────┴──────┐  │  │    │
│                   │  │ │Dev Stat │ │Dev Swap    │  │  │    │
│                   │  │ └────┬────┘ └─────┬──────┘  │  │    │
│                   │  │      └──────┬─────┘         │  │    │
│                   │  │      ┌──────▼──────┐        │  │    │
│                   │  │      │Risk Scoring │        │  │    │
│                   │  │      │Engine       │        │  │    │
│                   │  │      └──────┬──────┘        │  │    │
│                   │  │      ┌──────▼──────┐        │  │    │
│                   │  │      │Decision     │        │  │    │
│                   │  │      │Engine       │        │  │    │
│                   │  └──────┴──────┬──────┴────────┘  │    │
│                   │                │                   │    │
│  ┌─────────────┐  │  ┌─────────────▼──────────────┐   │    │
│  │ SUPABASE    │◄─┤  │ Nokia Network-as-Code      │   │    │
│  │ (PostgreSQL)│  │  │ Platform (CAMARA APIs)     │   │    │
│  │             │  │  │ - Simulator Environment    │   │    │
│  │ - Audit Log │  │  └────────────────────────────┘   │    │
│  │ - User      │  │                                   │    │
│  │   Profiles  │  │                                   │    │
│  │ - Tx History│  └───────────────────────────────────┘    │
│  └─────────────┘                                           │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Tech Stack

| Layer            | Technology                                   | Justification                                               |
| ---------------- | -------------------------------------------- | ----------------------------------------------------------- |
| **AI Agent**     | Google ADK + Gemini 2.0 Flash                | Approved tooling, native Gemini integration, fast inference |
| **Backend**      | FastAPI (Python 3.11+)                       | Async support, type safety, direct Nokia SDK integration    |
| **Network APIs** | Nokia NaC Python SDK (`network_as_code`)     | Official SDK, simulator support, Apache 2.0 license         |
| **Database**     | Supabase (PostgreSQL)                        | Managed DB, built-in auth, real-time subscriptions          |
| **Frontend**     | Next.js + React                              | SSR, WebSocket support for live dashboard                   |
| **Deployment**   | Vercel (frontend) + Railway/Render (backend) | Quick deployment for demo                                   |

### 6.3 Data Flow Summary

1. **Ingestion:** Payment platform sends transaction to SafePay API endpoint
2. **Enrichment:** Backend fetches sender profile (transaction history, known recipients, usual location)
3. **Agent orchestration:** AI agent receives enriched context, plans tool calls, queries Nokia NaC
4. **Scoring:** Risk engine aggregates API signals with configurable weights
5. **Decision:** Agent outputs APPROVE/STEP-UP/BLOCK with reasoning
6. **Logging:** Full decision trace persisted to Supabase for audit
7. **Visualization:** Dashboard updates in real-time via WebSocket

---

## 7. Business Model

### 7.1 Monetization Strategy

| Revenue Stream                  | Pricing                             | Target Customer                         |
| ------------------------------- | ----------------------------------- | --------------------------------------- |
| **Per-transaction fraud check** | $0.01-0.05 per check                | Banks, fintechs, payment processors     |
| **Monthly subscription**        | $500-5,000/month (tiered by volume) | Mid-size banks, mobile wallet operators |
| **Enterprise license**          | $50,000-200,000/year                | Central banks, large commercial banks   |

### 7.2 Commercial Value Summary

- **Cost of fraud:** $270-$160,000+ per SIM swap incident, plus $15-25 per manual investigation
- **Cost of SafePay:** <$0.01 per API call on Nokia NaC. At $0.02 per check, the system pays for itself if it prevents even 1 fraud case per 10,000 transactions.
- **Addressable market:** Egypt's InstaPay alone (2.2B transactions/year) represents $44M annual revenue at $0.02/check
- **Total MENA addressable market:** $275B in digital payments across 22 countries

### 7.3 Potential Impact

| Metric                   | Projection                                                                                  |
| ------------------------ | ------------------------------------------------------------------------------------------- |
| Fraud loss reduction     | 44% (based on early CAMARA pilot data)                                                      |
| False positive reduction | 55% (fewer legitimate transactions wrongly blocked)                                         |
| Unbanked conversion      | Reduced fraud -> increased trust -> accelerated financial inclusion for 200M unbanked Arabs |
| Operator revenue         | New API monetization stream for MENA carriers already investing in Open Gateway             |

---

## 8. Team Overview

| Member                      | Role                             | Background                                                                                                                                                                                                                                                                                                                                                               |
| --------------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Karim Mohamed Abdelnabi** | Solo Developer - Full Stack + AI | Hands-on experience with Google ADK, Gemini API, LLM-based agent orchestration, and full-stack development (Next.js, FastAPI, Python, Supabase). Covers AI agent design, backend/API integration, frontend dashboard, and business pitch as a solo participant. |

---

## 9. Demos & Visuals

> **Status:** To be added during prototype development if selected for Phase 2.

**Planned demo components:**

- Live split-screen demonstration: left shows payment flow, right shows agent reasoning trace in real-time
- Risk gauge visualization (0-100) with color-coded thresholds
- Signal breakdown chart showing individual API contributions to risk score
- Three pre-built scenarios: normal transaction (APPROVE), SIM swap attack (BLOCK), ambiguous case (STEP-UP)
- Agent trace showing natural-language reasoning for each decision

---

## 10. Criterion Alignment Summary

| Criterion                       | How SafePay Scores                                                                                                                                                                                                                                          |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Relevance**                   | Theme 4 (Fintech Anti-Fraud). Egypt-specific InstaPay data, UAE Aani, Saudi SAMA investment. Regional pain point validated by INTERPOL Operation Ramz (200+ arrests across 13 MENA countries).                                                              |
| **Impact**                      | $275B addressable market, 64% unbanked (200M people), 22 MENA countries reachable via carrier-agnostic CAMARA APIs. Clear per-transaction business model with $44M Egypt-only revenue potential.                                                            |
| **Innovation**                  | First multi-API AI agent orchestration layer for payment fraud. Replaces SMS OTP with carrier-level Number Verification. Bridges the PwC-identified "fraud gap" between telecoms and banks.                                                                 |
| **Complexity & Implementation** | 4 CAMARA APIs (SIM Swap, Number Verify, Device Status, Device Swap) orchestrated by Google ADK agent with weighted risk scoring. Full architecture: FastAPI backend, Nokia NaC SDK, Supabase audit trail, Next.js dashboard. Feasible on free-tier tooling. |
