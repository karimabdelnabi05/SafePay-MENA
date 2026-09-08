"""
SafePay MENA - Deterministic Combinatorial Risk Engine
Executes sub-10ms mathematical scoring combining transaction metadata and telecom network signals.
Enforces SAMA, CBE, and CBUAE statutory thresholds.
"""

import time
from app.core.models import (
    TransactionRequest,
    CarrierSignalProfile,
    RiskDecision,
    RiskTier,
    ScamVector,
    Currency
)
from app.config import settings

class DeterministicRiskEngine:
    """
    High-throughput, in-memory risk matrix.
    Guarantees <10ms execution latency with zero external I/O during the evaluation path.
    """
    
    @staticmethod
    def evaluate(txn: TransactionRequest, signals: CarrierSignalProfile) -> RiskDecision:
        start_time = time.perf_counter()
        
        score = 0
        reasons = []
        statutory_flags = []
        primary_vector = ScamVector.CLEAN
        
        # 1. Critical Signal: SIM Swap Check (Account Takeover Defense)
        if signals.sim_swapped_recently:
            primary_vector = ScamVector.SIM_SWAP_ATO
            hours = signals.sim_swap_hours_ago or 2.0
            if hours <= 24.0:
                score += 80
                reasons.append(f"CRITICAL: SIM card swapped {hours:.1f} hours ago (HLR/HSS alert)")
            elif hours <= 48.0:
                score += 65
                reasons.append(f"HIGH RISK: SIM card swapped within last 48 hours ({hours:.1f}h)")
            else:
                score += 40
                reasons.append(f"ELEVATED RISK: SIM card swapped recently ({hours:.1f}h)")
                
        # 2. Critical Signal: Scam Signal (Vishing & Phone Call Coercion Defense)
        if signals.is_on_active_voice_call:
            score += 40
            reasons.append("SCAM SIGNAL: Customer phone is engaged in an active, unverified voice call")
            if primary_vector == ScamVector.CLEAN:
                primary_vector = ScamVector.VISHING_ACTIVE_CALL
                
            # Compounding factor: high amount or unsaved contact while on a call
            if not txn.is_saved_beneficiary:
                score += 15
                reasons.append("COERCION RISK: Transfer initiated to a new, unsaved contact while on active phone call")
                
        # 3. Cellular Possession: Number Verification (Silent Auth)
        if not signals.number_verified:
            score += 45
            reasons.append("BEARER MISMATCH: Silent cellular connection does not match registered SIM (Rogue Device / Wi-Fi unverified)")
            if primary_vector == ScamVector.CLEAN:
                primary_vector = ScamVector.CARD_LEAKAGE_CNP
                
        # 4. Device Integrity: Device Swap Check (IMEI)
        if not signals.device_match:
            score += 30
            reasons.append("HARDWARE ANOMALY: SIM inserted into unrecognized IMEI handset")
            
        # 5. Geo & Roaming Anomaly
        if signals.is_roaming:
            score += 20
            roam_country = signals.roaming_country or "FOREIGN"
            reasons.append(f"ROAMING NOTICE: Device currently roaming outside home network in {roam_country}")
            if primary_vector == ScamVector.CLEAN:
                primary_vector = ScamVector.ROAMING_ANOMALY
                
        # 6. SAMA Statutory Thresholds (Saudi Arabia)
        if txn.currency == Currency.SAR and txn.amount >= settings.SAMA_INSTANT_LIMIT_SAR:
            statutory_flags.append(f"SAMA_SARIE_LIMIT_20K: Transaction amount ({txn.amount:,.0f} SAR) meets/exceeds SAMA 20,000 SAR high-value instant threshold")
            reasons.append("SAMA 20k SAR transfer safeguard invoked")
            score = max(score, 35)  # Enforce at least STEP_UP
            if primary_vector == ScamVector.CLEAN:
                primary_vector = ScamVector.SAMA_LIMIT_EXCEEDED
                
        # 7. CBE Statutory Limits (Egypt)
        if txn.currency == Currency.EGP and txn.amount > settings.INSTAPAY_DAILY_LIMIT_EGP:
            statutory_flags.append(f"CBE_INSTAPAY_LIMIT_EXCEEDED: Amount ({txn.amount:,.0f} EGP) exceeds CBE 70,000 EGP per-transaction cap")
            reasons.append("CBE InstaPay per-transaction regulatory cap exceeded")
            score = max(score, 75)  # Force BLOCK
            
        # 8. CBUAE Notice 2025/3057 Compliance Verification
        if signals.number_verified and not signals.sim_swapped_recently:
            statutory_flags.append("CBUAE_NOTICE_2025_3057_COMPLIANT: Authenticated via phishing-resistant cellular bearer (Zero SMS OTP liability)")
        elif not signals.number_verified:
            statutory_flags.append("CBUAE_NOTICE_2025_3057_SHIELD: Rogue device lacked cellular possession of registered SIM (Declined without SMS OTP exposure)")

            
        # Clamp score between 0 and 100
        normalized_score = min(100, max(0, score))
        
        # Decision Tiers
        if normalized_score >= 70:
            decision = RiskTier.BLOCK
            recommended_action = "HARD FREEZE: Transaction blocked immediately. High probability of account takeover or syndicate compromise. Zero funds moved."
        elif normalized_score >= 25:
            decision = RiskTier.STEP_UP
            recommended_action = "BIOMETRIC STEP-UP REQUIRED: Prompt 1-second on-device Face ID challenge with anti-coercion warning to break scammer control."
        else:
            decision = RiskTier.APPROVE
            primary_vector = ScamVector.CLEAN
            recommended_action = "SILENT APPROVAL: Cellular identity validated in <200ms. Zero customer friction, no SMS OTP."
            if not reasons:
                reasons.append("Normal user transaction profile; cellular bearer verified with no carrier anomalies")
                
        exec_latency = (time.perf_counter() - start_time) * 1000.0  # ms
        
        return RiskDecision(
            transaction_id=txn.transaction_id,
            decision=decision,
            risk_score=normalized_score,
            primary_vector=primary_vector,
            reasons=reasons,
            statutory_flags=statutory_flags,
            recommended_action=recommended_action,
            execution_time_ms=round(exec_latency, 2),
            signals=signals,
            raw_wire_trace=signals.raw_wire_trace,
            orchestration=signals.orchestration
        )
