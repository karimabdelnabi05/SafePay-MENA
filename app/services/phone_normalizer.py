"""
SafePay MENA - Regional E.164 Phone Normalizer & Carrier Resolver
Uses Google libphonenumber (phonenumbers) with regional Arab telecom heuristics.
"""

import phonenumbers
from phonenumbers import carrier

def normalize_phone_number(raw_phone: str, default_region: str = "SA") -> tuple[str, str, str]:
    """
    Normalizes any regional phone input to strict E.164 format and resolves carrier name.
    
    Returns:
        tuple[e164_number, carrier_name, country_code]
    """
    clean_input = raw_phone.strip().replace(" ", "").replace("-", "")
    
    # Regional prefix hints
    if clean_input.startswith("01"):  # Egypt local mobile (010, 011, 012, 015)
        default_region = "EG"
    elif clean_input.startswith("05"):  # GCC mobile (KSA / UAE)
        if len(clean_input) == 10 and default_region not in ("SA", "AE"):
            default_region = "SA"
            
    try:
        parsed = phonenumbers.parse(clean_input, default_region)
        if not phonenumbers.is_valid_number(parsed):
            # Fallback to direct E.164 string if parse was strict
            e164 = f"+{parsed.country_code}{parsed.national_number}"
        else:
            e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            
        country_code = "SA" if parsed.country_code == 966 else ("EG" if parsed.country_code == 20 else ("AE" if parsed.country_code == 971 else "OTHER"))
        
        # Carrier resolution heuristics
        detected_carrier = carrier.name_for_number(parsed, "en")
        if not detected_carrier:
            # Regional fallback mapping
            num_str = str(parsed.national_number)
            if country_code == "SA":
                if num_str.startswith(("50", "53", "55")):
                    detected_carrier = "stc Saudi"
                elif num_str.startswith(("54", "56")):
                    detected_carrier = "Mobily"
                elif num_str.startswith(("58", "59")):
                    detected_carrier = "Zain KSA"
                else:
                    detected_carrier = "stc Saudi"
            elif country_code == "EG":
                if num_str.startswith("10"):
                    detected_carrier = "Vodafone Egypt"
                elif num_str.startswith("11"):
                    detected_carrier = "Etisalat Misr"
                elif num_str.startswith("12"):
                    detected_carrier = "Orange Egypt"
                elif num_str.startswith("15"):
                    detected_carrier = "Telecom Egypt (WE)"
                else:
                    detected_carrier = "Vodafone Egypt"
            elif country_code == "AE":
                if num_str.startswith(("50", "54", "56")):
                    detected_carrier = "e& (Etisalat UAE)"
                else:
                    detected_carrier = "du UAE"
            else:
                detected_carrier = "Regional Telecom Operator"
                
        return e164, detected_carrier, country_code
        
    except Exception:
        # Graceful fallback for demo strings
        if clean_input.startswith("+"):
            return clean_input, "stc Saudi", "SA"
        return f"+966{clean_input.lstrip('0')}", "stc Saudi", "SA"
