# Nokia Quota and Access Options

Reviewed 10 September 2026 against Nokia's official documentation and actual SafePay hosted results.

## Current Connection

SafePay already calls Nokia Network as Code through `network-as-code.p.rapidapi.com`. Nokia's product and RapidAPI's gateway are not two interchangeable unlimited providers. Gemini has a separate account, bill and quota.

Hosted SIM Swap, Device Swap and Number Verification succeeded during the 10 September browser review. Later Nokia requests returned HTTP 429. That status alone does not establish the applicable per-second, per-minute, daily or subscription limit, nor its reset time.

## Portal Access

Nokia's [getting-started guide](https://networkascode.nokia.io/_docs/getting-started) documents application keys obtained from the Nokia portal and an SDK example using `network-as-code.nokia.rapidapi.com`. Its [portal update](https://networkascode.nokia.io/blog/q3-2025-network-as-code-developer-portal-updates) describes free test-mode access. Neither page establishes that this project's portal key has the same five API subscriptions, compatible endpoint versions, larger quotas or production permissions.

Do not substitute keys or hosts blindly, and do not rotate keys to evade a quota. Before a separate portal adapter is enabled, verify the application's subscriptions, allowed gateway, endpoint versions, authentication and simulator subjects with Nokia. No provider switch or billing change is part of this release.

## Next Steps for the Team

1. Open the current RapidAPI Network as Code subscription's usage and plan information. Check the actual request allowance, rate limit, reset time and whether a larger authorized plan is available. No paid plan is assumed or purchased here.
2. Ask the Nokia/GSMA hackathon contact for a demo allowance or confirmation that the existing Nokia portal application is entitled to the required APIs.
3. If portal access is proposed, share the non-secret endpoint examples, API versions and plan limits with the developer. Store its key privately in the local environment only after an explicit configuration is agreed.
4. Retest one connected workflow after allowance is confirmed. Do not run the entire 36-case synthetic suite against live providers merely for a green table.

Suggested message:

> We are demonstrating SafePay MENA in the GSMA MENA Ignite prototype phase. Our Nokia Network as Code sandbox calls succeed but later receive HTTP 429 via RapidAPI. Could you confirm the rate/request limits and reset window, and provide a hackathon demo allowance? We use SIM Swap, Number Verification (including its OAuth requests), Device Swap, Roaming and Reachability. We also have a Nokia portal application; please confirm whether those APIs can be enabled there and which gateway, API versions and quota apply. We can provide a sanitized trace privately.

## Implemented Protection

SafePay records Nokia 429, the failing API/OAuth path and safe HTTP metadata. It stops further checks and model calls for the investigation, then applies a conservative provider-wide cooldown shared within its single server process. `Retry-After` is used when valid; otherwise a 60-second local pause is used. This is not a guarantee that provider quota resets after 60 seconds. No requests are automatically retried when the cooldown expires.

The access panel distinguishes SafePay's run allowance from Nokia's last observed availability. Refreshing that panel reads local status only and does not consume Nokia quota. Routine locally screened payments remain zero-call. There is no silent fallback to fixture evidence.

Number Verification can make several OAuth HTTP requests for one logical capability check. Plan usage should therefore be checked in the provider dashboard, not inferred from the app's network-check count. Cooldowns and demo grants reset when this single-worker, in-memory demo restarts; they are not a production distributed rate limiter.
