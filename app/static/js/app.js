const state = {
  catalog: null,
  ready: false,
  country: "EG",
  currentRun: null,
  sessionSignature: null,
  enrolled: false,
  pending: false,
  operationGeneration: 0,
  liveAccess: {
    authorized: false,
    remaining: 0,
    global_remaining: 0,
    expires_at: null,
  },
};

const byId = (id) => document.getElementById(id);
const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (character) => ({
  "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
})[character]);

const decisionContent = {
  APPROVE: ["Payment approved", "Required checks found no blocking evidence. The payment may continue."],
  HOLD: ["Payment held", "Identity evidence alone cannot establish safe intent. Keep the funds in place for review."],
  BLOCK: ["Payment blocked", "The payment remains stopped for protective fraud review; automated policy never weakens this outcome."],
  RETRY: ["Verification incomplete", "Required evidence was missing or unavailable. Retry before releasing funds."],
  VERIFY_DEVICE: ["Verify this device", "Fresh enrollment checks are required before the first payment on this device."],
  TRUST_ESTABLISHED: ["Device trusted", "Fresh Number Verification and SIM Swap checks completed for this setup."],
  CANCELLED: ["Review cancelled", "This review is closed and cannot release the payment."],
};
const toolLabels = {
  sim_swap: "SIM Swap",
  number_verification: "Number Verification",
  device_swap: "Device Swap",
  roaming: "Roaming",
  reachability: "Reachability",
  finish: "Finish",
  stop: "Stop",
};
const toolLabel = (tool = "") => toolLabels[tool] || tool.replaceAll("_", " ");

function setBusy(button, busy, label) {
  if (!button.dataset.label) button.dataset.label = button.textContent;
  button.disabled = busy;
  button.textContent = busy ? label : button.dataset.label;
}

function showError(message) {
  const error = byId("formError");
  error.textContent = message;
  error.classList.toggle("visible", Boolean(message));
  if (message) error.focus();
}

function renderReady() {
  byId("outcomeMain").dataset.state = "READY";
  byId("outcomeEyebrow").textContent = "Decision workspace";
  byId("outcomeTitle").textContent = "Ready for review";
  byId("outcomeCopy").textContent = "Choose a scenario and review the payment. Technical evidence stays available below without obscuring the decision.";
  byId("preScore").textContent = "-";
  byId("finalScore").textContent = "-";
  byId("externalCalls").textContent = "0";
  byId("reasonList").innerHTML = "<li>The review has not started.</li>";
  byId("evidenceBody").innerHTML = '<p class="empty">No network evidence requested.</p>';
  byId("traceBody").innerHTML = '<p class="empty">No agent investigation was needed.</p>';
  byId("liveProgress").hidden = true;
  byId("resultActions").hidden = true;
  byId("resumeButton").hidden = true;
  document.querySelectorAll(".step").forEach((step, index) => step.classList.toggle("active", index === 0));
}

function invalidateSession() {
  if (state.pending) return;
  state.operationGeneration += 1;
  clearSessionState();
  renderReady();
}

function clearSessionState() {
  state.sessionSignature = null;
  state.enrolled = false;
  state.currentRun = null;
}

function setFormLocked(locked) {
  state.pending = locked;
  byId("reviewForm").setAttribute("aria-busy", String(locked));
  byId("reviewForm").querySelectorAll("button, input, select").forEach((control) => {
    control.disabled = locked;
  });
  if (!locked) updateReviewAvailability();
}

function connectedModeSelected() {
  return byId("modeSelect").value === "NOKIA_SANDBOX";
}

function updateReviewAvailability() {
  const accessBlocked = connectedModeSelected()
    && (!state.liveAccess.authorized || state.liveAccess.remaining <= 0 || state.liveAccess.global_remaining <= 0);
  byId("reviewButton").disabled = !state.ready || state.pending || accessBlocked || state.currentRun?.decision === "PENDING";
}

function updateLiveAccessUi() {
  const selected = connectedModeSelected();
  const panel = byId("liveAccessPanel");
  panel.hidden = !selected;
  if (!selected) {
    updateReviewAvailability();
    return;
  }
  const authorized = state.liveAccess.authorized;
  byId("liveAccessFields").hidden = authorized;
  byId("liveConnectionState").textContent = authorized ? "Unlocked" : "Locked";
  byId("liveConnectionState").dataset.state = authorized ? "UNLOCKED" : "LOCKED";
  if (!authorized) {
    byId("liveAccessStatus").textContent = "Enter the judge code to use protected connected mode.";
  } else if (state.liveAccess.remaining <= 0 || state.liveAccess.global_remaining <= 0) {
    byId("liveAccessStatus").textContent = "Connected quota is temporarily exhausted. Fixture mode remains available.";
  } else {
    const count = state.liveAccess.remaining;
    byId("liveAccessStatus").textContent = `${count} connected run${count === 1 ? "" : "s"} remaining this hour.`;
  }
  updateReviewAvailability();
}

function renderLiveProgress(result) {
  if (result?.decision === "PENDING") {
    byId("preScore").textContent = result.pre_call_score ?? "-";
    byId("externalCalls").textContent = (result.model_calls || 0) + (result.telecom_calls || 0);
    if (result.reasons?.length) {
      byId("reasonList").innerHTML = result.reasons.map((reason) => `<li>${escapeHtml(reason)}</li>`).join("");
    }
    if (result.evidence?.length) renderEvidence(result.evidence, result);
  }
  const progress = result?.progress || [];
  const visibleProgress = progress.filter((item, index) => {
    if (item.stage === "QUEUED") return progress.length === 1;
    if (item.stage !== "AGENT_DECISION") return true;
    return index === progress.length - 1;
  });
  const panel = byId("liveProgress");
  panel.hidden = !result?.connected && !progress.length;
  if (panel.hidden) return;
  const stageNames = {
    QUEUED: "Queued",
    LOCAL_SCREEN: "Local screen",
    AGENT_DECISION: "Agent choosing",
    API_SELECTED: "API selected",
    EVIDENCE_RECEIVED: "Evidence received",
    POLICY_DECISION: "Policy decision",
    COMPLETE: "Complete",
    CANCELLED: "Cancelled",
  };
  byId("progressStage").textContent = stageNames[result.stage || progress.at(-1)?.stage] || "Running";
  byId("progressList").innerHTML = visibleProgress.map((item, index) => {
    const metadata = [item.tool ? toolLabel(item.tool) : null, item.status,
      item.http_status ? `HTTP ${item.http_status}` : null,
      item.latency_ms != null ? `${item.latency_ms} ms` : null]
      .filter(Boolean).join(" | ");
    return `<li data-stage="${escapeHtml(item.stage || "")}"><span class="progress-index">${index + 1}</span><div><strong>${escapeHtml(item.actor || "SAFEPAY")} | ${escapeHtml(stageNames[item.stage] || item.stage || "Update")}</strong><span>${escapeHtml(item.message || "Progress recorded")}</span>${metadata ? `<small>${escapeHtml(metadata)}</small>` : ""}</div></li>`;
  }).join("");
  if (result.decision === "PENDING") byId("progressList").scrollTop = byId("progressList").scrollHeight;
}

function renderPending(enrollment, connected = false) {
  byId("outcomeMain").dataset.state = "READY";
  byId("outcomeEyebrow").textContent = "Investigation running";
  byId("outcomeTitle").textContent = enrollment ? "Verifying device" : "Reviewing payment";
  byId("outcomeCopy").textContent = "SafePay is collecting only the evidence required for this context.";
  byId("preScore").textContent = "-";
  byId("finalScore").textContent = "-";
  byId("externalCalls").textContent = "-";
  byId("reasonList").innerHTML = "<li>Waiting for the bounded investigation to complete.</li>";
  byId("evidenceBody").innerHTML = '<p class="empty">Evidence will appear when the review completes.</p>';
  byId("traceBody").innerHTML = '<p class="empty">The trace will appear when the review completes.</p>';
  if (connected) {
    renderLiveProgress({connected: true, stage: "QUEUED", progress: [{
      stage: "QUEUED", actor: "SAFEPAY", message: "Preparing the protected connected investigation",
    }]});
  } else {
    byId("liveProgress").hidden = true;
  }
  byId("resultActions").hidden = true;
  document.querySelectorAll(".step").forEach((step, index) => step.classList.toggle("active", index < 2));
}

function updateScenarioContext() {
  if (!state.catalog) return;
  const scenario = state.catalog.scenarios.find((item) => item.id === byId("scenarioSelect").value);
  byId("scenarioHelp").textContent = scenario?.description || "";
  const enrollment = ["first_setup", "new_device", "enrollment_outage"].includes(scenario?.id);
  byId("reviewButton").textContent = enrollment
    ? (state.enrolled ? "Continue to payment" : "Verify device")
    : "Review payment";
  byId("reviewButton").dataset.label = byId("reviewButton").textContent;
  const defaults = {
    routine: [200, "family", "INSTANT_PAYMENT"],
    identity_mismatch: [300, "new_payee", "INSTANT_PAYMENT"],
    first_setup: [100, "family", "INSTANT_PAYMENT"],
    new_device: [100, "family", "INSTANT_PAYMENT"],
    scam_transfer: [15000, "new_payee", "INSTANT_PAYMENT"],
    sim_swap: [35000, "new_payee", "INSTANT_PAYMENT"],
    card_misuse: [1200, "merchant", "CARD_CHECKOUT"],
    combined_attack: [8000, "wallet", "WALLET_TRANSFER"],
    legitimate_travel: [600, "new_payee", "INSTANT_PAYMENT"],
    velocity: [100, "new_payee", "INSTANT_PAYMENT"],
    provider_outage: [500, "new_payee", "INSTANT_PAYMENT"],
    enrollment_outage: [100, "family", "INSTANT_PAYMENT"],
  };
  const values = defaults[scenario?.id] || [200, "family", "INSTANT_PAYMENT"];
  byId("amountInput").value = values[0];
  byId("recipientSelect").value = values[1];
  byId("channelSelect").value = values[2];
}

function chooseCountry(code) {
  const changed = state.country !== code;
  state.country = code;
  document.querySelectorAll(".segment").forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.country === code));
  });
  const market = state.catalog.countries[code];
  byId("currencyHelp").textContent = market.currency;
  byId("railContext").textContent = `${market.name} | ${market.rail}`;
  if (changed) invalidateSession();
}

function renderEvidence(items = [], result = {}) {
  if (!items.length) {
    let copy = "No network evidence was returned for this result.";
    if (result.decision_source === "LOCAL_SCREENING" && result.decision === "APPROVE") {
      copy = "No network evidence requested. The local screen kept this routine payment on the zero-call path.";
    } else if (result.decision === "VERIFY_DEVICE") {
      copy = "No network evidence was returned because fresh device verification is required first.";
    } else if ((result.model_calls || 0) > 0) {
      copy = "No network evidence was returned before the agent investigation stopped.";
    }
    byId("evidenceBody").innerHTML = `<p class="empty">${copy}</p>`;
    return;
  }
  const rows = items.map((item) => {
    const value = Object.entries(item.data || {}).map(([key, val]) => `${key}: ${val}`).join(", ") || item.error || "No value";
    const subject = item.subject ? `<br><small>${escapeHtml(item.subject)}</small>` : "";
    const transport = [item.http_status ? `HTTP ${item.http_status}` : null,
      item.latency_ms != null ? `${item.latency_ms} ms` : null].filter(Boolean).join(" | ");
    const endpoint = item.endpoint ? `<br><small>${escapeHtml(item.endpoint)}</small>` : "";
    return `<tr><td><strong>${escapeHtml(toolLabel(item.tool))}</strong>${subject}</td><td><span class="source-tag">${escapeHtml(item.source)}</span>${endpoint}</td><td><strong>${escapeHtml(item.status)}</strong>${transport ? `<br><small>${escapeHtml(transport)}</small>` : ""}</td><td>${escapeHtml(value)}</td></tr>`;
  }).join("");
  byId("evidenceBody").innerHTML = `<table><thead><tr><th>Observation</th><th>Source</th><th>Status</th><th>Returned value</th></tr></thead><tbody>${rows}</tbody></table>`;
}

function renderTrace(items = [], source = "") {
  if (!items.length) {
    const copy = source === "LOCAL_SCREENING"
      ? "Local screening completed the decision; Gemini and telecom APIs were not called."
      : "Deterministic policy evaluated the returned evidence.";
    byId("traceBody").innerHTML = `<p class="empty">${copy}</p>`;
    return;
  }
  const rows = items.map((item) =>
    `<li><strong>${escapeHtml(item.actor)} | ${escapeHtml(toolLabel(item.tool))} ${item.status ? `| ${escapeHtml(item.status)}` : ""}</strong><span>${escapeHtml(item.reason || "Observation recorded")}</span></li>`
  ).join("");
  byId("traceBody").innerHTML = `<ol class="trace">${rows}</ol>`;
}

function renderResult(result) {
  state.currentRun = result;
  byId("resumeButton").hidden = true;
  const content = decisionContent[result.decision] || ["Review complete", "The workflow returned a decision."];
  byId("outcomeMain").dataset.state = result.decision;
  byId("outcomeEyebrow").textContent = result.decision_source?.replaceAll("_", " ") || "Decision";
  byId("outcomeTitle").textContent = content[0];
  byId("outcomeCopy").textContent = content[1];
  byId("preScore").textContent = result.pre_call_score ?? "Not scored";
  byId("finalScore").textContent = result.final_risk_score ?? "Not scored";
  byId("externalCalls").textContent = String((result.telecom_calls || 0) + (result.model_calls || 0));
  const reasons = result.reasons?.length
    ? result.reasons
    : [result.decision_source === "LOCAL_SCREENING"
      ? "Routine context stayed below the investigation threshold; no external evidence was requested."
      : "No additional risk reason was recorded."];
  byId("reasonList").innerHTML = reasons.map((reason) => `<li>${escapeHtml(reason)}</li>`).join("");
  renderEvidence(result.evidence, result);
  renderTrace(result.agent_trace, result.decision_source);
  renderLiveProgress(result);
  byId("resultActions").hidden = !["HOLD", "RETRY", "VERIFY_DEVICE"].includes(result.decision);
  document.querySelectorAll(".step").forEach((step) => step.classList.add("active"));
  byId("outcomeMain").scrollIntoView({ behavior: "smooth", block: "nearest" });
  byId("outcomeMain").focus({preventScroll: true});
}

async function ensureSession(scenario) {
  const context = { scenario, country: state.country, mode: byId("modeSelect").value };
  const signature = JSON.stringify(context);
  if (state.sessionSignature === signature) return;
  const session = await fetch("/api/v1/sessions", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(context),
  });
  if (!session.ok) {
    const error = new Error((await session.json()).detail || "Could not start the review session.");
    error.status = session.status;
    throw error;
  }
  state.sessionSignature = signature;
  state.enrolled = false;
}

async function refreshLiveAccess() {
  if (!state.catalog?.live_enabled) return;
  const response = await fetch("/api/v1/live-access");
  if (!response.ok) throw new Error("Connected access status is unavailable.");
  state.liveAccess = await response.json();
  updateLiveAccessUi();
}

async function unlockConnectedMode() {
  const button = byId("unlockButton");
  const input = byId("accessCodeInput");
  byId("accessError").textContent = "";
  if (!input.value) {
    byId("accessError").textContent = "Enter the judge access code.";
    input.focus();
    return;
  }
  setBusy(button, true, "Unlocking...");
  try {
    const response = await fetch("/api/v1/live-access", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({code: input.value}),
    });
    const body = await response.json();
    if (!response.ok) {
      const error = new Error(body.detail || "Connected mode could not be unlocked.");
      error.status = response.status;
      throw error;
    }
    state.liveAccess = body;
    input.value = "";
    updateLiveAccessUi();
  } catch (error) {
    byId("accessError").textContent = error.message;
    input.focus();
  } finally {
    setBusy(button, false, "");
  }
}

async function pollConnectedRun(runId, operation) {
  const deadline = Date.now() + 60000;
  while (Date.now() < deadline) {
    if (operation !== state.operationGeneration) return null;
    await new Promise((resolve) => setTimeout(resolve, 350));
    if (operation !== state.operationGeneration) return null;
    const response = await fetch(`/api/v1/runs/${encodeURIComponent(runId)}`);
    if (!response.ok) {
      const error = new Error((await response.json()).detail || "Could not read connected progress.");
      error.status = response.status;
      throw error;
    }
    const result = await response.json();
    if (operation !== state.operationGeneration) return null;
    state.currentRun = result;
    renderLiveProgress(result);
    byId("resultActions").hidden = result.decision !== "PENDING";
    if (result.decision !== "PENDING") return result;
  }
  throw new Error("The connected review is still running. Reconnect to read its result without starting another investigation.");
}

async function reconnectReview() {
  if (state.pending || state.currentRun?.decision !== "PENDING") return;
  const operation = ++state.operationGeneration;
  setFormLocked(true);
  byId("resumeButton").hidden = true;
  showError("");
  try {
    const result = await pollConnectedRun(state.currentRun.id, operation);
    if (result && operation === state.operationGeneration) {
      state.enrolled = result.decision === "TRUST_ESTABLISHED" || state.enrolled;
      if (state.enrolled) byId("reviewButton").dataset.label = "Continue to payment";
      renderResult(result);
    }
  } catch (error) {
    if (operation === state.operationGeneration) {
      showError(error.message);
      byId("resumeButton").hidden = false;
    }
  } finally {
    if (operation === state.operationGeneration) {
      setFormLocked(false);
      byId("reviewButton").textContent = byId("reviewButton").dataset.label;
    }
  }
}

async function startAndRun(event) {
  event.preventDefault();
  if (!state.ready || state.pending) return;
  showError("");
  const button = byId("reviewButton");
  const scenario = byId("scenarioSelect").value;
  const connected = connectedModeSelected();
  if (connected && !state.liveAccess.authorized) {
    updateLiveAccessUi();
    byId("accessCodeInput").focus();
    return;
  }
  const enrollment = ["first_setup", "new_device", "enrollment_outage"].includes(scenario) && !state.enrolled;
  const amount = Number(byId("amountInput").value);
  if (!Number.isFinite(amount) || amount <= 0 || amount > 1000000) {
    showError("Enter an amount between 1 and 1,000,000.");
    byId("amountInput").focus();
    return;
  }
  const operation = ++state.operationGeneration;
  setFormLocked(true);
  button.dataset.label = enrollment ? "Verify device" : (state.enrolled ? "Continue to payment" : "Review payment");
  button.textContent = enrollment ? "Verifying device..." : "Reviewing payment...";
  renderPending(enrollment, connected);
  state.currentRun = null;
  try {
    await ensureSession(scenario);
    const requestId = `${enrollment ? "enroll" : "payment"}-${Date.now()}`;
    const path = connected
      ? (enrollment ? "/api/v1/live-enrollments" : "/api/v1/live-payments")
      : (enrollment ? "/api/v1/enrollments" : "/api/v1/payments");
    const payload = enrollment
      ? { request_id: requestId }
      : {
          request_id: requestId,
          amount,
          recipient: byId("recipientSelect").value,
          channel: byId("channelSelect").value,
        };
    const response = await fetch(path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      const error = new Error((await response.json()).detail || "The review could not complete.");
      error.status = response.status;
      throw error;
    }
    let result = await response.json();
    if (operation !== state.operationGeneration) return;
    if (connected && response.status === 202) {
      state.liveAccess.remaining = Math.max(0, state.liveAccess.remaining - 1);
      state.liveAccess.global_remaining = Math.max(0, state.liveAccess.global_remaining - 1);
      updateLiveAccessUi();
      state.currentRun = result;
      renderLiveProgress(result);
      byId("resultActions").hidden = false;
      result = await pollConnectedRun(result.id, operation);
      if (!result || operation !== state.operationGeneration) return;
    }
    if (result.decision === "TRUST_ESTABLISHED") {
      state.enrolled = true;
      button.dataset.label = "Continue to payment";
    } else if (enrollment) {
      button.dataset.label = "Retry device verification";
    } else {
      button.dataset.label = "Review payment";
    }
    renderResult(result);
  } catch (error) {
    if (operation !== state.operationGeneration) return;
    if (error.status === 401) clearSessionState();
    showError(`${error.message} Check the selected mode and retry.`);
    if (state.currentRun?.decision === "PENDING") {
      byId("resultActions").hidden = false;
      byId("resumeButton").hidden = false;
    } else {
      renderReady();
    }
    if (connected && [401, 403, 429].includes(error.status)) {
      await refreshLiveAccess().catch(() => {});
    }
  } finally {
    if (operation === state.operationGeneration) {
      setFormLocked(false);
      button.textContent = button.dataset.label;
    }
  }
}

async function cancelCurrent() {
  if (!state.currentRun) return;
  const button = byId("cancelButton");
  const operation = ++state.operationGeneration;
  setBusy(button, true, "Cancelling...");
  try {
    const response = await fetch(`/api/v1/runs/${encodeURIComponent(state.currentRun.id)}/cancel`, { method: "POST" });
    if (!response.ok) throw new Error((await response.json()).detail || "Could not cancel this review.");
    const result = await response.json();
    if (operation === state.operationGeneration) renderResult(result);
  } catch (error) {
    if (operation === state.operationGeneration) {
      showError(error.message);
      byId("resumeButton").hidden = state.currentRun?.decision !== "PENDING";
    }
  } finally {
    setBusy(button, false, "");
    if (operation === state.operationGeneration && state.pending) {
      setFormLocked(false);
      byId("reviewButton").textContent = byId("reviewButton").dataset.label;
    }
  }
}

async function runEvaluation() {
  const button = byId("evaluationButton");
  setBusy(button, true, "Running evaluation...");
  byId("evaluationResult").textContent = "";
  try {
    const response = await fetch("/api/v1/evaluations", { method: "POST" });
    if (!response.ok) throw new Error("Evaluation could not run.");
    const result = await response.json();
    byId("evaluationResult").textContent = `${result.passed} passed · ${result.failed} failed · ${result.mode} · ${result.elapsed_ms} ms`;
  } catch (error) {
    byId("evaluationResult").textContent = `${error.message} Retry when the service is available.`;
  } finally {
    setBusy(button, false, "");
  }
}

function handleModeChange() {
  if (state.pending) return;
  const connected = connectedModeSelected();
  const fixtureOnly = new Set(["provider_outage", "enrollment_outage"]);
  Array.from(byId("scenarioSelect").options).forEach((option) => {
    option.disabled = connected && fixtureOnly.has(option.value);
  });
  if (byId("scenarioSelect").selectedOptions[0]?.disabled) {
    const replacement = Array.from(byId("scenarioSelect").options).find((option) => !option.disabled);
    if (replacement) byId("scenarioSelect").value = replacement.value;
  }
  invalidateSession();
  updateScenarioContext();
  updateLiveAccessUi();
  byId("environmentBadge").textContent = connected ? "CONNECTED SANDBOX SELECTED" : "REPEATABLE FIXTURE";
  if (connected) refreshLiveAccess().catch(() => {});
}

async function init() {
  setFormLocked(true);
  try {
    const [catalogResponse, healthResponse] = await Promise.all([
      fetch("/api/v1/catalog"),
      fetch("/api/v1/health"),
    ]);
    if (!catalogResponse.ok || !healthResponse.ok) throw new Error("Service unavailable");
    state.catalog = await catalogResponse.json();
    const health = await healthResponse.json();
    byId("healthText").textContent = health.status === "healthy" ? "Service ready" : "Service unavailable";
    byId("environmentBadge").textContent = state.catalog.live_enabled ? "CONNECTED SANDBOX AVAILABLE" : "FIXTURE DEMO";
    byId("countrySegments").innerHTML = Object.entries(state.catalog.countries).map(([code, market]) =>
      `<button class="segment" type="button" data-country="${escapeHtml(code)}" aria-pressed="${code === state.country}">${escapeHtml(market.name)}</button>`
    ).join("");
    byId("scenarioSelect").innerHTML = state.catalog.scenarios.map((item) =>
      `<option value="${escapeHtml(item.id)}">${escapeHtml(item.name)}</option>`
    ).join("");
    if (state.catalog.live_enabled) {
      byId("modeSelect").insertAdjacentHTML("beforeend", '<option value="NOKIA_SANDBOX">Connected: Nokia + Gemini</option>');
      await refreshLiveAccess().catch(() => {
        byId("accessError").textContent = "Connected access is unavailable. Fixture mode remains available.";
      });
    }
    document.querySelectorAll(".segment").forEach((button) =>
      button.addEventListener("click", () => chooseCountry(button.dataset.country))
    );
    chooseCountry(state.country);
    updateScenarioContext();
    state.ready = true;
    setFormLocked(false);
  } catch (error) {
    byId("healthText").textContent = "Service unavailable";
    showError("SafePay could not load its scenario catalog. Refresh after the service is running.");
    byId("reviewButton").disabled = true;
  }
}

byId("reviewForm").addEventListener("submit", startAndRun);
byId("scenarioSelect").addEventListener("change", () => {
  invalidateSession();
  updateScenarioContext();
});
byId("modeSelect").addEventListener("change", handleModeChange);
byId("unlockButton").addEventListener("click", unlockConnectedMode);
byId("accessCodeInput").addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    unlockConnectedMode();
  }
});
byId("cancelButton").addEventListener("click", cancelCurrent);
byId("resumeButton").addEventListener("click", reconnectReview);
byId("evaluationButton").addEventListener("click", runEvaluation);
init();
