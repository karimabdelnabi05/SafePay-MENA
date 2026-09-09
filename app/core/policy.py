"""Explainable demo heuristics, not calibrated fraud probabilities or legal rules."""


def screen(context, amount, recipient):
    reasons = []
    if recipient != "family":
        reasons.append((20, "Recipient has no established relationship"))
    if amount > context["usual_amount"] * 3:
        reasons.append((25, "Amount exceeds the customer's usual range"))
    if context["session_anomaly"]:
        reasons.append((35, "Unusual authenticated session"))
    if context["reported_bank_transfer_request"]:
        reasons.append((45, "Customer reports a caller requesting a bank transfer"))
    if context["recent_new_recipients"] >= 3:
        reasons.append((40, "Several new recipients in a short period"))
    if context.get("recent_attempts", 0) >= 5:
        reasons.append((40, "Unusual payment-attempt velocity"))
    if context["travel_expected"]:
        reasons.append((15, "Travel context needs confirmation"))
    return min(100, sum(score for score, _ in reasons)), [reason for _, reason in reasons]


def assess(context, evidence):
    observed = {e["tool"]: e["data"] for e in evidence if e["status"] == "SUCCESS"}
    swap = observed.get("sim_swap", {}).get("swapped")
    number = observed.get("number_verification", {}).get("devicePhoneNumberVerified")
    device = observed.get("device_swap", {}).get("swapped")
    reasons = list(context.get("pre_call_reasons", []))
    pre_call_score = int(context.get("pre_call_score", 0))
    evidence_score = 0
    if context["session_anomaly"]:
        evidence_score += 25
        reasons.append("Independent session anomaly")
    if swap is True:
        evidence_score += 40
        reasons.append("SIM change within the checked 120-hour window; exact age unknown")
    if number is False:
        evidence_score += 55
        reasons.append("Verified bearer does not match the expected phone number")
    if device is True:
        evidence_score += 25
        reasons.append("Device change within the checked window")

    # Pre-screen context remains relevant after clean identity evidence, but it
    # cannot independently manufacture a high-confidence network block.
    score = max(evidence_score, min(pre_call_score, 60))
    reasons = list(dict.fromkeys(reasons))
    if evidence_score >= 70:
        return "BLOCK", min(score, 100), reasons
    if swap is None or number is None:
        return "RETRY", min(score, 100), reasons + ["Required evidence is missing or unavailable"]
    transaction = context.get("transaction", {})
    high_value_new_payee = (
        transaction.get("recipient_relationship") == "new_payee"
        and transaction.get("amount", 0) > context["usual_amount"] * 3
    )
    if (context["reported_bank_transfer_request"] or context["recent_new_recipients"] >= 3
            or context.get("recent_attempts", 0) >= 5 or high_value_new_payee):
        return "HOLD", max(score, 55), reasons + ["Identity checks do not establish safe payment intent"]
    if swap or number is False or device is True or context["session_anomaly"]:
        return "HOLD", max(score, 40), reasons + ["Further review is needed before release"]
    return "APPROVE", score, reasons + ["Required observations returned no blocking evidence"]
