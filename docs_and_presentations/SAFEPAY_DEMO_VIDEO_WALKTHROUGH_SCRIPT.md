# SafePay MENA - Three-Minute Demo

## Before recording

- Start the app in fixture mode for a repeatable presentation.
- Keep the browser at 100% zoom and use a desktop viewport.
- Confirm the status reads `Service ready` and the badge reads `FIXTURE DEMO`.
- Keep a separately recorded, sanitized Nokia sandbox trace available if the live quota is unavailable.
- Do not describe fixtures as live operator data or claim that a payment is executed.

## 0:00-0:25 - Problem and product

"Instant-payment applications understand transaction context, while mobile networks can observe events such as SIM changes, number association, device changes, roaming, and reachability. SafePay brings those observations into the payment-release decision only when risk warrants it."

Show the market controls, payment channel, scenario, amount, and recipient relationship.

## 0:25-0:45 - Routine zero-call path

Select **Everyday payment** and click **Review payment**.

"This is a known recipient, usual amount, and established device. Local screening approves immediately. The pre-call and final scores are zero, and SafePay makes zero Gemini or CAMARA calls. We do not pay for or delay checks that are not needed."

Point to the decision, both scores, and the zero call counter.

## 0:45-1:10 - Mandatory first setup

Select **First-time setup** and click **Verify device**.

"Some events bypass risk scoring. A first installation or a new phone always requires fresh Number Verification and SIM Swap observations before device trust is established."

Open **Network evidence**, show the two fixture observations and their source labels, then click **Continue to payment**.

"Enrollment and payment stay in the same session. Once trust is established, the routine payment continues without another external investigation."

## 1:10-1:40 - Suspicious transfer

Select **Suspicious transfer** and click **Review payment**.

"The customer reports that a caller claiming to be the bank requested this transfer. Identity evidence can be clean while intent remains unsafe, so deterministic policy holds the payment rather than treating Number Verification as proof of consent."

Show **Why this happened**, then cancel the held review.

## 1:40-2:10 - SIM and device takeover

Select **SIM-swap takeover** and click **Review payment**.

"Here an unusual session combines with recent SIM and device changes. SafePay blocks the payment. Each observation shows its tool, source, status, and returned boolean. The system never invents an exact SIM-swap age from a boolean response."

Open **Network evidence** and **Agent and policy trace**. Explain that fixture mode is repeatable; live mode lets Gemini choose tools against Nokia's sandbox when quotas are available.

## 2:10-2:30 - Fail closed

Select **Network unavailable** and click **Review payment**.

"Timeouts, malformed responses, authorization failures, and rate limits become unknown evidence. Unknown never becomes safe. The result is RETRY, so the payment is not automatically released."

## 2:30-2:50 - Quality gate

Click **Run 36-case evaluation**.

"This quality gate runs 12 workflows for Egypt, Saudi Arabia, and the UAE. It verifies decisions, exact fixture tool plans, evidence status, and zero real external calls. It is software acceptance evidence, not a fraud-accuracy claim."

## 2:50-3:00 - Close

"SafePay keeps routine payments instant, orchestrates network evidence for elevated risk, and keeps final control in deterministic policy. Our next step is a measured pilot with one operator and one payment provider."

## Live sandbox Q&A

When live mode is available, state these boundaries before running it:

- Gemini selects from five allowlisted tools.
- Phone subjects and endpoint paths remain server controlled.
- Nokia calls use only documented simulator subjects.
- Simulator results are not production MENA operator observations.
- The free RapidAPI plan can return HTTP 429; SafePay will display unknown evidence and return RETRY.
