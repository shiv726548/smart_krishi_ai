// Smart Krishi AI - Responsive Web + Mobile Application

let isPumpOn = false;
let currentScreen = "dashboard";

const API_BASE = "";


// ============================================================
// NAVIGATION
// ============================================================

function switchScreen(screenId) {
    currentScreen = screenId;

    document.querySelectorAll(".screen").forEach(screen => {
        screen.classList.remove("active");
    });

    const target = document.getElementById(`screen-${screenId}`);

    if (target) {
        target.classList.add("active");
    }

    document.querySelectorAll(".nav-item").forEach(button => {
        button.classList.remove("active");
    });

    const desktopButton = document.getElementById(`nav-${screenId}`);

    if (desktopButton) {
        desktopButton.classList.add("active");
    }

    document.querySelectorAll(".mobile-nav button").forEach(button => {
        button.classList.remove("active");
    });

    const mobileButton = document.getElementById(`mobile-${screenId}`);

    if (mobileButton) {
        mobileButton.classList.add("active");
    }

    refreshIcons();
}


// ============================================================
// ICONS
// ============================================================

function refreshIcons() {
    if (window.lucide) {
        lucide.createIcons();
    }
}


// ============================================================
// DASHBOARD TELEMETRY
// ============================================================

async function updateSimulatedTelemetry() {

    const moistureElement = document.getElementById("sliderMoisture");
    const tempElement = document.getElementById("sliderTemp");
    const humidityElement = document.getElementById("sliderHumidity");

    if (!moistureElement || !tempElement || !humidityElement) {
        return;
    }

    const moisture = parseFloat(moistureElement.value);
    const temp = parseFloat(tempElement.value);
    const humidity = parseFloat(humidityElement.value);

    const lblMoisture = document.getElementById("lblMoisture");
    const lblTemp = document.getElementById("lblTemp");
    const lblHumidity = document.getElementById("lblHumidity");

    const valMoisture = document.getElementById("val-moisture");
    const valTemp = document.getElementById("val-temp");
    const valHumidity = document.getElementById("val-humidity");

    if (lblMoisture) {
        lblMoisture.innerText = `${moisture.toFixed(1)}%`;
    }

    if (lblTemp) {
        lblTemp.innerText = `${temp.toFixed(1)}°C`;
    }

    if (lblHumidity) {
        lblHumidity.innerText = `${humidity}%`;
    }

    if (valMoisture) {
        valMoisture.innerText = `${moisture.toFixed(1)}%`;
    }

    if (valTemp) {
        valTemp.innerText = `${temp.toFixed(1)}°C`;
    }

    if (valHumidity) {
        valHumidity.innerText = `${humidity}%`;
    }


    // Automatic irrigation recommendation
    if (moisture < 40) {
        setPumpUI(true);
    } else if (moisture >= 70) {
        setPumpUI(false);
    }


    // Send telemetry to backend
    try {

        const response = await fetch(
            `${API_BASE}/api/sensors/telemetry`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    device_id: "ESP32_KRISHI_01",
                    soil_moisture: moisture,
                    temperature: temp,
                    humidity: humidity
                })
            }
        );

        if (response.ok) {

            const data = await response.json();

            if (data.pump_status !== undefined) {
                setPumpUI(data.pump_status);
            }
        }

    } catch (error) {

        console.log(
            "Telemetry API unavailable. Running local simulation."
        );
    }
}


// ============================================================
// PUMP CONTROL
// ============================================================

async function togglePumpWeb() {

    const nextState = !isPumpOn;

    setPumpUI(nextState);

    try {

        const response = await fetch(
            `${API_BASE}/api/sensors/pump/toggle`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    device_id: "ESP32_KRISHI_01",
                    action: nextState ? "ON" : "OFF"
                })
            }
        );

        if (response.ok) {

            const data = await response.json();

            if (data.pump_status !== undefined) {
                setPumpUI(data.pump_status);
            }
        }

    } catch (error) {

        console.log(
            "Pump API unavailable. Running local pump simulation."
        );
    }
}


function setPumpUI(status) {

    isPumpOn = Boolean(status);

    const button = document.getElementById("pumpToggleBtn");
    const text = document.getElementById("pumpStatusText");
    const icon = document.getElementById("pumpIconBg");

    if (!button || !text || !icon) {
        return;
    }


    if (isPumpOn) {

        button.innerText = "STOP";

        button.className =
            "px-3 py-1.5 bg-red-600 hover:bg-red-500 text-white rounded-xl text-xs font-bold transition";

        text.innerText =
            "Status: ON (Irrigating Field)";

        text.className =
            "text-[11px] text-emerald-400 font-bold animate-pulse";

        icon.className =
            "w-10 h-10 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center";

    } else {

        button.innerText = "START";

        button.className =
            "px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold transition";

        text.innerText =
            "Status: OFF (Standby)";

        text.className =
            "text-[11px] text-slate-400";

        icon.className =
            "w-10 h-10 rounded-full bg-slate-800 text-slate-400 flex items-center justify-center";
    }

    refreshIcons();
}


// ============================================================
// CROP SCANNER
// ============================================================

function previewAndScanLeaf(event) {

    const file =
        event &&
        event.target &&
        event.target.files
            ? event.target.files[0]
            : null;

    if (!file) {
        return;
    }

    const preview =
        document.getElementById("leafPreview");

    if (preview) {

        const reader = new FileReader();

        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.classList.remove("hidden");
        };

        reader.readAsDataURL(file);
    }

    simulateLeafScan();
}


function simulateLeafScan() {

    const card =
        document.getElementById("scanResultCard");

    if (!card) {
        return;
    }

    card.classList.remove("hidden");

    const confidence =
        document.getElementById("resConf");

    const disease =
        document.getElementById("resDisease");

    const symptoms =
        document.getElementById("resSymptoms");

    const actions =
        document.getElementById("resActions");


    if (confidence) {
        confidence.innerText = "94%";
    }

    if (disease) {
        disease.innerText =
            "Tomato Early Blight";
    }

    if (symptoms) {
        symptoms.innerText =
            "Brown spots, yellowing leaves and dark circular lesions.";
    }

    if (actions) {
        actions.innerText =
            "Remove affected leaves, improve airflow and avoid overhead watering.";
    }

    card.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


// ============================================================
// AI ASSISTANT
// ============================================================

async function sendChatMessage() {

    const input =
        document.getElementById("chatInput");

    const chatHistory =
        document.getElementById("chatMessages");

    const languageElement =
        document.getElementById("assistantLang");


    if (!input || !chatHistory) {
        return;
    }


    const text =
        input.value.trim();

    if (!text) {
        return;
    }


    const language =
        languageElement
            ? languageElement.value
            : "en";


    // User message
    const userMessage =
        document.createElement("div");

    userMessage.className =
        "bg-emerald-800 border border-emerald-600 p-2.5 rounded-xl text-white max-w-[85%] ml-auto text-xs mb-2";

    userMessage.innerText = text;

    chatHistory.appendChild(userMessage);

    input.value = "";

    chatHistory.scrollTop =
        chatHistory.scrollHeight;


    // Typing indicator
    const typing =
        document.createElement("div");

    typing.id = "aiTypingIndicator";

    typing.className =
        "bg-slate-900 border border-slate-800 p-2.5 rounded-xl text-slate-400 max-w-[85%] text-xs mb-2";

    typing.innerText =
        "Smart Krishi AI is thinking...";

    chatHistory.appendChild(typing);

    chatHistory.scrollTop =
        chatHistory.scrollHeight;


    let botReply = "";


    // ========================================================
    // TRY BACKEND AI
    // ========================================================

    try {

        const response =
            await fetch(
                `${API_BASE}/api/assistant/chat`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        message: text,
                        language: language,
                        crop_name: "Tomato"
                    })
                }
            );


        if (response.ok) {

            const data =
                await response.json();

            botReply =
                data.reply ||
                data.response ||
                data.message ||
                "";
        }

    } catch (error) {

        console.log(
            "AI backend unavailable. Using local Smart Krishi AI."
        );
    }


    // Remove typing indicator
    const typingElement =
        document.getElementById(
            "aiTypingIndicator"
        );

    if (typingElement) {
        typingElement.remove();
    }


    // ========================================================
    // LOCAL AI FALLBACK
    // ========================================================

    if (!botReply) {

        botReply =
            generateLocalAIResponse(
                text,
                language
            );
    }


    // AI message
    const botMessage =
        document.createElement("div");

    botMessage.className =
        "bg-slate-900 border border-slate-800 p-2.5 rounded-xl text-slate-200 max-w-[85%] text-xs mb-2";

    botMessage.innerText =
        botReply;

    chatHistory.appendChild(botMessage);

    chatHistory.scrollTop =
        chatHistory.scrollHeight;


    speakText(
        botReply,
        language
    );
}


// ============================================================
// LOCAL AI RESPONSE
// ============================================================

function generateLocalAIResponse(question, language) {

    const q =
        question.toLowerCase();


    if (
        q.includes("water") ||
        q.includes("irrigation") ||
        q.includes("पाणी") ||
        q.includes("सिंचन") ||
        q.includes("पाणी कधी")
    ) {

        if (language === "mr") {

            return "सध्याच्या मातीतील ओलावा पाहता पिकाला हलके सिंचन देणे योग्य आहे. माती खूप ओली असल्यास पाणी देणे टाळा.";

        }

        if (language === "hi") {

            return "मिट्टी की नमी कम होने पर हल्की सिंचाई करें। यदि मिट्टी पहले से बहुत गीली है तो पानी देने से बचें.";

        }

        return "Based on the simulated soil conditions, give light irrigation when soil moisture is low. Avoid watering if the soil is already wet.";
    }


    if (
        q.includes("tomato") ||
        q.includes("टोमॅटो") ||
        q.includes("टमाटर")
    ) {

        if (language === "mr") {

            return "टोमॅटो पिकासाठी नियमित पाणी व्यवस्थापन, योग्य निचरा आणि पानांवर डाग दिसल्यास त्वरित तपासणी महत्त्वाची आहे.";

        }

        if (language === "hi") {

            return "टमाटर की फसल में उचित सिंचाई, जल निकासी और पत्तियों पर दाग दिखाई देने पर तुरंत जांच जरूरी है.";

        }

        return "For tomatoes, maintain consistent irrigation, good drainage and inspect leaves regularly for spots or discoloration.";
    }


    if (
        q.includes("disease") ||
        q.includes("diseases") ||
        q.includes("रोग") ||
        q.includes("disease")
    ) {

        if (language === "mr") {

            return "पानांवर डाग, पिवळेपणा किंवा वाळणे दिसत असल्यास फोटो स्कॅनरमध्ये अपलोड करा. Smart Krishi AI प्राथमिक रोग ओळखण्यात मदत करेल.";

        }

        if (language === "hi") {

            return "यदि पत्तियों पर दाग, पीलापन या सूखापन दिखाई दे तो फोटो स्कैनर में अपलोड करें. Smart Krishi AI प्राथमिक रोग पहचान में मदद करेगा.";

        }

        return "If you see spots, yellowing or wilting leaves, upload a photo to the Crop Scanner for a preliminary disease assessment.";
    }


    if (
        q.includes("weather") ||
        q.includes("rain") ||
        q.includes("पाऊस") ||
        q.includes("हवामान") ||
        q.includes("बारिश")
    ) {

        if (language === "mr") {

            return "हवामानानुसार सिंचनाचे नियोजन करा. पावसाची शक्यता असल्यास अतिरिक्त सिंचन टाळणे चांगले.";

        }

        if (language === "hi") {

            return "मौसम के अनुसार सिंचाई की योजना बनाएं। बारिश की संभावना होने पर अतिरिक्त सिंचाई से बचें.";

        }

        return "Plan irrigation according to the weather. If rain is expected, avoid unnecessary additional irrigation.";
    }


    if (
        q.includes("fertilizer") ||
        q.includes("खत") ||
        q.includes("उर्वरक")
    ) {

        if (language === "mr") {

            return "खत वापरण्यापूर्वी पिकाची अवस्था, मातीची स्थिती आणि उपलब्ध माती परीक्षण माहिती तपासा.";

        }

        if (language === "hi") {

            return "उर्वरक देने से पहले फसल की अवस्था, मिट्टी की स्थिति और उपलब्ध मिट्टी परीक्षण रिपोर्ट देखें.";

        }

        return "Before applying fertilizer, consider the crop stage, soil condition and available soil-test information.";
    }


    if (language === "mr") {

        return "मी Smart Krishi AI आहे. तुम्ही पाणी, पिकांचे रोग, हवामान, खत किंवा पिकांच्या व्यवस्थापनाबद्दल प्रश्न विचारू शकता.";

    }

    if (language === "hi") {

        return "मैं Smart Krishi AI हूं. आप सिंचाई, फसल रोग, मौसम, उर्वरक या फसल प्रबंधन के बारे में प्रश्न पूछ सकते हैं.";

    }

    return "I am Smart Krishi AI. You can ask me about irrigation, crop diseases, weather, fertilizers or crop management.";
}


// ============================================================
// VOICE INPUT
// ============================================================

function startVoiceInput() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {

        alert(
            "Speech recognition is not supported in this browser. Please type your question."
        );

        return;
    }


    const languageElement =
        document.getElementById(
            "assistantLang"
        );


    const language =
        languageElement
            ? languageElement.value
            : "en";


    const recognition =
        new SpeechRecognition();


    recognition.lang =
        language === "hi"
            ? "hi-IN"
            : language === "mr"
                ? "mr-IN"
                : "en-IN";


    recognition.interimResults = false;

    recognition.continuous = false;


    recognition.onstart = function() {

        const input =
            document.getElementById(
                "chatInput"
            );

        if (input) {
            input.placeholder =
                "Listening...";
        }
    };


    recognition.onresult =
        function(event) {

            const speechResult =
                event.results[0][0].transcript;


            const input =
                document.getElementById(
                    "chatInput"
                );


            if (input) {
                input.value =
                    speechResult;
            }


            sendChatMessage();
        };


    recognition.onerror =
        function() {

            const input =
                document.getElementById(
                    "chatInput"
                );

            if (input) {
                input.placeholder =
                    "Ask Smart Krishi AI...";
            }
        };


    recognition.onend =
        function() {

            const input =
                document.getElementById(
                    "chatInput"
                );

            if (input) {
                input.placeholder =
                    "Ask Smart Krishi AI...";
            }
        };


    recognition.start();
}


// ============================================================
// TEXT TO SPEECH
// ============================================================

function speakText(text, language) {

    if (!("speechSynthesis" in window)) {
        return;
    }


    window.speechSynthesis.cancel();


    const utterance =
        new SpeechSynthesisUtterance(text);


    utterance.lang =
        language === "hi"
            ? "hi-IN"
            : language === "mr"
                ? "mr-IN"
                : "en-IN";


    utterance.rate = 0.95;

    utterance.pitch = 1;


    window.speechSynthesis.speak(
        utterance
    );
}


// ============================================================
// QUICK QUESTIONS
// ============================================================

function sendQuickQuestion(question) {

    const input =
        document.getElementById(
            "chatInput"
        );


    if (!input) {
        return;
    }


    input.value =
        question;


    sendChatMessage();
}


// ============================================================
// ENTER KEY
// ============================================================

function setupChatInput() {

    const input =
        document.getElementById(
            "chatInput"
        );


    if (!input) {
        return;
    }


    input.addEventListener(
        "keydown",
        function(event) {

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();

                sendChatMessage();
            }
        }
    );
}


// ============================================================
// VIEW MODE
// ============================================================

function toggleViewMode() {

    const container =
        document.getElementById(
            "mobileContainer"
        );

    const button =
        document.getElementById(
            "viewToggleBtn"
        );


    if (!container || !button) {
        return;
    }


    container.classList.toggle(
        "desktop-view"
    );


    const isDesktop =
        container.classList.contains(
            "desktop-view"
        );


    if (isDesktop) {

        button.innerHTML =
            '<i data-lucide="smartphone"></i> Mobile Frame Mode';

    } else {

        button.innerHTML =
            '<i data-lucide="monitor"></i> Desktop View';
    }


    refreshIcons();
}


// ============================================================
// SYSTEM STATUS
// ============================================================

async function checkBackendStatus() {

    try {

        const response =
            await fetch(
                `${API_BASE}/`
            );


        if (response.ok) {

            console.log(
                "Smart Krishi AI backend connected."
            );

            return true;
        }

    } catch (error) {

        console.log(
            "Backend connection unavailable."
        );
    }


    return false;
}


// ============================================================
// INITIALIZATION
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        console.log(
            "Smart Krishi AI frontend loaded."
        );


        setPumpUI(false);

        setupChatInput();

        checkBackendStatus();

        refreshIcons();


        // Make Dashboard active
        switchScreen("dashboard");


        // Initial telemetry values
        updateSimulatedTelemetry();
    }
);