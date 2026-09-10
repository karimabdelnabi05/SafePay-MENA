# Activate Connected Judging on Render

Use the existing `safepay-mena-demo` web service. No new Blueprint or project is needed.

1. Confirm the latest release commit has deployed under the service's Events page.
2. Open **Environment** for the service and add or edit these values:

| Key | Value |
|---|---|
| `SAFEPAY_ENABLE_LIVE` | `true` |
| `NOKIA_RAPIDAPI_KEY` | The working RapidAPI key used for Network as Code |
| `GEMINI_API_KEY` | The working Gemini key |
| `SAFEPAY_JUDGE_ACCESS_CODE` | A private code you choose; minimum 8 characters, preferably 16 or more |
| `SAFEPAY_LIVE_RUN_LIMIT` | `4` |
| `SAFEPAY_LIVE_GLOBAL_LIMIT` | `12` |
| `SAFEPAY_DATABASE` | `:memory:` |

3. Select **Save, rebuild, and deploy** and wait for the service to become live.
4. Visit `/api/v1/health` on the demo URL. `mode` must be `SANDBOX_ENABLED`. This confirms configuration, not current provider availability.
5. In the app, choose **Connected: Nokia + Gemini**, enter the private judge code, and unlock.
6. Run **SIM-swap takeover** once. Check actual Nokia response statuses and final policy. Successful local runs used three Nokia tools and four Gemini turns; provider availability and agent choices can vary.

The `sync: false` entries in `render.yaml` prompt only on initial Blueprint creation. For an existing Blueprint, add these secret values manually in the service's Environment page. [Render Blueprint specification](https://render.com/docs/blueprint-spec#prompting-for-secret-values)

Render's environment save/deploy options are described in its [environment-variable guide](https://render.com/docs/configure-environment-variables#in-the-render-dashboard).

## Judge Access and Fallback

Supply the judge code through the organizer's private instructions or another private channel. Confirm field visibility before placing it in a submission field. Provider keys stay on the server; judges do not need their own accounts.

If the app shows an exhausted allowance, wait for the hourly window or select **Repeatable fixture**. Nokia HTTP 429 is a separate provider quota and is retained as unavailable evidence. A connection interruption offers **Reconnect to review**, which fetches the same run without another investigation.

Limits count connected workflow starts, including zero-call routine reviews, rather than individual HTTP requests. Number Verification includes several OAuth requests. A cancelled or unsuccessful run can still consume provider quota.

Use the included single-worker start command. Grants, runs and quotas are in memory and reset on service restart. These are demonstration controls, not production infrastructure.
