"""
SafePay MENA - CAMARA Telecom Signal Gateway
Encapsulates GSMA Open Gateway network APIs with in-memory TTL caching and deterministic fallback fixtures.
"""

import time
import asyncio
from typing import Optional, Dict
from cachetools import TTLCache
from app.core.models import CarrierSignalProfile, PresetScenario
from app.services.phone_normalizer import normalize_phone_number
from app.config import settings

class TelecomGateway:
    """
    Unified gateway for CAMARA Open Gateway network APIs:
    - Number Verification (3-Legged)
    - SIM Swap (2-Legged)
    - Scam Signal (Active Call State)
    - Device Status (Roaming & Reachability)
    """
    
    def __init__(self):
        # 15-minute TTL cache for SIM swap results to minimize redundant carrier billing
        self._sim_swap_cache: TTLCache[str, Dict] = TTLCache(maxsize=10000, ttl=settings.SIM_SWAP_CACHE_TTL_SECONDS)
        
    async def evaluate_carrier_signals(
        self,
        raw_phone: str,
        scenario_override: Optional[PresetScenario] = None,
        timeout_seconds: float = 0.25
    ) -> CarrierSignalProfile:
        """
        Gathers real-time telecom network signals.
        Enforces a 250ms circuit breaker timeout to guarantee payment rail SLAs.
        """
        start_time = time.perf_counter()
        e164_phone, carrier_name, country_code = normalize_phone_number(raw_phone)
        
        try:
            profile = await asyncio.wait_for(
                self._resolve_signals(e164_phone, carrier_name, country_code, scenario_override),
                timeout=timeout_seconds
            )
        except asyncio.TimeoutError:
            # Circuit breaker: Fallback gracefully to default clean profile if carrier lags
            profile = CarrierSignalProfile(
                phone_number=e164_phone,
                carrier_name=carrier_name,
                number_verified=True,
                sim_swapped_recently=False,
                is_on_active_voice_call=False,
                is_roaming=False,
                device_match=True,
                eval_latency_ms=round((time.perf_counter() - start_time) * 1000.0, 2)
            )
            
        profile.eval_latency_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
        return profile
        
    async def _resolve_signals(
        self,
        phone: str,
        carrier: str,
        country: str,
        scenario: Optional[PresetScenario]
    ) -> CarrierSignalProfile:
        """Internal resolver supporting one-click demo presets and deterministic mock rules."""
        
        # 1. Preset Scenarios for Hackathon Demo
        if scenario == PresetScenario.CLEAN_TRANSFER:
            return CarrierSignalProfile(
                phone_number=phone,
                carrier_name=carrier,
                number_verified=True,
                sim_swapped_recently=False,
                is_on_active_voice_call=False,
                is_roaming=False,
                device_match=True
            )
            
        if scenario == PresetScenario.SPAM_CALL_SCAM:
            return CarrierSignalProfile(
                phone_number=phone,
                carrier_name=carrier,
                number_verified=True,
                sim_swapped_recently=False,
                is_on_active_voice_call=True,  # Scam Signal triggered!
                is_roaming=False,
                device_match=True
            )
            
        if scenario == PresetScenario.SIM_SWAP_ATTACK:
            return CarrierSignalProfile(
                phone_number=phone,
                carrier_name=carrier,
                number_verified=False,  # Rogue device / stolen credentials
                sim_swapped_recently=True,
                sim_swap_hours_ago=2.1,
                is_on_active_voice_call=False,
                is_roaming=False,
                device_match=False
            )
            
        # 2. Check in-memory SIM swap cache
        cached_swap = self._sim_swap_cache.get(phone)
        if cached_swap is not None:
            sim_swapped = cached_swap.get("swapped", False)
            swap_hours = cached_swap.get("hours", None)
        else:
            sim_swapped = False
            swap_hours = None
            
            # Live Nokia NaC RapidAPI check if configured
            if settings.NOKIA_RAPIDAPI_KEY and not settings.USE_MOCK_TELECOM:
                live_swap = await self._query_nokia_rapidapi_sim_swap(phone)
                if live_swap is not None:
                    sim_swapped = live_swap.get("swapped", False)
                    swap_hours = live_swap.get("hours", None)
                else:
                    # Deterministic fallback if carrier API unavailable or unsubscribed
                    sim_swapped = phone.endswith("99")
                    swap_hours = 1.5 if sim_swapped else None
            else:
                # Deterministic simulation based on number pattern
                # Numbers ending in '99' simulate a recent SIM swap for manual testing
                if phone.endswith("99"):
                    sim_swapped = True
                    swap_hours = 1.5
                else:
                    sim_swapped = False
                    swap_hours = None
                    
            self._sim_swap_cache[phone] = {"swapped": sim_swapped, "hours": swap_hours}
            
        # Numbers ending in '00' simulate active phone call (Scam Signal)
        is_on_call = phone.endswith("00")
        
        # Roaming check based on country mismatch
        is_roaming = country == "AE" and carrier.startswith("stc")
        
        return CarrierSignalProfile(
            phone_number=phone,
            carrier_name=carrier,
            number_verified=not sim_swapped,
            sim_swapped_recently=sim_swapped,
            sim_swap_hours_ago=swap_hours,
            is_on_active_voice_call=is_on_call,
            is_roaming=is_roaming,
            roaming_country="AE" if is_roaming else None,
            device_match=not sim_swapped
        )

    async def _query_nokia_rapidapi_sim_swap(self, phone: str) -> Optional[Dict]:
        """Queries Nokia Network as Code RapidAPI passthrough endpoint with strict timeout."""
        import httpx
        url = f"{settings.NOKIA_API_BASE_URL}/passthrough/camara/v1/sim-swap/sim-swap/v0/check"
        headers = {
            "x-rapidapi-key": settings.NOKIA_RAPIDAPI_KEY,
            "x-rapidapi-host": "network-as-code.p.rapidapi.com",
            "Content-Type": "application/json",
            "User-Agent": "SafePayMENA/1.0"
        }
        payload = {"phoneNumber": phone, "maxAge": 240}
        try:
            async with httpx.AsyncClient(timeout=0.25) as client:
                resp = await client.post(url, json=payload, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    swapped = data.get("swapped", False)
                    return {"swapped": swapped, "hours": 2.0 if swapped else None}
        except Exception:
            pass
        return None


telecom_gateway = TelecomGateway()
