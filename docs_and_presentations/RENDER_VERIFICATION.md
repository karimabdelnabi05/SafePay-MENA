# Render Deployment Verification

## Post-Merge Submission Check: 10 September 2026

PR #10 merged as `71d2ed2`. It only formats imports in the build scripts and local launcher. Subsequent public verification returned healthy with `SANDBOX_ENABLED`, both provider configuration flags true and `production_networks=false`. Hosted JavaScript and CSS matched the local application assets. A routine fixture payment completed with zero external calls, the Quality suite returned 36 passed and zero failed, and the mobile Quality view had no horizontal overflow. GitHub opened without authentication. This check made no Nokia or Gemini requests; the connected provider evidence below is from the earlier verified run.

The tracked-file scan, including extracted PDF text, found no configured provider credentials, judge access code or removed personal reference. The final source archive receives a separate scan and extraction test during packaging; its adjacent manifest records the exact packaged commit.

Validation provenance: the local 88 backend and 26 browser tests passed. Ruff import formatting was corrected in PR #10. The no-mistakes tool's review/test workers failed on Windows, so its corresponding stages were skipped after direct checks. GitHub reports no CI status checks on PR #10. The tool's `checks-passed` outcome is not evidence of a GitHub CI test run.

## Final Investigation Release: 10 September 2026

The public Render service was verified after the investigation and quota release deployed.

- The served JavaScript asset matched the release exactly.
- A single access-controlled SIM-swap investigation returned BLOCK. SIM Swap, Number Verification and Device Swap each returned SUCCESS with HTTP 200 from the Nokia sandbox; Gemini made four model requests.
- The allowlisted trace export did not contain the configured Nokia key, Gemini key or judge access code.
- The hosted Quality view returned 36 fixture cases passed and zero failed. This suite is regression evidence only and does not call live providers or measure fraud-model accuracy.
- The 375 x 812 connected investigation and Quality views had no horizontal overflow.

This is a working connected-sandbox prototype. It does not connect to a bank ledger or move funds, and one successful run does not establish production reliability or remaining provider quota.

## Connected Browser Review: 10 September 2026

The later hosted deployment was verified as `SANDBOX_ENABLED`, with both providers configured. The earlier fixture-only observations below are historical.

- Routine payment: APPROVE, zero external calls.
- SIM-swap takeover: BLOCK; Number Verification, SIM Swap and Device Swap all returned HTTP 200. Browser elapsed time was 6.53 seconds for this one run, not a performance benchmark.
- Stolen card: BLOCK; three successful Nokia observations, 6.33 seconds.
- Subsequent travel, suspicious transfer and first-setup attempts returned RETRY on unavailable evidence. Nokia SIM Swap and Roaming returned HTTP 429. Number Verification's older OAuth error handling lost the status of its failing intermediate request.
- The 36-case fixture evaluation passed, but a controlled browser-only failed response exposed hard-coded PASS/4-of-4 labels. The expanded table overflowed a 375-pixel mobile viewport.
- The investigation/UX release fixes those observed UI/diagnostic issues and adds conservative quota handling. It is documented in [release verification](INVESTIGATION_UX_RELEASE.md). See that document for the latest release's deployment status.

## Release Check: 10 September 2026

- Connected implementation commit `93cc428` was pushed and confirmed on GitHub main. Local verification passed 79 backend tests and 24 browser tests against a fresh server. Ruff, Bandit and pip-audit passed.
- The committed source archive was extracted and all 79 backend tests passed there too. `dist/SafePay_MENA_Source.manifest.json` records the packaged commit and checksum; regenerate it after later commits.
- At this public check, Render still served the previous release: the JavaScript did not match the pushed file and `GET /api/v1/live-access` returned 404.
- Public health remained `healthy`, `FIXTURE_ONLY`, `nokia_configured=false`, `gemini_configured=false`, `production_networks=false`.
- All 36 public fixture API journeys again passed, and the hosted evaluation returned 36 passed, zero failed. No external provider calls were made.
- The public browser check reproduced the earlier first-load failure: an immediate review returned to `Ready for review` instead of completing. The corrected first-load behavior passed locally; it must not be reported as deployed yet.
- Hosted connected verification remains pending. Use the existing service's Environment settings and **Manual Deploy > Deploy latest commit** if auto-deploy has not started. See [activation steps](RENDER_CONNECTED_SETUP.md).

The following sections preserve the earlier deployment baseline, not the status of the new code.

Verified 9 September 2026: https://safepay-mena-demo.onrender.com/

## Hosted Deployment

- Health returned `healthy`, `FIXTURE_ONLY`, `nokia_configured=false`, `gemini_configured=false`, `production_networks=false`.
- All 36 hosted scenario journeys passed using independent HTTP sessions: 12 scenarios in each of Egypt, Saudi Arabia and UAE. Checks covered expected decisions, exact logical evidence tools, evidence status and zero external calls.
- The hosted evaluation endpoint returned 36 passed and 0 failed.
- A request to start Nokia sandbox mode returned HTTP 403, as configured.
- The original 19-test browser suite returned 16 passed and 3 failed. All failures involved clicking the initial routine review before the catalog finished loading, at desktop, portrait-mobile and landscape-mobile sizes. Some tests intentionally mock responses to exercise frontend error handling.

## First-Load Defect

The review button was enabled before the asynchronous catalog arrived. A quick click submitted an empty scenario, and the API correctly returned HTTP 422 with `Unknown scenario`. The UI returned to the ready state with an error. This was reproduced against the hosted deployment and then captured with two controlled browser regressions for delayed and failed catalog loading.

The local correction disables the initial submit button in HTML, locks the form during initialization and guards submission until initialization succeeds. Failed initialization keeps the form locked. A pending review also rejects duplicate submissions.

After correction, all 75 backend tests and all 21 browser tests passed locally, including the two new regressions. This result does not mean the correction is deployed: a repository push and Render redeploy are still required.

## Judging Assessment

The hosted service is an interactive fixture prototype. It does not invoke Gemini or Nokia. The next functional improvement is protected connected-sandbox access with usage limits and explicit provider availability. Presentation and UI must distinguish deterministic simulated evidence from actual requests to Nokia simulator subjects. Production bank execution and real subscriber access remain outside this prototype.

The checks did not measure cold-start duration or production capacity. No live provider requests or real payments were made during deployment verification.
