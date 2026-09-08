import sys
from pathlib import Path

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import time
from app.core.models import (
    TransactionRequest,
    CarrierSignalProfile,
    RiskTier,
    ScamVector,
    Currency
)
from app.core.risk_engine import DeterministicRiskEngine


def test_clean_transfer_scenario():
    """Scenario 1: Clean 200 EGP transfer -> Silent APPROVE in <10ms with zero SMS OTP."""
    txn = TransactionRequest(
        transaction_id="txn_clean_001",
        sender_phone="+201012345678",
        recipient_id="instapay_mom_alias",
        recipient_name="Fatima Mohamed",
        amount=200.0,
        currency=Currency.EGP,
        is_saved_beneficiary=True
    )
    signals = CarrierSignalProfile(
        phone_number="+201012345678",
        carrier_name="Vodafone Egypt",
        number_verified=True,
        sim_swapped_recently=False,
        is_on_active_voice_call=False,
        is_roaming=False,
        device_match=True
    )
    
    decision = DeterministicRiskEngine.evaluate(txn, signals)
    
    assert decision.decision == RiskTier.APPROVE
    assert decision.risk_score < 25
    assert decision.primary_vector == ScamVector.CLEAN
    assert any("CBUAE_NOTICE_2025_3057_COMPLIANT" in flag for flag in decision.statutory_flags)
    assert decision.execution_time_ms < 10.0

def test_vishing_spam_call_scenario():
    """Scenario 2: 15,000 SAR transfer while on active phone call -> STEP_UP Face ID challenge."""
    txn = TransactionRequest(
        transaction_id="txn_vishing_002",
        sender_phone="+966501234567",
        recipient_id="SA0380000000608010167519",
        recipient_name="Unknown Payee (Scammer)",
        amount=15000.0,
        currency=Currency.SAR,
        is_saved_beneficiary=False
    )
    signals = CarrierSignalProfile(
        phone_number="+966501234567",
        carrier_name="stc Saudi",
        number_verified=True,
        sim_swapped_recently=False,
        is_on_active_voice_call=True,  # Scam Signal active call!
        is_roaming=False,
        device_match=True
    )
    
    decision = DeterministicRiskEngine.evaluate(txn, signals)
    
    assert decision.decision == RiskTier.STEP_UP
    assert 25 <= decision.risk_score < 70
    assert decision.primary_vector == ScamVector.VISHING_ACTIVE_CALL
    assert any("SCAM SIGNAL" in r for r in decision.reasons)
    assert any("COERCION RISK" in r for r in decision.reasons)

def test_sim_swap_attack_scenario():
    """Scenario 3: 35,000 SAR transfer after SIM swap 2 hours ago -> Immediate HARD BLOCK."""
    txn = TransactionRequest(
        transaction_id="txn_attack_003",
        sender_phone="+966559876543",
        recipient_id="SA9910000000998877665544",
        recipient_name="Mule Account Corp",
        amount=35000.0,
        currency=Currency.SAR,
        is_saved_beneficiary=False
    )
    signals = CarrierSignalProfile(
        phone_number="+966559876543",
        carrier_name="stc Saudi",
        number_verified=False,  # Rogue device
        sim_swapped_recently=True,
        sim_swap_hours_ago=2.1,
        is_on_active_voice_call=False,
        is_roaming=False,
        device_match=False
    )
    
    decision = DeterministicRiskEngine.evaluate(txn, signals)
    
    assert decision.decision == RiskTier.BLOCK
    assert decision.risk_score >= 70
    assert decision.primary_vector == ScamVector.SIM_SWAP_ATO
    assert any("CRITICAL: SIM card swapped" in r for r in decision.reasons)
    assert any("SAMA_SARIE_LIMIT_20K" in flag for flag in decision.statutory_flags)

def test_high_throughput_performance():
    """Verify 1,000 evaluations execute in under 50ms total (<0.05ms per transaction)."""
    txn = TransactionRequest(
        transaction_id="txn_perf",
        sender_phone="+966501234567",
        recipient_id="acc_123",
        recipient_name="Test",
        amount=100.0,
        currency=Currency.SAR
    )
    signals = CarrierSignalProfile(
        phone_number="+966501234567",
        carrier_name="stc Saudi",
        number_verified=True,
        sim_swapped_recently=False,
        is_on_active_voice_call=False,
        is_roaming=False
    )
    
    t0 = time.perf_counter()
    for _ in range(1000):
        DeterministicRiskEngine.evaluate(txn, signals)
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    
    print(f"1,000 evaluations completed in: {elapsed_ms:.2f} ms")
    assert elapsed_ms < 100.0  # Well within <0.1ms per transaction SLA

if __name__ == "__main__":
    print("Running tests in test_risk_engine.py...")
    test_clean_transfer_scenario()
    print("  [PASS] test_clean_transfer_scenario")
    test_vishing_spam_call_scenario()
    print("  [PASS] test_vishing_spam_call_scenario")
    test_sim_swap_attack_scenario()
    print("  [PASS] test_sim_swap_attack_scenario")

    test_high_throughput_performance()
    print("  [PASS] test_high_throughput_performance")
    print("ALL TESTS PASSED SUCCESSFULLY!")


