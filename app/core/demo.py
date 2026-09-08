"""Synthetic bank context and independent provider fixtures for repeatable demos."""

COUNTRIES = {"EG": {"name": "Egypt", "currency": "EGP", "rail": "InstaPay / IPN"},
             "SA": {"name": "Saudi Arabia", "currency": "SAR", "rail": "sarie"},
             "AE": {"name": "United Arab Emirates", "currency": "AED", "rail": "Aani"}}

SCENARIOS = {
    "routine": ("Everyday payment", "A familiar recipient, established device, usual amount.", "APPROVE"),
    "identity_mismatch": ("Number mismatch", "Number verification fails without other takeover signals.", "HOLD"),
    "first_setup": ("First-time setup", "A customer registers their payment app.", "TRUST_ESTABLISHED"),
    "new_device": ("New phone", "An existing customer registers a replacement phone.", "TRUST_ESTABLISHED"),
    "scam_transfer": ("Suspicious transfer", "A caller claiming to be the bank requests a transfer.", "HOLD"),
    "sim_swap": ("SIM-swap takeover", "An unusual session follows a SIM and device change.", "BLOCK"),
    "card_misuse": ("Stolen card attempt", "A new checkout session cannot verify the cardholder's bound number.", "BLOCK"),
    "combined_attack": ("Combined takeover", "A compromised card is used following a SIM change.", "BLOCK"),
    "legitimate_travel": ("Customer travelling", "A trusted customer is roaming on a planned trip.", "APPROVE"),
    "velocity": ("Repeated small transfers", "Several new recipients appear within a short window.", "HOLD"),
    "provider_outage": ("Network unavailable", "Required carrier evidence cannot be obtained.", "RETRY"),
    "enrollment_outage": ("Setup interrupted", "Verification is unavailable during registration.", "RETRY"),
}


def context_for(scenario):
    return {"session_anomaly": scenario in {"sim_swap", "card_misuse", "combined_attack"},
            "reported_bank_transfer_request": scenario == "scam_transfer",
            "travel_expected": scenario == "legitimate_travel",
            "recent_new_recipients": 6 if scenario == "velocity" else 0,
            "usual_amount": 500, "source": "SIMULATED_BANK_CONTEXT"}


def signals_for(scenario):
    if scenario in {"provider_outage", "enrollment_outage"}:
        return {"sim_swap": None, "number_verification": None}
    return {"sim_swap": scenario in {"sim_swap", "combined_attack"},
            "device_swap": scenario in {"sim_swap", "card_misuse", "combined_attack"},
            "number_verification": scenario not in {"card_misuse", "combined_attack", "identity_mismatch"},
            "roaming": scenario == "legitimate_travel", "reachability": True}
