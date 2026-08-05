// Smart Krishi AI - Mobile & Web Application Script

let isPumpOn = false;
let currentScreen = 'dashboard';
const API_BASE = 'http://localhost:8000';

function switchScreen(screenId) {
  currentScreen = screenId;
  document.querySelectorAll('.screen-view').forEach(s => s.classList.add('hidden'));
  document.getElementById(`screen-${screenId}`).classList.remove('hidden');

  // Reset nav highlights
  document.querySelectorAll('nav button').forEach(btn => {
    btn.classList.remove('text-emerald-400');
    btn.classList.add('hover:text-white');
  });
  const activeBtn = document.getElementById(`nav-${screenId}`);
  if (activeBtn) {
    activeBtn.classList.add('text-emerald-400');
    activeBtn.classList.remove('hover:text-white');
  }
}

async function updateSimulatedTelemetry() {
  const moisture = parseFloat(document.getElementById('sliderMoisture').value);
  const temp = parseFloat(document.getElementById('sliderTemp').value);
  const humidity = parseFloat(document.getElementById('sliderHumidity').value);

  document.getElementById('lblMoisture').innerText = `${moisture.toFixed(1)}%`;
  document.getElementById('lblTemp').innerText = `${temp.toFixed(1)}°C`;
  document.getElementById('lblHumidity').innerText = `${humidity}%`;

  document.getElementById('val-moisture').innerText = `${moisture.toFixed(1)}%`;
  document.getElementById('val-temp').innerText = `${temp.toFixed(1)}°C`;
  document.getElementById('val-humidity').innerText = `${humidity}%`;

  // Send to backend API
  try {
    const res = await fetch(`${API_BASE}/api/sensors/telemetry`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        device_id: "ESP32_KRISHI_01",
        soil_moisture: moisture,
        temperature: temp,
        humidity: humidity
      })
    });
    if (res.ok) {
      const data = await res.json();
      if (data.pump_status !== undefined) {
        setPumpUI(data.pump_status);
      }
    }
  } catch (err) {
    // Local fallback evaluation if backend not reachable
    if (moisture < 40 && !isPumpOn) {
      setPumpUI(true);
    } else if (moisture >= 70 && isPumpOn) {
      setPumpUI(false);
    }
  }
}

async function togglePumpWeb() {
  const nextState = !isPumpOn;
  try {
    const res = await fetch(`${API_BASE}/api/sensors/pump/toggle`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        device_id: "ESP32_KRISHI_01",
        action: nextState ? "ON" : "OFF"
      })
    });
    if (res.ok) {
      const data = await res.json();
      setPumpUI(data.pump_status);
      return;
    }
  } catch (e) {
    console.log("Local pump toggle");
  }
  setPumpUI(nextState);
}

function setPumpUI(status) {
  isPumpOn = status;
  const btn = document.getElementById('pumpToggleBtn');
  const txt = document.getElementById('pumpStatusText');
  const icon = document.getElementById('pumpIconBg');

  if (isPumpOn) {
    btn.innerText = "STOP";
    btn.className = "px-3 py-1.5 bg-red-600 hover:bg-red-500 text-white rounded-xl text-xs font-bold transition";
    txt.innerText = "Status: ON (Irrigating Field)";
    txt.className = "text-[11px] text-emerald-400 font-bold animate-pulse";
    icon.className = "w-10 h-10 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center";
  } else {
    btn.innerText = "START";
    btn.className = "px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold transition";
    txt.innerText = "Status: OFF (Standby)";
    txt.className = "text-[11px] text-slate-400";
    icon.className = "w-10 h-10 rounded-full bg-slate-800 text-slate-400 flex items-center justify-center";
  }
}

function simulateLeafScan() {
  const card = document.getElementById('scanResultCard');
  card.classList.remove('hidden');
  card.scrollIntoView({ behavior: 'smooth' });
}

function previewAndScanLeaf(event) {
  if (event.target.files && event.target.files[0]) {
    simulateLeafScan();
  }
}

async function sendChatMessage() {
  const input = document.getElementById('chatInput');
  const text = input.value.trim();
  if (!text) return;

  const lang = document.getElementById('assistantLang').value;
  const chatHistory = document.getElementById('chatMessages');

  // User msg
  const userDiv = document.createElement('div');
  userDiv.className = 'bg-emerald-800 border border-emerald-600 p-2.5 rounded-xl text-white max-w-[85%] ml-auto text-xs';
  userDiv.innerText = text;
  chatHistory.appendChild(userDiv);
  input.value = '';
  chatHistory.scrollTop = chatHistory.scrollHeight;

  // Bot response from API or fallback
  let botReply = "";
  try {
    const res = await fetch(`${API_BASE}/api/assistant/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text, language: lang, crop_name: "Tomato" })
    });
    if (res.ok) {
      const data = await res.json();
      botReply = data.reply;
    }
  } catch (err) {
    botReply = "Based on current soil moisture (38.5%), your tomato crop requires light irrigation today.";
  }

  if (!botReply) {
    botReply = "I am your Smart Krishi AI assistant. Please check moisture levels before watering.";
  }

  const botDiv = document.createElement('div');
  botDiv.className = 'bg-slate-900 border border-slate-800 p-2.5 rounded-xl text-slate-200 max-w-[85%] text-xs';
  botDiv.innerText = botReply;
  chatHistory.appendChild(botDiv);
  chatHistory.scrollTop = chatHistory.scrollHeight;

  // Speech Output (Voice TTS)
  speakText(botReply, lang);
}

function startVoiceInput() {
  if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
    alert("Speech recognition is not supported in this browser window. Try typing your question!");
    return;
  }
  const lang = document.getElementById('assistantLang').value;
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();

  recognition.lang = lang === 'hi' ? 'hi-IN' : (lang === 'mr' ? 'mr-IN' : 'en-US');
  recognition.onresult = function(event) {
    const speechResult = event.results[0][0].transcript;
    document.getElementById('chatInput').value = speechResult;
    sendChatMessage();
  };
  recognition.start();
}

function speakText(text, lang) {
  if ('speechSynthesis' in window) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang === 'hi' ? 'hi-IN' : (lang === 'mr' ? 'mr-IN' : 'en-US');
    window.speechSynthesis.speak(utterance);
  }
}

function toggleViewMode() {
  const container = document.getElementById('mobileContainer');
  const btn = document.getElementById('viewToggleBtn');
  if (container.classList.contains('py-4')) {
    btn.innerHTML = '<i class="fa-solid fa-expand"></i> Mobile Frame Mode';
  } else {
    btn.innerHTML = '<i class="fa-solid fa-mobile-screen"></i> Mobile Simulator View';
  }
}
