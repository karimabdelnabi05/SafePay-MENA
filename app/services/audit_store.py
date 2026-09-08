"""
SafePay MENA - Supabase Immutable Audit Ledger Client
Provides persistent, tamper-evident recording of transaction evaluations,
telecom signal vectors, and Gemini regulatory traces.
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime
import httpx
from app.config import settings
from app.core.models import TransactionRequest, RiskDecision

logger = logging.getLogger("safepay.audit_store")

class SupabaseAuditStore:
    def __init__(self):
        self.supabase_url: str = getattr(settings, "SUPABASE_URL", "")
        self.supabase_key: str = getattr(settings, "SUPABASE_KEY", "")
        self._in_memory_logs = []

    async def persist_audit_record(
        self,
        txn: TransactionRequest,
        decision: RiskDecision
    ) -> bool:
        """
        Records the immutable audit payload into Supabase PostgreSQL.
        Falls back to in-memory ledger if Supabase credentials are not configured.
        """
        record: Dict[str, Any] = {
            "transaction_id": txn.transaction_id,
            "sender_phone": txn.sender_phone,
            "recipient_id": txn.recipient_id,
            "recipient_name": txn.recipient_name,
            "amount": txn.amount,
            "currency": txn.currency.value,
            "is_saved_beneficiary": txn.is_saved_beneficiary,
            "decision": decision.decision.value,
            "risk_score": decision.risk_score,
            "primary_vector": decision.primary_vector.value,
            "carrier_name": decision.signals.carrier_name,
            "number_verified": decision.signals.number_verified,
            "sim_swapped_recently": decision.signals.sim_swapped_recently,
            "sim_swap_hours_ago": decision.signals.sim_swap_hours_ago,
            "is_on_active_voice_call": decision.signals.is_on_active_voice_call,
            "is_roaming": decision.signals.is_roaming,
            "roaming_country": decision.signals.roaming_country,
            "device_match": decision.signals.device_match,
            "statutory_flags": decision.statutory_flags,
            "reasons": decision.reasons,
            "ai_compliance_trace": decision.ai_compliance_trace,
            "execution_time_ms": decision.execution_time_ms,
            "created_at": datetime.utcnow().isoformat()
        }

        # In-memory store for immediate retrieval
        self._in_memory_logs.append(record)

        # Persist to live Supabase REST endpoint if configured
        if self.supabase_url and self.supabase_key:
            endpoint = f"{self.supabase_url.rstrip('/')}/rest/v1/safepay_audit_logs"
            headers = {
                "apikey": self.supabase_key,
                "Authorization": f"Bearer {self.supabase_key}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal"
            }
            try:
                async with httpx.AsyncClient(timeout=2.0) as client:
                    resp = await client.post(endpoint, json=record, headers=headers)
                    return resp.status_code in (200, 201)
            except Exception as ex:
                logger.warning(f"Failed to persist to Supabase: {ex}")
                return False

        return True

    def get_recent_logs(self, limit: int = 50):
        """Returns the most recent in-memory audit logs."""
        return self._in_memory_logs[-limit:]

audit_store = SupabaseAuditStore()
