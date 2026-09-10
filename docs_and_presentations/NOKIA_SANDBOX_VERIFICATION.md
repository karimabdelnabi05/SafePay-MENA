# Nokia Sandbox Verification

Verified September 8, 2026. Preparation only: no application implementation changes.

## Scope and credentials

Requests used the replacement `NOKIA_RAPIDAPI_KEY` loaded through the existing application Settings from local configuration. Keys, client credentials, authorization codes, and tokens are not included in this report or saved by the probes. Requests targeted documented simulated phone numbers only. No webhook subscriptions, real subscriber checks, bank integrations, or money movements were performed.

Verified RapidAPI transport:

- Base URL: `https://network-as-code.p.rapidapi.com`
- Routing header: `x-rapidapi-host: network-as-code.p.rapidapi.com`
- Authentication: `x-rapidapi-key`, kept private.
- Probe timeout: 15 seconds; automatic redirects disabled and OAuth redirects handled explicitly.

This working route supersedes earlier assumptions that the application's RapidAPI hostname must be changed merely because another Nokia SDK deployment uses a different base URL or routing header. Do not interchange the Nokia portal and RapidAPI credentials without verifying their intended gateway.

## Observed results

All successful results below are provider simulator responses, not production carrier observations.

| Operation | Simulated input | HTTP | Observed response |
|---|---|---|---|
| SIM Swap check, prior verified run | `+99999991000`, maxAge 120 | 200 | `swapped: true` |
| SIM Swap check, prior verified run | `+99999991001`, maxAge 120 | 200 | `swapped: false` |
| SIM Swap retrieve date | `+99999991000` | 200 | `latestSimChange: 2026-09-08T16:36:39.914697Z` |
| Device Swap check | `+99999991000`, maxAge 120 | 200 | `swapped: true` |
| Device Swap check | `+99999991001`, maxAge 120 | 200 | `swapped: false` |
| Roaming retrieve | device phone `+99999991000` | 200 | `roaming: true`, `countryCode: 36`, `countryName: ["HU"]` |
| Reachability retrieve | device phone `+99999991000` | 200 | `reachable: true`; connectivity and lastStatusTime fields also present |
| Number Verification, without OAuth | `+99999991000` | 401 | `Authorization header is missing` |
| Number Verification, completed fast OAuth flow | `+99999991000` | 200 | `devicePhoneNumberVerified: true` |
| Number Verification, completed fast OAuth flow | `+99999991001` | 200 | `devicePhoneNumberVerified: false` |
| Unconditional Call Forwarding | `+99999991111` | 200 | `active: true` |
| OAuth server discovery | no subscriber input | 200 | issuer, authorization/token endpoints and fast-flow endpoint returned |
| OpenID discovery | no subscriber input | 200 | same endpoint fields returned |
| OAuth client credentials | authenticated application | 200 | client ID and client secret present, kept in memory only |

Representative individual request times: SIM date 599 ms; Device Swap 305/183 ms; Roaming 164 ms; Reachability 145 ms; Call Forwarding 196 ms. Previous SIM check requests took 1176/204 ms. These are individual observations, not p50/p99 benchmarks or production latency guarantees. The current adapter therefore uses multi-second request limits for sandbox reliability.

## Exact verified endpoint paths

Paths relative to the verified RapidAPI base URL:

| Operation | Method | Path |
|---|---|---|
| SIM Swap check | POST | `/passthrough/camara/v1/sim-swap/sim-swap/v0/check` |
| SIM Swap date | POST | `/passthrough/camara/v1/sim-swap/sim-swap/v0/retrieve-date` |
| Device Swap check | POST | `/passthrough/camara/v1/device-swap/device-swap/v1/check` |
| Roaming | POST | `/device-status/device-roaming-status/v1/retrieve` |
| Reachability | POST | `/device-status/device-reachability-status/v1/retrieve` |
| Number Verification | POST | `/passthrough/camara/v1/number-verification/number-verification/v0/verify` |
| Unconditional Call Forwarding | POST | `/passthrough/camara/v1/call-forwarding-signal/call-forwarding-signal/v0.3/unconditional-call-forwardings` |
| OAuth discovery | GET | `/.well-known/oauth-authorization-server` |
| OpenID discovery | GET | `/.well-known/openid-configuration` |
| OAuth client credentials | GET | `/oauth2/v1/auth/clientcredentials` |

The client-credentials operation can return existing credentials or create them if absent, per the local SDK description. The response does not identify which occurred in this run.

## Number Verification authorization

1. Retrieve application client credentials through the authenticated gateway.
2. Discover the fast-flow authorization endpoint. The observed host was `nb-auth.nac-runtime-stg-eu.g002.saas.nokia.com`, with path `/oauth2/v1/retrieve_csp_auth_url`.
3. Send client ID, `response_type=code`, `scope=dpv:FraudPreventionAndDetection number-verification:verify`, simulator `login_hint`, `prompt=none`, random state and nonce, and a loopback callback URI.
4. Follow only the observed Nokia authorization hosts. The simulator redirected through `camara-auth.nac-runtime-stg-eu.g002.saas.nokia.com/camara/oauth2/v1/authorize`, then to the loopback callback with a code and matching state.
5. Intercept the callback Location without making a request to the loopback address; validate its state. This was an isolated verification probe, not an implemented application callback server.
6. POST the same simulator phone number to the verify endpoint with the returned `code` and `state` as query parameters, using the application RapidAPI headers. Nokia performs token exchange in this fast flow.
7. Repeat with a fresh authorization attempt for the negative simulator case. Both produced the expected boolean.

Do not transfer this server-driven simulator probe into a production identity-verification claim. Real Number Verification requires its supported device/network authorization and consent flow. The prototype adapter binds a fresh random state and nonce, validates the loopback callback, restricts redirect hosts, and never exposes the authorization code. A production callback, token lifecycle, consent UX, expiry, and replay controls still require provider-specific implementation and testing.

## Integrated end-to-end verification - 9 September 2026

The assembled SafePay API was started locally with live mode explicitly enabled.

| Workflow | Result |
|---|---|
| SIM-takeover payment | Gemini selected SIM Swap, Number Verification, Device Swap and Roaming; all four Nokia sandbox observations returned SUCCESS; deterministic policy returned BLOCK with final score 90 |
| First-time enrollment | Number Verification and SIM Swap both returned SUCCESS; mandatory enrollment policy returned TRUST_ESTABLISHED |
| Invalid model turn | The first controlled payment attempt returned RETRY with POLICY_FAIL_CLOSED and made no Nokia calls |

The successful payment workflow used five Gemini turns and four logical Nokia tool calls and completed in approximately 6.4 seconds. Enrollment used two logical Nokia tools and completed in approximately 1.9 seconds. These are single local observations, not performance benchmarks.

## Remaining boundaries

- Call Forwarding is not active-call detection or a Scam Signal verdict. No active-call/scam-detection tool was found in the inspected local SDK; none was verified in these requests.
- Device Swap indicates a device-change event within a time window. It does not directly prove that a handset is the application's registered trusted device.
- Simulator IDs encode predetermined per-API responses. They do not establish a coherent real customer's identity or attack history across APIs.
- Production access and coverage for Egypt, Saudi Arabia, and the UAE remain unverified.
- The current prototype now includes bounded Gemini tool orchestration, explicit source/subject labeling, pre-call screening, enrollment, unknown/failure handling, stored decisions, protected judge access, hourly usage limits, live progress, and HTTP/browser acceptance tests. Hosted activation, production readiness, calibrated fraud accuracy, and operator-specific consent remain future work.
- No additional user portal action was required to complete the tested simulator flows. Old exposed-key revocation remains a separate security housekeeping task; it has not been confirmed.

## Rate-limit QA follow-up - 9 September 2026

A later controlled run completed live first-time enrollment with successful Number Verification and SIM Swap observations, then completed a suspicious-transfer investigation with two successful observations. The RapidAPI free plan subsequently returned HTTP 429 for SIM Swap, Device Swap, Roaming, Reachability, and the first Number Verification credential request.

The adapter preserved those responses as `UNKNOWN` evidence without exposing provider bodies or credentials. The run also revealed that an earlier policy branch allowed a Gemini protective `BLOCK` proposal to strengthen a deterministic non-block when provider evidence was unavailable. That branch was removed: Gemini can now request review, but only deterministic evidence policy can produce `BLOCK`. A regression test reproduces HTTP 429 and requires `RETRY`.

No further live calls were made after the limit was isolated. This result demonstrates failure handling, not successful availability of every tool on every run.

## Protected connected judge-path verification - 10 September 2026

The new protected, asynchronous browser path was exercised locally with the configured Gemini and Nokia credentials. The access code remained server-side, the browser received only an HttpOnly grant, and the UI polled stored progress while the provider work ran in the background.

In the final controlled SIM-takeover run, Gemini autonomously selected SIM Swap, Number Verification and Device Swap from the contextually eligible tool set. All three Nokia sandbox observations returned `SUCCESS`. Deterministic policy returned `BLOCK` with a pre-call score of 80 and final risk score of 90. The run used four Gemini turns and three logical CAMARA calls and completed in under ten seconds end to end. This is one sandbox observation, not a production latency benchmark.

An earlier run exposed that offering every supported API on every turn encouraged unnecessary Roaming and Reachability calls. The investigator now limits declarations by observable context and removes tools after use: Roaming is eligible only for travel context, Device Swap only for a session anomaly, and Reachability only for an explicit connectivity concern. Gemini still chooses the order and whether to finish; server policy controls eligibility, call budgets and the final disposition.

Automated coverage now verifies access control, per-session quota enforcement, asynchronous progress, Nokia source labels, legacy-endpoint quota-bypass prevention, cancellation before a selected Nokia call, and fixture-mode regressions. Hosted deployment remains pending, so this section does not claim that the public Render URL is connected yet.

## Sources

- Local Nokia Python SDK under `references/nokia-nac-sdks/network-as-code-py/network_as_code/` and its `integration_tests/` fixtures.
- [Nokia Number Verification V1 documentation](https://networkascode.nokia.io/_docs/number-verification/number-verification-v1).
- Sanitized direct request results observed in this verification session.
