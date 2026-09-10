# Customer Trust Establishment

Status: Draft. Mandatory first-time setup and new-device checks are user requirements; the exact API set and recovery policy below are proposals pending capability verification and product decisions.

## Purpose and trigger

Establish or renew device/session trust before a customer can use the routine-payment fast path. Applies to the simulated payment-app integrations for Egypt, Saudi Arabia, and the UAE, not a claim about the internal implementation of InstaPay or other named apps.

Accepted triggers:

- First-time payment-app account setup/enrollment.
- Registration of a new phone/device for an existing customer.

Proposed interpretation: reinstalling the application requires this workflow when it loses the valid device binding and needs re-enrollment. An app download alone is not an observable authenticated enrollment event. Device-change signals must come from server-held registration state and validated credentials, not a client boolean or user-agent string alone.

Phone-number changes and account recovery are candidate additional mandatory triggers, not yet an exhaustive agreed policy.

## Proposed execution contract

1. Store an enrollment attempt with customer reference, country/channel, proposed device credential, expected bank-bound phone reference, and idempotency key. Keep the new binding untrusted.
2. Enforce a mandatory fresh-evidence requirement before considering any routine-payment pre-call score. Old clean payment-cache entries cannot satisfy this requirement.
3. Proposed baseline evidence: Number Verification through a supported consent/authentication flow plus a fresh SIM Swap check. Validate actual Nokia entitlement and test flows before treating either as executable. These checks complement host-app identity/authentication requirements; they do not replace KYC or prove card ownership.
4. The controlled agent must satisfy the mandatory evidence set and can select relevant additional supported tools based on observations. It cannot skip required evidence to reduce cost. A new-device event does not mean calling every available API or querying voice-call status automatically.
5. Store each observation with subject, source mode, request reference, observation time, freshness, and success/unknown/error state. Bind authentication callbacks and evidence to the same enrollment attempt. Deduplicate retries without reusing unrelated enrollment evidence.
6. Evaluate the evidence and host authentication under enrollment policy. A legitimate new phone is not automatically fraud; a recent SIM change is a risk signal requiring contextual assessment, not proof of takeover.
7. Only successful completion creates an active binding and its evidence references. Define expiry, revocation, and re-verification rules before implementation is considered complete. Eligible later payments enter the separate payment-screening workflow.

When a required API is unavailable, unsupported, or inconclusive, do not silently establish trust. Keep the attempt unresolved and offer a supported recovery/retry route. Whether an independently verified host-bank recovery route may substitute for telecom evidence remains an explicit policy decision. Do not trap a legitimate customer in repeated automatic API calls.

## Customer experience and demo honesty

- Present a single setup/verification experience, with clear pending, completed, unavailable, and recovery states. Do not expose technical risk scores in the customer flow.
- Preserve completed checks within the same valid attempt when retrying an independent failure; recheck evidence that has become stale.
- Keep routine payments free of additional SafePay challenges when the payment-screening policy permits it. Enrollment approval does not permanently establish that all future payments are safe.
- The current web demo has no native Secure Enclave/Android Keystore integration. Any simulated device binding must be labeled as simulation in technical evidence; an actual WebAuthn implementation would be a distinct implementation choice, not proof of native hardware attestation.
- Provider sandbox responses, local fixtures, and real operator observations must remain distinguishable. No synthetic success may replace a failed live observation without an explicit mode change.

## Acceptance scenarios

1. First-time setup with a low local risk score still invokes required available verification tools; it cannot use the payment fast path.
2. A new-device enrollment with an old cached clean SIM result requests fresh evidence.
3. A legitimate new-device enrollment can complete after required evidence and host authentication succeed.
4. An unavailable mandatory check leaves the new device untrusted and presents a recoverable state, not an approval or fraud accusation.
5. Duplicate requests do not create duplicate bindings or concurrent duplicate provider calls. Expired evidence still requires refresh.
6. Successful enrollment followed by a routine eligible payment makes zero optional CAMARA and model calls during that payment.
7. A forged device-trust flag, replayed callback, or client-reported authentication success cannot establish trust.

## Decisions still open

- Exact available API products, authentication flows, and enrollment evidence requirements.
- Binding implementation, lifetimes, and revocation policy for the demo.
- Recovery and review conditions for legitimate SIM replacement, unsupported verification, and failed checks.
- Agent action authority and bounded execution budgets.

## Sources

- User clarification: Nokia key only; new phone and first-time installation/setup require API checks.
- [Mentor readiness checklist](../MENTOR_MEETING_READINESS_CHECKLIST.md), Pillar 3: device trust and selective checks.
- [Master plan](../SAFEPAY_MASTER_PROJECT_PLAN.md): login/re-enrollment versus transaction-time trigger placement.
- [Payment fraud investigation](payment-fraud-investigation.md): selective screening and final risk assessment.
