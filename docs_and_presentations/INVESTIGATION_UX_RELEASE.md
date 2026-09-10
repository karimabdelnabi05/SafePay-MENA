# Investigation and Quota Release

## Changes

- Payment and Quality checks are separate keyboard-accessible views. Sample transactions remain explicitly synthetic; no real payment rail was connected.
- The regression table displays each returned case/check result instead of hard-coded PASS labels and remains horizontally contained on mobile.
- The live timeline includes selection rationale, time, provider errors and bounded model retries. Policy overrides identify both the proposed and enforced decisions.
- Incomplete investigations show Incomplete and Not assessed rather than a falsely final risk score.
- Investigation details expose the run ID, model requests/turns, network checks, missing/unavailable evidence and failing provider step. Export trace includes only allowlisted result fields, never provider request headers or credentials.
- Nokia rate limiting stops additional work and starts a conservative shared cooldown. The panel distinguishes that status from SafePay's own allowance. See [quota options](NOKIA_QUOTA_OPTIONS.md).
- Gemini transport failures and HTTP 502/503/504 receive at most one retry per turn within seven total model requests and the existing 45-second investigation deadline. HTTP 429 is not automatically retried. Cancellation is checked before retries; the test transport follows the production path.

## Verification

Local release checks passed 88 backend/adapter tests and 26 browser tests (114 total). Browser coverage includes a deliberately failed evaluation response, model/policy disagreement, unavailable OAuth evidence, trace export, tab navigation and desktop/mobile layout. The 36-case evaluation remains a synthetic fixture suite, not a live-provider health check or fraud accuracy claim.

Desktop 1440 x 1000, mobile 375 x 812 and landscape 812 x 375 were inspected. Recorded-run layout replays used only scratch captures and are not new live-provider evidence.

The final release was also checked on the public Render deployment. Its JavaScript asset matched this release. One access-controlled SIM-swap investigation returned `BLOCK` after three Nokia sandbox observations: SIM Swap, Number Verification and Device Swap each returned HTTP 200. Gemini made four model requests. The exported trace contained no configured provider credentials or access code. The hosted 36-case fixture evaluation returned 36 passed and zero failed, and its 375-pixel mobile view had no horizontal overflow. This is bounded deployment evidence, not a guarantee of production availability, fraud accuracy or remaining Nokia quota.

Application implementation commit: `feddd37`, included in the current main branch. No new Render environment variables are required; the existing provider keys and judge code are retained. Never treat a local cooldown as confirmation of the provider's reset time.
