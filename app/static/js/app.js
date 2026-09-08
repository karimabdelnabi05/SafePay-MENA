/**
 * SafePay MENA - Frontend Dashboard Client
 * Manages WebSocket telemetry, interactive mobile simulator, and live SVG gauge.
 */

let currentScenario = 'CLEAN_TRANSFER';
let currentTransactionId = 'txn_clean_001';
let socket = null;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  initWebSocket();
  loadScenario('CLEAN_TRANSFER');
});

// WebSocket Connection Management
function initWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${window.location.host}/ws/live-feed`;
  
  socket = new WebSocket(wsUrl);

  socket.onopen = () => {
    document.getElementById('wsStatus').innerText = 'Connected';
    document.getElementById('wsStatus').className = 'text-emerald-400 font-bold';
    console.log('SafePay WebSocket Connected');
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
    document.getElementById('wsStatus').innerText = 'Reconnecting...';
    document.getElementById('wsStatus').className = 'text-amber-400 font-bold';
    setTimeout(initWebSocket, 2000);
  };
}

// Preset Scenario Switcher
function loadScenario(type) {
  currentScenario = type;
  
  // Highlight active preset button
  ['Clean', 'Spam', 'Swap'].forEach(s => {
    const btn = document.getElementById(`btnScenario${s}`);
    if (btn) btn.classList.remove('ring-2', 'ring-cyan-400');
  });

  const activeBtnMap = {
    'CLEAN_TRANSFER': 'btnScenarioClean',
    'SPAM_CALL_SCAM': 'btnScenarioSpam',
    'SIM_SWAP_ATTACK': 'btnScenarioSwap'
  };
  const activeBtn = document.getElementById(activeBtnMap[type]);
  if (activeBtn) activeBtn.classList.add('ring-2', 'ring-cyan-400');

  const callBanner = document.getElementById('activeCallBanner');
  const savedBadge = document.getElementById('savedBadge');
  const carrierTag = document.getElementById('carrierTag');
  const inputRecipient = document.getElementById('inputRecipientName');
  const inputAmount = document.getElementById('inputAmount');
  const selectCurrency = document.getElementById('selectCurrency');
  const callIndicatorDot = document.getElementById('callIndicatorDot');
  const callIndicatorText = document.getElementById('callIndicatorText');

  if (type === 'CLEAN_TRANSFER') {
    callBanner.classList.add('hidden');
    savedBadge.classList.remove('hidden');
    carrierTag.innerText = 'stc Saudi 5G';
    inputRecipient.value = 'Fatima Mohamed (Mom)';
    inputAmount.value = '200';
    selectCurrency.value = 'SAR';
    updateCurrency('SAR');
    callIndicatorDot.className = 'h-2 w-2 rounded-full bg-slate-600';
    callIndicatorText.innerText = 'Cellular LTE';
  } 
  else if (type === 'SPAM_CALL_SCAM') {
    callBanner.classList.remove('hidden');
    savedBadge.classList.add('hidden');
    carrierTag.innerText = 'stc Saudi (Active Call)';
    inputRecipient.value = 'Unknown Payee (Scammer)';
    inputAmount.value = '15000';
    selectCurrency.value = 'SAR';
    updateCurrency('SAR');
    callIndicatorDot.className = 'h-2 w-2 rounded-full bg-amber-400 animate-ping';
    callIndicatorText.innerText = 'Call in Progress';
  } 
  else if (type === 'SIM_SWAP_ATTACK') {
    callBanner.classList.add('hidden');
    savedBadge.classList.add('hidden');
    carrierTag.innerText = 'Rogue Device (IMEI Mismatch)';
    inputRecipient.value = 'Mule Account Corp';
    inputAmount.value = '35000';
    selectCurrency.value = 'SAR';
    updateCurrency('SAR');
    callIndicatorDot.className = 'h-2 w-2 rounded-full bg-rose-500 animate-pulse';
    callIndicatorText.innerText = 'SIM Alert';
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
  const isSaved = currentScenario === 'CLEAN_TRANSFER';
  
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
    } else if (decision.decision === 'APPROVE') {
      // Confetti effect for instant approval
      if (window.confetti) {
        confetti({
          particleCount: 50,
          spread: 60,
          origin: { y: 0.8 }
        });
      }
    }

  } catch (err) {
    console.error('Evaluation failed:', err);
    alert('Evaluation request failed. Check server logs.');
  } finally {
    btn.disabled = false;
    btnText.innerText = 'Authorize & Send';
  }
}

// Render Risk Decision & CAMARA Telemetry to SOC Panel
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
  let badgeClass = 'text-lg font-black px-4 py-1.5 rounded-xl bg-emerald-950/80 text-emerald-400 border border-emerald-700/60 tracking-wider';

  if (tier === 'STEP_UP') {
    tierColor = '#F59E0B';
    badgeClass = 'text-lg font-black px-4 py-1.5 rounded-xl bg-amber-950/80 text-amber-400 border border-amber-700/60 tracking-wider animate-pulse';
  } else if (tier === 'BLOCK') {
    tierColor = '#EF4444';
    badgeClass = 'text-lg font-black px-4 py-1.5 rounded-xl bg-rose-950/80 text-rose-400 border border-rose-700/60 tracking-wider animate-bounce';
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

  document.getElementById('engineLatency').innerText = `${decision.execution_time_ms || 2.4} ms`;
  document.getElementById('decisionTimeBadge').innerText = `${decision.execution_time_ms || 2.4} ms`;

  // 3. Update CAMARA Telemetry Badges
  const sig = decision.signals;
  
  // Number Verify
  const numStatus = document.getElementById('sigStatusNum');
  const numIcon = document.getElementById('sigIconNum');
  if (sig.number_verified) {
    numStatus.innerText = 'VERIFIED';
    numStatus.className = 'text-xs font-black text-emerald-400 font-mono';
    numIcon.setAttribute('data-lucide', 'check');
    numIcon.className = 'h-3.5 w-3.5 text-emerald-400';
  } else {
    numStatus.innerText = 'FAILED (Rogue)';
    numStatus.className = 'text-xs font-black text-rose-400 font-mono';
    numIcon.setAttribute('data-lucide', 'x');
    numIcon.className = 'h-3.5 w-3.5 text-rose-400';
  }

  // SIM Swap
  const swapStatus = document.getElementById('sigStatusSwap');
  const swapIcon = document.getElementById('sigIconSwap');
  if (sig.sim_swapped_recently) {
    swapStatus.innerText = `SWAPPED (${sig.sim_swap_hours_ago || 2.1}h)`;
    swapStatus.className = 'text-xs font-black text-rose-400 font-mono';
    swapIcon.setAttribute('data-lucide', 'alert-octagon');
    swapIcon.className = 'h-3.5 w-3.5 text-rose-400';
  } else {
    swapStatus.innerText = 'CLEAN (0h)';
    swapStatus.className = 'text-xs font-black text-emerald-400 font-mono';
    swapIcon.setAttribute('data-lucide', 'check');
    swapIcon.className = 'h-3.5 w-3.5 text-emerald-400';
  }

  // Scam Signal
  const scamStatus = document.getElementById('sigStatusScam');
  const scamIcon = document.getElementById('sigIconScam');
  if (sig.is_on_active_voice_call) {
    scamStatus.innerText = 'CALL ACTIVE';
    scamStatus.className = 'text-xs font-black text-amber-400 font-mono animate-pulse';
    scamIcon.setAttribute('data-lucide', 'phone-incoming');
    scamIcon.className = 'h-3.5 w-3.5 text-amber-400';
  } else {
    scamStatus.innerText = 'NO CALL';
    scamStatus.className = 'text-xs font-black text-emerald-400 font-mono';
    scamIcon.setAttribute('data-lucide', 'phone-off');
    scamIcon.className = 'h-3.5 w-3.5 text-emerald-400';
  }

  // Device Status
  const devStatus = document.getElementById('sigStatusDevice');
  const devIcon = document.getElementById('sigIconDevice');
  if (sig.is_roaming) {
    devStatus.innerText = `ROAMING (${sig.roaming_country})`;
    devStatus.className = 'text-xs font-black text-amber-400 font-mono';
    devIcon.setAttribute('data-lucide', 'globe');
    devIcon.className = 'h-3.5 w-3.5 text-amber-400';
  } else if (!sig.device_match) {
    devStatus.innerText = 'IMEI MISMATCH';
    devStatus.className = 'text-xs font-black text-rose-400 font-mono';
    devIcon.setAttribute('data-lucide', 'smartphone-nfc');
    devIcon.className = 'h-3.5 w-3.5 text-rose-400';
  } else {
    devStatus.innerText = 'HOME NETWORK';
    devStatus.className = 'text-xs font-black text-emerald-400 font-mono';
    devIcon.setAttribute('data-lucide', 'signal');
    devIcon.className = 'h-3.5 w-3.5 text-emerald-400';
  }

  // 4. Update Gemini 2.0 Flash AI Compliance Trace Log
  if (decision.ai_compliance_trace) {
    typewriterLog(decision.ai_compliance_trace);
  }

  if (window.lucide) lucide.createIcons();
}

// Typewriter effect for AI Audit Log
function typewriterLog(text) {
  const logElem = document.getElementById('aiTraceLog');
  logElem.innerText = '';
  let idx = 0;
  const speed = 8; // ms per char
  
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
    
    if (window.confetti) {
      confetti({
        particleCount: 80,
        spread: 70,
        origin: { y: 0.6 }
      });
    }
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
  decisionBadge.className = 'text-sm font-black px-3 py-1.5 rounded-xl bg-emerald-950/80 text-emerald-300 border border-emerald-600 tracking-wider';
  document.getElementById('actionText').innerText = data.message;
}
