# GEMINI.md - SafePay MENA Project Operating Manual

**Project Name:** SafePay MENA  
**Tagline:** Real-Time AI Fraud Shield for Instant Payments Powered by Telecom Network Intelligence  
**Hackathon:** GSMA MENA Ignite Hackathon (Theme 4: Secure FinTech, Payments & Anti-Fraud Innovation)  
**Status:** Phase 2 (Prototype Development & Mentorship)  
**Team:** Karim Mohamed Abdelnabi (Solo Full-Stack & AI Engineer)  
**Assigned Mentor:** Eng. Abdullah A. Alkaoud (`mentor-contact-removed`) - stc  

---

## 1. Project Vision & Architecture

SafePay MENA is an AI-orchestrated telecom-banking security middleware.  
It bridges the "fraud gap" between banking payment rails (InstaPay Egypt, Sarie / STC Bank Saudi, Aani UAE) and telecom operators (stc, Vodafone, e&).  

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
│  │ • E.164 Regional Phone Normalizer (+20 / +966)                        │  │
│  │ • Non-Linear Combinatorial Risk Matrix Engine                         │  │
│  │ • In-Memory Cache (Redis TTL 15m) & Circuit Breaker                   │  │
│  └──────────────────────────────────┬────────────────────────────────────┘  │
│                                     │                                       │
│         ┌───────────────────────────┴───────────────────────────┐           │
│         ▼                                                       ▼           │
│  ┌───────────────────────────────┐     ┌─────────────────────────────────┐  │
│  │ AI REASONING & RISK ENGINE    │     │ CAMARA NETWORK API CLIENT       │  │
│  │ • Gemini 2.0 Flash Agent      │     │ • 3-Legged Mobile Number Verify │  │
│  │ • Natural Language Audit Log  │     │ • 2-Legged Server SIM Swap      │  │
│  │ • SAMA 2026 Compliance Trace  │     │ • 2-Legged Device Status        │  │
│  │ • Velocity & Anomaly Scorer   │     │ • 2-Legged Device Swap          │  │
│  └───────────────┬───────────────┘     └────────────────┬────────────────┘  │
│                  │                                      │                   │
│                  ▼                                      ▼                   │
│  ┌───────────────────────────────┐     ┌─────────────────────────────────┐  │
│  │ SUPABASE (PostgreSQL)         │     │ TELECOM SANDBOX / MOCK LAYER    │  │
│  │ • Immutable Audit Logs        │     │ • Nokia NaC Live Sandbox        │  │
│  │ • User Device Profiles        │     │ • Deterministic Local Mock      │  │
│  │ • Transaction History         │     │ • Toggle: USE_MOCK=True/False   │  │
│  └───────────────────────────────┘     └─────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Core CAMARA APIs & Verification Roles

| API Name | Type | Standard Endpoint | Role in SafePay |
| :--- | :--- | :--- | :--- |
| **Number Verification** | **3-Legged OAuth** (Cellular Bearer) | `/number-verification/v0/verify` | Silently verifies that the active mobile data connection belongs to the registered SIM in 300ms. Replaces SMS OTPs. |
| **SIM Swap** | **2-Legged OAuth** (Server-to-Server) | `/sim-swap/v0/check` | Queries carrier DB to detect if the SIM card was swapped within the last 24-48 hours. Primary account takeover indicator. |
| **Device Status** | **2-Legged OAuth** (Server-to-Server) | `/device-status/v0/roaming` | Detects international roaming anomalies and unreachable handsets. |
| **Device Swap** | **2-Legged OAuth** (Server-to-Server) | `/device-swap/v0/check` | Detects if the SIM was inserted into a new hardware device (IMEI change). |

---

## 3. Technology Stack & Key Libraries

- **AI Agent Brain:** Google Gemini 2.0 Flash via Google GenAI SDK / Google ADK.  
- **Backend API:** FastAPI (Python 3.11+), Pydantic v2, AsyncIO (Parallel concurrent API execution), Uvicorn.  
- **Telecom SDK:** Nokia Network-as-Code Python SDK (`network_as_code`) + Local Deterministic Mock Server.  
- **Database & Auth:** Supabase (PostgreSQL) for tamper-proof audit trails.  
- **Caching & Resilience:** Redis (TTL 15m) + Circuit Breaker pattern.  
- **Frontend Dashboard:** Next.js 14, Tailwind CSS, Lucide icons, Framer Motion, WebSockets.  

---

## 4. The 3 Demo Scenarios

1. **Scenario 1 (Clean Flow):** Normal 200 EGP transfer to saved contact $\rightarrow$ Silent 3-legged Number Verification passes $\rightarrow$ **Instant APPROVE (200ms)**.  
2. **Scenario 2 (SIM Swap Attack):** Scammer initiates 35,000 SAR transfer at 3:00 AM $\rightarrow$ 2-legged SIM Swap returns "Swapped 2h ago" + Device Mismatch $\rightarrow$ **Immediate HARD BLOCK + AI Compliance Trace**.  
3. **Scenario 3 (Travel / Step-Up):** User sends 2,500 EGP while roaming in UAE $\rightarrow$ Moderate risk (Score 42) $\rightarrow$ **Prompts Step-Up Face ID Biometric Challenge $\rightarrow$ Passes**.  

---

## 5. File Map & Key Artifacts

- [SAFEPAY_MASTER_PROJECT_PLAN.md](file:///C:/Users/karee/Desktop/Mena_Ignite_hackathon/SAFEPAY_MASTER_PROJECT_PLAN.md) - Master Phase 2 execution roadmap and timeline.  
- [MENTOR_MEETING_READINESS_CHECKLIST.md](file:///C:/Users/karee/Desktop/Mena_Ignite_hackathon/MENTOR_MEETING_READINESS_CHECKLIST.md) - Official GSMA Mentorship Readiness Dossier (English): 2.5m pitch, 4 guidance pillars, 5 questions, run sheet & objection matrix.  
- [MENTOR_MEETING_READINESS_CHECKLIST_AR.md](file:///C:/Users/karee/Desktop/Mena_Ignite_hackathon/MENTOR_MEETING_READINESS_CHECKLIST_AR.md) - Official GSMA Mentorship Readiness Dossier (Arabic): كامل باللغة العربية.  
- [MENTOR_MEETING_MASTER_PREP.html](file:///C:/Users/karee/Desktop/Mena_Ignite_hackathon/MENTOR_MEETING_MASTER_PREP.html) - Interactive English meeting dashboard with live 30-minute timer, teleprompter & 5 questions.  
- [MENTOR_MEETING_MASTER_PREP_AR.html](file:///C:/Users/karee/Desktop/Mena_Ignite_hackathon/MENTOR_MEETING_MASTER_PREP_AR.html) - Interactive Arabic meeting dashboard (RTL) with live 30-minute stopwatch.  
- [SafePay_MENA_Mentor_Slides.html](file:///C:/Users/karee/Desktop/Mena_Ignite_hackathon/SafePay_MENA_Mentor_Slides.html) - Interactive 16:9 widescreen presentation slides for screen sharing.  
- [SafePay_MENA_Mentor_Presentation.pdf](file:///C:/Users/karee/Desktop/Mena_Ignite_hackathon/SafePay_MENA_Mentor_Presentation.pdf) - Compiled landscape 16:9 PDF presentation for the mentor call.  
- [build_mentor_presentation.py](file:///C:/Users/karee/Desktop/Mena_Ignite_hackathon/build_mentor_presentation.py) - ReportLab PDF presentation builder script.  
- [SafePay_Architecture_and_UseCases_Guide.html](file:///C:/Users/karee/Desktop/Mena_Ignite_hackathon/SafePay_Architecture_and_UseCases_Guide.html) - Visual interactive guide covering 10 real use cases, dynamic risk scoring formula, and API optimization.  
- [CAMARA_DOCUMENTATION_AND_TOOLS_GUIDE.md](file:///C:/Users/karee/Desktop/Mena_Ignite_hackathon/CAMARA_DOCUMENTATION_AND_TOOLS_GUIDE.md) - Direct links to official CAMARA GitHub repos, OpenAPI specs, and tools.  
- [SAFEPAY_DEEP_ASSESSMENT_AND_IMPROVEMENTS.md](file:///C:/Users/karee/Desktop/Mena_Ignite_hackathon/SAFEPAY_DEEP_ASSESSMENT_AND_IMPROVEMENTS.md) - Industry audit across 8 dimensions.  
- [SAFEPAY_SECURITY_THREAT_MODEL_AND_TRACES.md](file:///C:/Users/karee/Desktop/Mena_Ignite_hackathon/SAFEPAY_SECURITY_THREAT_MODEL_AND_TRACES.md) - Threat model, 7 attack vectors & observability trace schema.  
- [SAFEPAY_FINANCIAL_AND_UNIT_ECONOMICS_DEEP_DIVE.md](file:///C:/Users/karee/Desktop/Mena_Ignite_hackathon/SAFEPAY_FINANCIAL_AND_UNIT_ECONOMICS_DEEP_DIVE.md) - Financial model, ROI (693%), and unit economics.  
- [context/progress-tracker.md](file:///C:/Users/karee/Desktop/Mena_Ignite_hackathon/context/progress-tracker.md) - Active milestone checklist.  
- [context/dev-log.md](file:///C:/Users/karee/Desktop/Mena_Ignite_hackathon/context/dev-log.md) - Timestamped developer log.  
- [SafePay_MENA_Pitch_Deck_Content.md](file:///C:/Users/karee/Desktop/Mena_Ignite_hackathon/SafePay_MENA_Pitch_Deck_Content.md) - Pitch deck content with speaker notes.  

---

## 6. Development Rules & Guidelines

- **Deterministic Shield First:** All financial authorization decisions (`APPROVE`, `STEP_UP`, `BLOCK`) must be calculated deterministically in <10ms before or alongside asynchronous LLM trace generation.  
- **E.164 Normalization:** All phone numbers must be sanitized and converted to E.164 (`+20...`, `+966...`) before calling telecom endpoints.  
- **Zero PII Exposure:** Never pass bank account numbers, OTPs, or customer names to telecom network APIs. Only exchange verification tokens and status booleans.  
- **Mock-First Reliability:** Always keep `USE_MOCK=True` working with offline preset fixtures so the demo and test suites run with 100% reliability.  
