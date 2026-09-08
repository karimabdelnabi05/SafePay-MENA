# SafePay MENA - Security Threat Model, Attack Vectors & Observability Trace Architecture

**Document Version:** 1.0 (Cybersecurity & Observability Blueprint)  
**Purpose:** Defines the 7 adversarial attack vectors, defense countermeasures, and the unified diagnostic trace schema for debugging, live demos, and regulatory audits.  

---

## 1. The 7 Adversarial Attack Vectors & Countermeasures

```
┌──────────────────────────────────────┬──────────────────────────────────────┐
│ Attack Vector (Hacker Strategy)      │ SafePay Defense Countermeasure       │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ 1. The 72h "Sleeper" Attack          │ Multi-Signal Correlation: Checks     │
│    (Waiting past the 48h SIM clock)  │ Device Swap (IMEI) + New Beneficiary │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ 2. Authorized Push Payment (APP)     │ GSMA "Scam Signal" Call Detection +  │
│    (Social engineering / fake calls) │ Recipient Mule Velocity Tripwires    │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ 3. Telco Insider Store Collusion     │ 3-Legged Physical Cellular Bearer +  │
│    (Bribed employee issuing SIMs)    │ In-App Biometric Liveness Face Scan  │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ 4. Distributed Botnet Smurfing       │ Destination Graph Velocity: Freezes  │
│    (Hundreds of 50 EGP micro-tx)     │ mule accounts receiving bursts of tx │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ 5. AI Prompt Injection               │ Zero LLM Authorization Dependency:   │
│    ("System Override" in memo field) │ Math engine decides in 10ms; memo PII│
│                                      │ is strictly sanitized via Pydantic   │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ 6. Telco DDoS / Outage Exploitation  │ Fail-Secure Circuit Breaker: If API  │
│    (Trying to force "Fail-Open")     │ times out, requires Face ID/Step-Up  │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ 7. Rogue IMSI Catchers / Stingrays   │ Encrypted 5G Core OIDC Tokens + TLS  │
│    (Man-in-the-middle radio towers)  │ Certificate Pinning to Telco Gateway │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

---

## 2. The Unified Diagnostic Trace Schema (`TransactionTrace`)

Every transaction processed by SafePay generates an immutable, structured diagnostic trace.  
If any test fails or an unexpected decision occurs, this trace reveals the exact sub-millisecond execution timeline and signal breakdown.

```json
{
  "trace_id": "tr_9a8b7c6d-5e4f-3a2b-1c0d-e9f8a7b6c5d4",
  "timestamp": "2026-08-31T00:51:00.124Z",
  "environment": "MOCK_SANDBOX",
  "transaction_context": {
    "transaction_id": "tx_20260831_98210",
    "amount": 35000.00,
    "currency": "SAR",
    "sender_phone": "+966501234567",
    "sender_country": "SA",
    "recipient_iban": "SA4420000001234567890123",
    "channel": "MOBILE_WALLET",
    "timestamp_local": "03:15:22 AM"
  },
  "execution_timings_ms": {
    "e164_normalization": 0.4,
    "redis_cache_lookup": 1.2,
    "parallel_camara_fetch": {
      "sim_swap_api": 85.3,
      "device_status_api": 92.1,
      "device_swap_api": 78.4,
      "number_verification": 110.2,
      "longest_api_wait": 110.2
    },
    "deterministic_risk_matrix": 0.8,
    "gemini_audit_trace_generation": 210.5,
    "total_decision_latency": 112.6,
    "total_e2e_pipeline_latency": 235.6
  },
  "raw_signals_captured": {
    "sim_swap": {
      "swapped": true,
      "age_hours": 2.1,
      "source": "stc_open_gateway_v0"
    },
    "number_verification": {
      "device_phone_verified": false,
      "bearer": "CELLULAR_MISMATCH"
    },
    "device_status": {
      "roaming": true,
      "roaming_country": "NG",
      "reachability": "CONNECTED"
    },
    "device_swap": {
      "hardware_changed": true,
      "previous_imei_hash": "a1b2...",
      "current_imei_hash": "f9e8..."
    },
    "behavioral_velocity": {
      "transactions_last_1h": 4,
      "total_amount_last_1h": 85000.00,
      "novel_recipient": true
    }
  },
  "risk_calculation_breakdown": {
    "base_risk": 10,
    "sim_swap_trigger": 85,
    "device_hardware_multiplier": 1.5,
    "velocity_multiplier": 1.2,
    "roaming_anomaly_penalty": 15,
    "calculated_score": 94,
    "calibrated_final_score": 94
  },
  "decision_output": {
    "action": "BLOCK",
    "action_code": "CRITICAL_ACCOUNT_TAKEOVER",
    "http_status_code": 403,
    "client_ui_message": "Transfer blocked for your protection. Immediate account security hold applied."
  },
  "ai_audit_compliance_trace": {
    "model": "gemini-2.0-flash",
    "sama_framework_category": "Real-Time Transaction Interception (Rule 4.2)",
    "audit_reasoning": "BLOCKED: Critical Account Takeover probability (Score: 94/100). Subscriber's SIM was replaced 2.1 hours ago, device hardware IMEI does not match profile baseline, and session originates from an active roaming network in Nigeria."
  },
  "circuit_breaker_state": {
    "status": "CLOSED",
    "failure_rate": 0.0,
    "fallback_used": false
  }
}
```

---

## 3. How Traces Are Used in Development & Testing

1. **Instant CLI Debugging:**  
   During automated `pytest` test runs, if an assertion fails, the test suite outputs the exact `trace_id` and timing breakdown so you know immediately if an API call timed out or if a score calculation diverged.
2. **Interactive Live Dashboard Drawer (Next.js):**  
   In the web dashboard, clicking on any transaction in the live feed opens an **"Inspect Trace" Slide-Over Drawer**, showing the exact JSON breakdown, latencies, and signal cards in real time.
3. **Regulatory Audit Log (Supabase):**  
   Every trace is stored in the Supabase PostgreSQL table `transaction_traces` with Row-Level Security, providing an immutable audit trail compliant with **SAMA 2026** and **CBE IPN** standards.
