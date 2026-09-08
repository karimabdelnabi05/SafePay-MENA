/**
 * SafePay MENA - Institutional Frontend Dashboard Client
 * Enterprise SOC Controller with Adaptive CAMARA Orchestration, UX Telemetry, and Wire Inspector.
 */

let currentScenario = 'CLEAN_TRANSFER';
let currentTransactionId = 'txn_clean_001';
let socket = null;
let activeTab = 'ai';

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  initWebSocket();
  loadScenario('CLEAN_TRANSFER');
  switchTab('ai');
});

// Tab Switching Controller
function switchTab(tab) {
  activeTab = tab;
  
  const tabs = ['ai', 'wire', 'rail'];
  tabs.forEach(t => {
    const btn = document.getElementById(`tabBtn${capitalize(t)}`);
    const content = document.getElementById(`tabContent${capitalize(t)}`);
    if (btn) {
      if (t === tab) {
        btn.classList.add('active');
        btn.classList.remove('text-slate-400');
        btn.classList.add('text-slate-200');
      } else {
        btn.classList.remove('active');
        btn.classList.remove('text-slate-200');
        btn.classList.add('text-slate-400');
      }
    }
    if (content) {
      if (t === tab) {
        content.classList.remove('hidden');
      } else {
        content.classList.add('hidden');
      }
    }
  });

  if (window.lucide) lucide.createIcons();
}

function capitalize(s) {
  if (!s) return '';
  return s.charAt(0).toUpperCase() + s.slice(1);
}

// WebSocket Connection Management
function initWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${window.location.host}/ws/live-feed`;
  
  socket = new WebSocket(wsUrl);

  socket.onopen = () => {
    const wsBadge = document.getElementById('wsStatus');
    if (wsBadge) {
      wsBadge.innerText = 'Connected';
      wsBadge.className = 'font-semibold text-emerald-400';
    }
    console.log('[SafePay SOC] WebSocket Connected to Gateway');
  };

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      if (data.type === 'TRANSACTION_EVALUATED') {
        renderEvaluation(data.decision);
      } else if (data.type === 'STEP_UP_RESOLVED') {
        renderStepUpResolved(data);
      }
    } catch (e) {
      console.error('Error parsing WS message:', e);
    }
  };

  socket.onclose = () => {
    const wsBadge = document.getElementById('wsStatus');
    if (wsBadge) {
      wsBadge.innerText = 'Reconnecting...';
      wsBadge.className = 'font-semibold text-amber-400';
    }
    setTimeout(initWebSocket, 2000);
  };
}

// Beneficiary Trust Toggle
function toggleSavedBeneficiary(isSaved) {
  const badge = document.getElementById('savedBadge');
  const trustText = document.getElementById('trustLevelText');
  if (badge) {
    if (isSaved) {
      badge.innerText = 'TRUSTED';
      badge.className = 'absolute right-2.5 top-2 text-[10px] bg-emerald-950 text-emerald-400 border border-emerald-800/60 px-1.5 py-0.5 rounded font-medium';
    } else {
      badge.innerText = 'NEW PAYEE';
      badge.className = 'absolute right-2.5 top-2 text-[10px] bg-amber-950 text-amber-400 border border-amber-800/60 px-1.5 py-0.5 rounded font-medium';
    }
  }
  if (trustText) {
    trustText.innerText = isSaved ? 'Trust Level: HIGH' : 'Trust Level: UNVERIFIED';
    trustText.className = isSaved ? 'text-[10px] font-mono text-emerald-400' : 'text-[10px] font-mono text-amber-400';
  }
}

// Preset Scenario Switcher
function loadScenario(type) {
  currentScenario = type;
  
  // Highlight active preset button
  ['Clean', 'Spam', 'Swap', 'Card'].forEach(s => {
    const btn = document.getElementById(`btnScenario${s}`);
    if (btn) {
      btn.classList.remove('border-sky-500', 'bg-slate-800', 'text-sky-300');
      btn.classList.add('border-slate-700', 'bg-slate-900/90', 'text-slate-200');
    }
  });

  const activeBtnMap = {
    'CLEAN_TRANSFER': 'btnScenarioClean',
    'SPAM_CALL_SCAM': 'btnScenarioSpam',
    'SIM_SWAP_ATTACK': 'btnScenarioSwap',
    'STOLEN_CARD_CNP': 'btnScenarioCard'
  };
  const activeBtn = document.getElementById(activeBtnMap[type]);
  if (activeBtn) {
    activeBtn.classList.remove('border-slate-700', 'bg-slate-900/90', 'text-slate-200');
    activeBtn.classList.add('border-sky-500', 'bg-slate-800', 'text-sky-300');
  }

  const callBanner = document.getElementById('activeCallBanner');
  const carrierTag = document.getElementById('carrierTag');
  const inputRecipient = document.getElementById('inputRecipientName');
  const inputAmount = document.getElementById('inputAmount');
  const selectCurrency = document.getElementById('selectCurrency');
  const callIndicatorDot = document.getElementById('callIndicatorDot');
  const callIndicatorText = document.getElementById('callIndicatorText');
  const chkSaved = document.getElementById('chkSavedBeneficiary');

  if (type === 'CLEAN_TRANSFER') {
    callBanner.classList.add('hidden');
    if (chkSaved) chkSaved.checked = true;
    toggleSavedBeneficiary(true);
    carrierTag.innerText = 'stc Saudi 5G';
    inputRecipient.value = 'Fatima Mohamed (Mom)';
    inputAmount.value = '200';
    selectCurrency.value = 'SAR';
    updateCurrency('SAR');
    callIndicatorDot.className = 'h-1.5 w-1.5 rounded-full bg-slate-600';
    callIndicatorText.innerText = 'Cellular LTE';
  } 
  else if (type === 'SPAM_CALL_SCAM') {
    callBanner.classList.remove('hidden');
    if (chkSaved) chkSaved.checked = false;
    toggleSavedBeneficiary(false);
    carrierTag.innerText = 'stc Saudi (Active Voice Call)';
    inputRecipient.value = 'Unknown Payee (Scammer)';
    inputAmount.value = '15000';
    selectCurrency.value = 'SAR';
    updateCurrency('SAR');
    callIndicatorDot.className = 'h-1.5 w-1.5 rounded-full bg-amber-400 animate-ping';
    callIndicatorText.innerText = 'Call in Progress';
  } 
  else if (type === 'SIM_SWAP_ATTACK') {
    callBanner.classList.add('hidden');
    if (chkSaved) chkSaved.checked = false;
    toggleSavedBeneficiary(false);
    carrierTag.innerText = 'Rogue Handset (IMEI Mismatch)';
    inputRecipient.value = 'Mule Account Corp';
    inputAmount.value = '35000';
    selectCurrency.value = 'SAR';
    updateCurrency('SAR');
    callIndicatorDot.className = 'h-1.5 w-1.5 rounded-full bg-rose-500 animate-pulse';
    callIndicatorText.innerText = 'SIM Alert';
  }
  else if (type === 'STOLEN_CARD_CNP') {
    callBanner.classList.add('hidden');
    if (chkSaved) chkSaved.checked = false;
    toggleSavedBeneficiary(false);
    carrierTag.innerText = 'Rogue Web Browser (No SIM)';
    inputRecipient.value = 'Amazon UAE (3DS Online)';
    inputAmount.value = '1200';
    selectCurrency.value = 'AED';
    updateCurrency('AED');
    callIndicatorDot.className = 'h-1.5 w-1.5 rounded-full bg-purple-400 animate-pulse';
    callIndicatorText.innerText = 'No SIM Carrier Match';
  }

  if (window.lucide) lucide.createIcons();
}

function updateCurrency(curr) {
  document.getElementById('currencySymbol').innerText = curr;
  document.getElementById('balanceCurrency').innerText = curr;
  if (curr === 'EGP') {
    document.getElementById('balanceAmount').innerText = '120,000.00';
  } else if (curr === 'AED') {
    document.getElementById('balanceAmount').innerText = '32,500.00';
  } else {
    document.getElementById('balanceAmount').innerText = '45,250.00';
  }
}

// Execute Pre-Auth Evaluation Hook
async function executeTransfer() {
  const btn = document.getElementById('btnSubmitTransfer');
  const btnText = document.getElementById('btnSubmitText');
  
  btn.disabled = true;
  btnText.innerText = 'Evaluating CAMARA Shield...';

  const amount = parseFloat(document.getElementById('inputAmount').value) || 200;
  const currency = document.getElementById('selectCurrency').value;
  const recipientName = document.getElementById('inputRecipientName').value;
  const chkSaved = document.getElementById('chkSavedBeneficiary');
  const isSaved = chkSaved ? chkSaved.checked : (currentScenario === 'CLEAN_TRANSFER');
  
  currentTransactionId = 'txn_' + Date.now().toString().slice(-6);

  const payload = {
    transaction_id: currentTransactionId,
    sender_phone: '+966501234567',
    recipient_id: 'REC_' + Math.floor(Math.random() * 900000 + 100000),
    recipient_name: recipientName,
    amount: amount,
    currency: currency,
    is_saved_beneficiary: isSaved,
    device_ip: '197.34.12.89'
  };

  try {
    const url = `/api/v1/transfer/evaluate?scenario=${currentScenario}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const decision = await response.json();
    renderEvaluation(decision);

    // Handle Client Modal Behaviors
    if (decision.decision === 'STEP_UP') {
      document.getElementById('modalAmount').innerText = `${amount.toLocaleString()} ${currency}`;
      document.getElementById('modalRecipient').innerText = recipientName;
      document.getElementById('biometricModal').classList.remove('hidden');
    } else if (decision.decision === 'BLOCK') {
      document.getElementById('blockModal').classList.remove('hidden');
    }

  } catch (err) {
    console.error('Evaluation failed:', err);
    alert('Evaluation request failed. Check server logs.');
  } finally {
    btn.disabled = false;
    btnText.innerText = 'Authorize & Send';
  }
}

// Render Risk Decision, Orchestration, Wire Inspector & Telemetry to SOC Panel
function renderEvaluation(decision) {
  const score = decision.risk_score;
  const tier = decision.decision;

  // 1. Update Gauge
  const circle = document.getElementById('gaugeProgress');
  const scoreText = document.getElementById('gaugeScoreText');
  const circumference = 427.25;
  const offset = circumference - (score / 100) * circumference;
  
  circle.style.strokeDashoffset = offset;
  scoreText.innerText = score;

  let tierColor = '#10B981';
  let badgeClass = 'text-sm font-bold px-3 py-1 rounded-lg bg-emerald-950 text-emerald-400 border border-emerald-800 tracking-wider font-mono';

  if (tier === 'STEP_UP') {
    tierColor = '#F59E0B';
    badgeClass = 'text-sm font-bold px-3 py-1 rounded-lg bg-amber-950 text-amber-400 border border-amber-800 tracking-wider font-mono';
  } else if (tier === 'BLOCK') {
    tierColor = '#EF4444';
    badgeClass = 'text-sm font-bold px-3 py-1 rounded-lg bg-rose-950 text-rose-400 border border-rose-800 tracking-wider font-mono';
  }

  circle.style.stroke = tierColor;
  scoreText.style.color = tierColor;

  // 2. Decision Badge & Text
  const decisionBadge = document.getElementById('decisionBadge');
  decisionBadge.innerText = tier;
  decisionBadge.className = badgeClass;

  document.getElementById('vectorBadge').innerText = decision.primary_vector;
  document.getElementById('actionText').innerText = decision.recommended_action;
  
  const statText = decision.statutory_flags.length > 0 ? decision.statutory_flags.join(' • ') : 'Standard SAMA/CBE risk scoring baseline';
  document.getElementById('statutoryText').innerText = statText;

  const latencyStr = `${decision.execution_time_ms || 2.1} ms`;
  document.getElementById('engineLatency').innerText = latencyStr;
  const kpiElem = document.getElementById('kpiLatency');
  if (kpiElem) kpiElem.innerText = latencyStr;

  // 3. Update Adaptive Orchestration & UX Telemetry Banner
  const orch = decision.orchestration || (decision.signals && decision.signals.orchestration);
  if (orch) {
    const tierBadge = document.getElementById('orchTierBadge');
    const apisInvoked = document.getElementById('orchApisInvoked');
    const apisSkipped = document.getElementById('orchApisSkipped');
    const costActual = document.getElementById('orchCostActual');
    const costNaive = document.getElementById('orchCostNaive');
    const costSaved = document.getElementById('orchCostSaved');
    const uxExp = document.getElementById('orchUxExperience');
    const uxImp = document.getElementById('orchUxImpact');

    if (tierBadge) {
      tierBadge.innerText = orch.tier.replace(/_/g, ' ');
      if (orch.tier.includes('BASELINE')) {
        tierBadge.className = 'text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800';
      } else if (orch.tier.includes('COERCION')) {
        tierBadge.className = 'text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-800';
      } else {
        tierBadge.className = 'text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800';
      }
    }

    if (apisInvoked) apisInvoked.innerText = `${orch.carrier_api_calls_count} / 4 APIs Active (${orch.apis_invoked[0] || 'Targeted'})`;
    if (apisSkipped) apisSkipped.innerText = orch.apis_skipped_or_cached.join(' • ');
    if (costActual) costActual.innerText = `$${orch.cost_actual_usd.toFixed(2)}`;
    if (costNaive) costNaive.innerText = `$${orch.cost_naive_usd.toFixed(2)}`;
    if (costSaved) costSaved.innerText = `${orch.cost_reduction_percent}% Saved`;
    if (uxExp) uxExp.innerText = orch.user_friction;
    if (uxImp) uxImp.innerText = orch.checkout_experience;
  }

  // 4. Update CAMARA Telemetry Badges
  const sig = decision.signals;
  
  // Number Verify
  const numStatus = document.getElementById('sigStatusNum');
  const numIcon = document.getElementById('sigIconNum');
  if (sig.number_verified) {
    numStatus.innerText = 'VERIFIED';
    numStatus.className = 'text-xs font-bold text-emerald-400 font-mono';
    numIcon.setAttribute('data-lucide', 'check');
    numIcon.className = 'h-3.5 w-3.5 text-emerald-400';
  } else {
    numStatus.innerText = 'FAILED (Rogue)';
    numStatus.className = 'text-xs font-bold text-rose-400 font-mono';
    numIcon.setAttribute('data-lucide', 'x');
    numIcon.className = 'h-3.5 w-3.5 text-rose-400';
  }

  // SIM Swap
  const swapStatus = document.getElementById('sigStatusSwap');
  const swapIcon = document.getElementById('sigIconSwap');
  if (sig.sim_swapped_recently) {
    swapStatus.innerText = `SWAPPED (${sig.sim_swap_hours_ago || 2.1}h)`;
    swapStatus.className = 'text-xs font-bold text-rose-400 font-mono';
    swapIcon.setAttribute('data-lucide', 'alert-octagon');
    swapIcon.className = 'h-3.5 w-3.5 text-rose-400';
  } else {
    swapStatus.innerText = 'CLEAN (0h)';
    swapStatus.className = 'text-xs font-bold text-emerald-400 font-mono';
    swapIcon.setAttribute('data-lucide', 'check');
    swapIcon.className = 'h-3.5 w-3.5 text-emerald-400';
  }

  // Scam Signal
  const scamStatus = document.getElementById('sigStatusScam');
  const scamIcon = document.getElementById('sigIconScam');
  if (sig.is_on_active_voice_call) {
    scamStatus.innerText = 'CALL ACTIVE';
    scamStatus.className = 'text-xs font-bold text-amber-400 font-mono';
    scamIcon.setAttribute('data-lucide', 'phone-incoming');
    scamIcon.className = 'h-3.5 w-3.5 text-amber-400';
  } else {
    scamStatus.innerText = 'NO CALL';
    scamStatus.className = 'text-xs font-bold text-emerald-400 font-mono';
    scamIcon.setAttribute('data-lucide', 'phone-off');
    scamIcon.className = 'h-3.5 w-3.5 text-emerald-400';
  }

  // Device Status
  const devStatus = document.getElementById('sigStatusDevice');
  const devIcon = document.getElementById('sigIconDevice');
  if (sig.is_roaming) {
    devStatus.innerText = `ROAMING (${sig.roaming_country})`;
    devStatus.className = 'text-xs font-bold text-amber-400 font-mono';
    devIcon.setAttribute('data-lucide', 'globe');
    devIcon.className = 'h-3.5 w-3.5 text-amber-400';
  } else if (!sig.device_match) {
    devStatus.innerText = 'IMEI MISMATCH';
    devStatus.className = 'text-xs font-bold text-rose-400 font-mono';
    devIcon.setAttribute('data-lucide', 'smartphone-nfc');
    devIcon.className = 'h-3.5 w-3.5 text-rose-400';
  } else {
    devStatus.innerText = 'HOME NETWORK';
    devStatus.className = 'text-xs font-bold text-emerald-400 font-mono';
    devIcon.setAttribute('data-lucide', 'signal');
    devIcon.className = 'h-3.5 w-3.5 text-emerald-400';
  }

  // 5. Update Gemini 2.0 Flash AI Compliance Trace Log
  if (decision.ai_compliance_trace) {
    typewriterLog(decision.ai_compliance_trace);
  }

  // 6. Update Raw CAMARA Wire Inspector
  if (decision.raw_wire_trace) {
    renderWireInspector(decision.raw_wire_trace);
  }

  // 7. Update ISO 20022 Bank Rail Payload
  renderBankRailPayload(decision);

  if (window.lucide) lucide.createIcons();
}

// Render Wire Inspector Frame
function renderWireInspector(wire) {
  const methodEl = document.getElementById('wireMethod');
  const urlEl = document.getElementById('wireUrl');
  const statusEl = document.getElementById('wireStatus');
  const latencyEl = document.getElementById('wireLatency');
  const reqJsonEl = document.getElementById('wireRequestJson');
  const resJsonEl = document.getElementById('wireResponseJson');
  const carrierTagEl = document.getElementById('wireCarrierTag');

  if (methodEl) methodEl.innerText = wire.method || 'POST';
  if (urlEl) urlEl.innerText = wire.url || 'https://network-as-code.p.rapidapi.com...';
  if (statusEl) {
    statusEl.innerText = `${wire.response_status || 200} OK`;
    statusEl.className = wire.response_status < 400 
      ? 'px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 font-bold border border-emerald-800'
      : 'px-2 py-0.5 rounded bg-rose-950 text-rose-400 font-bold border border-rose-800';
  }
  if (latencyEl) latencyEl.innerText = `${wire.latency_ms || 12.8} ms`;
  if (carrierTagEl) carrierTagEl.innerText = `${wire.carrier_gateway || 'stc'} HSS/HLR`;

  if (reqJsonEl) {
    reqJsonEl.innerText = JSON.stringify(wire.request_payload || {}, null, 2);
  }
  if (resJsonEl) {
    resJsonEl.innerText = JSON.stringify(wire.response_payload || {}, null, 2);
  }
}

// Render ISO 20022 Banking Payload
function renderBankRailPayload(decision) {
  const bankRailEl = document.getElementById('bankRailJson');
  if (!bankRailEl) return;

  const recipientName = document.getElementById('inputRecipientName').value;
  const amount = document.getElementById('inputAmount').value;
  const currency = document.getElementById('selectCurrency').value;

  const isoPayload = {
    GrpHdr: {
      MsgId: `SAFEPAY/SARIE/${new Date().toISOString().slice(0,10).replace(/-/g,'')}/${decision.transaction_id.slice(-6)}`,
      CreDtTm: new Date().toISOString(),
      NbOfTxs: "1",
      InitgPty: {
        Nm: "SafePay MENA Telecom Pre-Auth Shield"
      }
    },
    CdtTrfTxInf: {
      PmtId: { EndToEndId: decision.transaction_id },
      IntrBkSttlmAmt: { Ccy: currency, Value: `${parseFloat(amount).toFixed(2)}` },
      Dbtr: {
        Nm: "Karim Abdelnabi",
        CtctDtls: { MobNb: decision.signals.phone_number }
      },
      Cdtr: { Nm: recipientName },
      RgltryRptg: {
        Dtls: {
          Cd: decision.decision === 'APPROVE' ? 'CAMARA_PASSKEY_VERIFIED' : 'CAMARA_CHALLENGE_FLAGGED',
          Prtry: decision.statutory_flags[0] || 'SAMA_INSTANT_TRANSFER_STANDARD_RULE',
          AuthrtyNm: currency === 'SAR' ? 'SAMA' : (currency === 'EGP' ? 'CBE' : 'CBUAE')
        }
      }
    }
  };

  bankRailEl.innerText = JSON.stringify(isoPayload, null, 2);
}

// Typewriter effect for AI Audit Log
function typewriterLog(text) {
  const logElem = document.getElementById('aiTraceLog');
  if (!logElem) return;
  logElem.innerText = '';
  let idx = 0;
  const speed = 6; // ms per char
  
  function type() {
    if (idx < text.length) {
      logElem.innerText += text.charAt(idx);
      idx++;
      setTimeout(type, speed);
    }
  }
  type();
}

// Confirm Biometric Face ID Step-Up Challenge
async function confirmBiometricStepUp() {
  document.getElementById('biometricModal').classList.add('hidden');
  
  try {
    const resp = await fetch('/api/v1/transfer/step-up/verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        transaction_id: currentTransactionId,
        biometric_token: 'face_id_token_' + Date.now(),
        biometric_type: 'FACE_ID',
        success: true
      })
    });
  } catch (e) {
    console.error('Step up confirmation failed:', e);
  }
}

function cancelTransfer() {
  document.getElementById('biometricModal').classList.add('hidden');
  alert('Transfer cancelled by user volition. Fraud risk avoided.');
}

function dismissBlockModal() {
  document.getElementById('blockModal').classList.add('hidden');
}

function renderStepUpResolved(data) {
  const decisionBadge = document.getElementById('decisionBadge');
  decisionBadge.innerText = 'APPROVED (POST-BIOMETRIC)';
  decisionBadge.className = 'text-xs font-bold px-3 py-1 rounded-lg bg-emerald-950 text-emerald-300 border border-emerald-700 tracking-wider font-mono';
  document.getElementById('actionText').innerText = data.message;
}
