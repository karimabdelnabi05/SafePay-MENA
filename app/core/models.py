"""
SafePay MENA - Core Data Models
Strict Pydantic v2 Schemas for Transactions, Telecom Signals, and Risk Decisions.
"""

from enum import Enum
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class Currency(str, Enum):
    EGP = "EGP"  # Egyptian Pound (InstaPay)
    SAR = "SAR"  # Saudi Riyal (Sarie / STC Bank)
    AED = "AED"  # UAE Dirham (Aani)
    USD = "USD"  # Cross-border

class RiskTier(str, Enum):
    APPROVE = "APPROVE"    # Tier 1: Score < 25 (Silent authorization <200ms, NO OTP)
    STEP_UP = "STEP_UP"    # Tier 2: Score 25-69 (Prompt 1-sec Face ID challenge)
    BLOCK = "BLOCK"        # Tier 3: Score >= 70 (Hard block, zero money moves, SOC alert)

class ScamVector(str, Enum):
    CLEAN = "CLEAN"
    VISHING_ACTIVE_CALL = "VISHING_ACTIVE_CALL"
    SIM_SWAP_ATO = "SIM_SWAP_ATO"
    ROAMING_ANOMALY = "ROAMING_ANOMALY"
    CARD_LEAKAGE_CNP = "CARD_LEAKAGE_CNP"
    SAMA_LIMIT_EXCEEDED = "SAMA_LIMIT_EXCEEDED"

class TransactionRequest(BaseModel):
    transaction_id: str = Field(..., description="Unique transaction UUID")
    sender_phone: str = Field(..., description="Sender phone in local or E.164 format")
    recipient_id: str = Field(..., description="Recipient IBAN, phone, or wallet alias")
    recipient_name: str = Field(..., description="Recipient display name")
    amount: float = Field(..., gt=0, description="Transfer amount")
    currency: Currency = Field(default=Currency.SAR, description="Payment currency")
    is_saved_beneficiary: bool = Field(default=False, description="Whether recipient is a trusted saved contact")
    device_ip: str = Field(default="192.168.1.1", description="Client IP address")
    device_imei: Optional[str] = Field(default=None, description="Client hardware identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="UTC initiation timestamp")

class CarrierSignalProfile(BaseModel):
    phone_number: str = Field(..., description="Sanitized E.164 phone number")
    carrier_name: str = Field(..., description="Identified carrier (e.g. stc Saudi, Vodafone Egypt, e& UAE)")
    number_verified: bool = Field(..., description="CAMARA Number Verification: cellular bearer matches SIM")
    sim_swapped_recently: bool = Field(..., description="CAMARA SIM Swap: SIM changed within maxAge window")
    sim_swap_hours_ago: Optional[float] = Field(default=None, description="Hours since last SIM pairing change")
    is_on_active_voice_call: bool = Field(..., description="CAMARA Scam Signal: user actively on phone call")
    is_roaming: bool = Field(..., description="CAMARA Device Status: device roaming outside home network")
    roaming_country: Optional[str] = Field(default=None, description="ISO country code if roaming")
    device_match: bool = Field(default=True, description="Device Swap check: IMEI matches carrier registry")
    eval_latency_ms: float = Field(default=0.0, description="Time taken to collect telecom signals in ms")

class RiskDecision(BaseModel):
    transaction_id: str
    decision: RiskTier
    risk_score: int = Field(..., ge=0, le=100, description="Normalized risk gauge score (0-100)")
    primary_vector: ScamVector
    reasons: List[str] = Field(default_factory=list, description="Specific risk indicators triggered")
    statutory_flags: List[str] = Field(default_factory=list, description="Central bank regulatory citations")
    recommended_action: str
    execution_time_ms: float
    signals: CarrierSignalProfile
    ai_compliance_trace: Optional[str] = None

class BiometricStepUpRequest(BaseModel):
    transaction_id: str
    biometric_token: str
    biometric_type: str = "FACE_ID"  # FACE_ID or PASSKEY
    success: bool = True

class PresetScenario(str, Enum):
    CLEAN_TRANSFER = "CLEAN_TRANSFER"         # 200 EGP to Mom -> Silent Approve (<200ms)
    SPAM_CALL_SCAM = "SPAM_CALL_SCAM"         # 15,000 SAR on active phone call -> Face ID Step-Up
    SIM_SWAP_ATTACK = "SIM_SWAP_ATTACK"       # 35,000 SAR swapped 2h ago -> Immediate Hard Block
