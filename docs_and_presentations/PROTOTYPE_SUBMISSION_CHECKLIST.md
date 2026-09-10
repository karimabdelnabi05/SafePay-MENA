# Prototype Phase Submission Checklist

Saved from the user's submission form on 9 September 2026. This is the canonical checklist for completing the form and assembling its files. No submission has been sent by this checklist.

## Agreed Demo Requirement

The main judge experience must show genuine connected-sandbox execution, not just a predefined scenario outcome:

- [x] Local screening displays the pre-call risk and reasons before any external request.
- [x] Routine payments visibly complete with zero Gemini and Nokia calls.
- [x] Elevated risk invokes Gemini, which selects the next relevant Nokia tool from transaction facts and prior observations.
- [x] The backend makes actual Nokia sandbox requests; the UI shows tool, evidence source, status, returned observation and elapsed time.
- [x] The trace updates during investigation so judges can follow progress, rather than only receiving a final answer.
- [x] The agent can request further evidence or finish; enforced policy owns the final action and risk score.
- [x] First setup and a new phone always require fresh Number Verification and SIM Swap checks.
- [x] Connected mode is protected with judge access and usage limits; provider keys stay on the server.
- [x] Provider errors, missing evidence and quota failures remain visible. No silent switch to simulated evidence.
- [x] The existing deterministic mode remains available as an explicitly labeled fallback.

Test transactions and Nokia simulator subscribers are acceptable inputs to this agreed design. Real Gemini execution and real HTTP requests to Nokia are required for the connected demonstration. Neither mode transfers real money or establishes production operator access.

**Current status (10 September 2026):** Protected connected access is deployed on Render. A hosted SIM-swap investigation returned BLOCK with successful HTTP 200 responses from SIM Swap, Number Verification and Device Swap. Local verification passed 88 backend and 26 browser tests. The 36-case fixture evaluation also passed on Render. See [deployment verification](RENDER_VERIFICATION.md). Source ZIP provenance is recorded in its adjacent manifest. Required form uploads and the video URL still need to be completed.

## Form Checklist

An unchecked box means that field has not been confirmed as final and submitted. A draft or existing asset is not the same as a completed upload.

| Done | Form field | Required | Accepted content / limit | Current status and remaining action |
|---|---|---|---|---|
| [ ] | Title | Yes | Clear, descriptive title; no character limit supplied | Draft below. Confirm final wording. |
| [ ] | Description | Yes | Formatted text and links supported; no length limit supplied | Ready-to-paste wording below reflects the verified connected deployment. |
| [ ] | Parent Submission | Yes | Select an existing parent submission | User must select the original SafePay entry that advanced to Prototype Phase. Exact dropdown entry not supplied. |
| [ ] | Theme | Yes | Select from the form's available themes | Exact options not supplied. Select the option matching payment fraud / fintech security with Open Gateway and agentic AI; do not invent an option label. |
| [ ] | Snapshots | No asterisk shown | JPG, JPEG or PNG; up to 3 MB each. Image-count limit not supplied. | Refreshed desktop/mobile and actual local connected-result PNGs are ready; each is under 3 MB. Upload the chosen images. |
| [ ] | Video URL | Yes | Product demo or pitch video URL | No final hosted video URL recorded. Record the actual connected workflow, publish a reviewer-accessible video and test access. |
| [ ] | Presentation | Yes | .key, .odp, .odt, .pdf, .pps, .ppt or .pptx; max 50 MB | Updated single 17-slide PDF is ready, under 0.2 MB, with sourced business numbers, actual local connected capture and final technical summary. |
| [ ] | Demo Link | Yes | Working demo or prototype URL | Render connected sandbox is deployed and verified. Use the URL below. |
| [ ] | Repository URL | Yes | Source repository URL, such as GitHub or Bitbucket | Connected-demo release pushed to main. Test reviewer access before submission. |
| [ ] | Source Code | Yes | File upload, e.g. ZIP or APK; max 50 MB | `dist/SafePay_MENA_Source.zip` is prepared and tested after extraction. Its adjacent manifest records the exact commit and SHA-256. Upload the ZIP, not the manifest. |
| [ ] | Instructions to Run | Yes | Steps reviewers can follow to test the project | Draft below includes the implemented access procedure. Verify hosted connected mode and provide the code privately. |

The source-code upload is a separate required field: supplying a GitHub URL does not fill it. The video URL is also required, not merely an optional backup.

## Draft Title

**SafePay MENA: AI-Guided Fraud Checks for Instant Payments**

## Draft Description

The following wording reflects the verified hosted prototype.

> SafePay MENA is a working prototype that helps banks and wallets investigate risky payments while keeping routine payments free of unnecessary network checks.
>
> It combines transaction context with mobile-network evidence to support clear outcomes: approve, hold, block or retry. Demonstrated journeys include suspicious transfers, SIM-related account takeover, stolen-card attempts, legitimate travel, first-time setup and new-device registration, with market contexts for Egypt, Saudi Arabia and the UAE.
>
> Routine payments follow a local screening path without calling an AI model or telecom API. In connected-sandbox mode, a bounded Gemini agent chooses relevant CAMARA APIs through Nokia Network as Code, observes their responses and selects further checks when needed. Integrated capabilities include SIM Swap, Number Verification, Device Swap, Roaming and Reachability. Enforced policy controls the final decision, and unknown evidence is not treated as a clean result.
>
> The hosted prototype offers protected connected access with actual Gemini execution and Nokia sandbox HTTP requests, plus an explicitly labeled fixture mode for repeatable testing. Judges can follow tool selection, returned evidence, provider failures and the enforced decision, and export an investigation trace. The separate 36-case Quality suite checks software behavior using fixtures. No real payment is executed, and Nokia tests use simulator subscribers rather than production customer data.
>
> Our business proposal is a platform subscription plus investigation-based usage pricing. The presentation separates published market evidence, measured prototype results and financial assumptions to be validated in a bank pilot.
>
> Demo: https://safepay-mena-demo.onrender.com/
>
> Repository: https://github.com/karimabdelnabi05/SafePay-MENA

Provide the judge access code through a reviewer-only channel. Do not publish it in the description or repository.

## File and Link Locations

| Item | Location | Status |
|---|---|---|
| Demo | https://safepay-mena-demo.onrender.com/ | Deployed; protected connected sandbox and repeatable fixtures |
| Repository | https://github.com/karimabdelnabi05/SafePay-MENA | Connected-demo release pushed to main |
| Single presentation PDF | [SafePay_MENA_Phase2_Pitch_Deck.pdf](SafePay_MENA_Phase2_Pitch_Deck.pdf) | Exists; 17 slides, under 50 MB at this review |
| Editable presentation source | [SafePay_MENA_Phase2_Slides.html](SafePay_MENA_Phase2_Slides.html) | Source for the same PDF, not a second upload |
| Speaker notes and evidence | [PHASE2_PITCH_NOTES.md](PHASE2_PITCH_NOTES.md) | Internal preparation |
| Desktop screenshot | [safepay-desktop.png](../artifacts/safepay-desktop.png) | Refreshed fixture UI; under 3 MB |
| Mobile screenshot | [safepay-mobile.png](../artifacts/safepay-mobile.png) | Refreshed fixture UI; under 3 MB |
| Connected result screenshot | [safepay-connected-result.png](../artifacts/safepay-connected-result.png) | Actual local Gemini/Nokia run, not a hosted-production claim; under 3 MB |
| Held-payment screenshot | [pitch-hold.png](../artifacts/pitch-hold.png) | Actual fixture outcome capture |
| Video URL | Not yet available | Required |
| Source ZIP | `dist/SafePay_MENA_Source.zip` | Prepared, under 50 MB; clean extraction passes all 88 backend tests; exact commit in adjacent manifest |

Recommended final snapshots: a completed payment decision, the genuine connected investigation trace, and the evaluation or mobile experience. No fabricated API-success image. Use only the number of snapshots the form permits.

## Video Checklist

- [ ] Confirm any time limit from the organizer; none was supplied in this form.
- [ ] Explain the user problem and business value briefly before opening the product.
- [ ] Show a routine payment completing with zero external calls.
- [ ] Show genuine Gemini selection and Nokia sandbox responses during an elevated-risk investigation.
- [ ] Explain the final action in plain language and demonstrate hold/cancel or block.
- [ ] Identify simulator inputs and distinguish connected mode from fixture fallback.
- [ ] Show the mandatory setup/new-phone path if the allotted time permits.
- [ ] Show the acceptance evaluation without presenting it as fraud-detection accuracy.
- [ ] Hide keys, access codes, personal data and account dashboards from the recording.
- [ ] Host the final video and confirm that its URL opens and plays for an unauthenticated reviewer.

## Source ZIP Checklist

- [ ] Package the same release as the repository and deployed demo; record its commit SHA.
- [x] Include `app/`, relevant `tests/`, `requirements.txt`, `requirements-dev.txt`, `pytest.ini`, `run_dashboard.py`, `render.yaml`, `.env.example`, `README.md` and any final files required to run it.
- [x] Include supporting documentation deliberately; do not zip the entire desktop/workspace.
- [x] Exclude `.git/`, `.env`, real keys, OAuth credentials, token/cookie files, virtual environments, caches, scratch artifacts, downloaded reference repositories, mentor materials and unrelated research.
- [x] Confirm the tracked release and PDF text contain no current provider credentials or removed mentor reference; archive secret/path scan passed.
- [x] Extract it into a clean directory and run all 88 backend tests successfully. The startup tests verify clean fixture-mode import.
- [ ] Confirm size is below 50 MB and upload it in the Source Code field.

## Draft Instructions to Run

### Hosted Prototype: Available Now

1. Open https://safepay-mena-demo.onrender.com/ and allow the service to load.
2. Wait for the sample situations to load; the review button enables when ready.
3. Select Egypt, Saudi Arabia or UAE.
4. Choose a scenario and select **Review payment**, or **Verify device** for setup/new-phone scenarios.
5. Inspect the outcome, risk scores and reasons. Expand **Network evidence** and **Investigation details** for supporting observations and trace export.
6. For a held payment, use **Cancel review** to demonstrate cancellation.
7. Open **Quality checks**, then run the evaluation to check 36 repeatable synthetic workflows.

The default **Repeatable fixture** mode uses simulated inputs and telecom responses without external Gemini/Nokia calls. The connected option below makes provider requests. No money moves in either mode.

### Connected Judge Experience: Available Now

1. Obtain the private judge access code from the submission instructions or team; no provider account is required.
2. Open the demo and select **Connected: Nokia + Gemini** under **Evidence mode**.
3. Enter the judge code and select **Unlock connected mode**. The panel shows the remaining hourly run allowance.
4. Select **SIM-swap takeover** and run the review. Watch the connected timeline show local screening, Gemini tool selection, Nokia simulator responses and deterministic policy.
5. Expand **Network evidence** to inspect `NOKIA_SANDBOX` source labels and returned observations. Agent-selected tool order can vary; do not expect an identical sequence on every run.
6. If a provider or quota error occurs, the outcome remains `RETRY` or fail-closed and never switches silently to fixtures. Select **Repeatable fixture** explicitly for the offline fallback.
7. The prototype uses synthetic bank inputs and Nokia simulator subjects. No money moves and no production subscriber is queried.

### Run the Current Source Locally

From an extracted source archive or cloned repository, with Python and pip installed:

```bash
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Install and start:

```bash
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000/. A clean environment runs fixture mode without provider credentials.

For optional local connected-sandbox testing, configure `NOKIA_RAPIDAPI_KEY`, `GEMINI_API_KEY`, `SAFEPAY_JUDGE_ACCESS_CODE` and `SAFEPAY_ENABLE_LIVE=true` privately using `.env.example` as the template, then restart. All four values are required. Provider access and quota must be valid; Nokia simulator subjects are used. Reviewers should not need this setup after the hosted connected demo is verified.

For automated backend checks:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q --ignore=tests/test_browser.py
```

Browser-test setup and commands are in the README. Final run instructions must be retested against the submitted ZIP, not only the working directory.

## Final Submission Gate

- [ ] All required fields above are completed.
- [ ] Correct parent submission and actual theme dropdown option selected.
- [x] Final first-load fix and connected-demo changes deployed and verified.
- [ ] Demo, video, presentation, repository and source ZIP describe the same release and mode boundaries.
- [ ] No simulated response is presented as an actual Nokia result; no synthetic QA result is presented as real-world fraud accuracy.
- [ ] Presentation is the single agreed PDF and under 50 MB.
- [ ] Every snapshot is an allowed image format and under 3 MB.
- [ ] Source ZIP is under 50 MB, complete, clean and runnable.
- [ ] Video, demo and repository links work from a fresh browser session.
- [ ] Review the full submission preview and record the successful submission confirmation.
