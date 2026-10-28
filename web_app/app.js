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

function updateSimulatedTelemetry() {

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


    const sourceLabel = document.getElementById("dataSourceLabel");
    if (sourceLabel) sourceLabel.innerText = "DEMO VALUES — not live sensor data";
}


// ============================================================
// PUMP CONTROL
// ============================================================

async function togglePumpWeb() {
    setPumpUI(false);
}


function setPumpUI(status) {

    // This web simulator must never issue or imply a physical pump command.
    isPumpOn = false;

    const button = document.getElementById("pumpToggleBtn");
    const text = document.getElementById("pumpStatusText");
    const icon = document.getElementById("pumpIconBg");

    if (!button || !text || !icon) {
        return;
    }


    button.innerText = "DISABLED";
    button.disabled = true;
    button.title = "Hardware control is disabled in the demo";
    text.innerText = "Demo only — no pump connected";
    text.className = "text-[11px] text-amber-300";
    icon.className =
        "w-10 h-10 rounded-full bg-slate-800 text-slate-400 flex items-center justify-center";

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

    if (!["image/jpeg", "image/png", "image/webp"].includes(file.type)) {
        alert("Choose a JPEG, PNG, or WebP image.");
        return;
    }
    if (file.size > 5 * 1024 * 1024) {
        alert("Image is too large. The maximum size is 5 MB.");
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

    card.style.display = "block";

    const confidence =
        document.querySelector(".confidence");

    const disease =
        document.getElementById("resDisease");

    const symptoms =
        document.getElementById("resSymptoms");

    const actions =
        document.getElementById("resActions");


    if (confidence) {
        confidence.style.display = "none";
    }

    if (disease) {
        disease.innerText =
            "Diagnosis unavailable";
    }

    if (symptoms) {
        symptoms.innerText =
            "No trained disease-detection model is installed. This image was not classified.";
    }

    if (actions) {
        actions.innerText =
            "No disease label, confidence score, or treatment recommendation was generated.";
    }

    const header = card.querySelector(".result-header strong");
    if (header) header.innerText = "No diagnosis generated";

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

            return "सत्यापित माती-ओलावा रीडिंग उपलब्ध नाही. सिंचनाचा निर्णय घेण्यापूर्वी माती आणि पिकाची अवस्था तपासा.";

        }

        if (language === "hi") {

            return "मिट्टी की सत्यापित नमी रीडिंग उपलब्ध नहीं है। सिंचाई का निर्णय लेने से पहले मिट्टी और फसल की अवस्था जांचें।";

        }

        return "No verified soil-moisture reading is available. Check the soil and crop stage before deciding whether to irrigate.";
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

            return "या डेमोमध्ये प्रशिक्षित रोग-ओळख मॉडेल नाही. पानांवरील लक्षणांसाठी स्थानिक कृषी तज्ज्ञांचा सल्ला घ्या.";

        }

        if (language === "hi") {

            return "इस डेमो में प्रशिक्षित रोग-पहचान मॉडल नहीं है। पत्तियों के लक्षणों के लिए स्थानीय कृषि विशेषज्ञ से सलाह लें.";

        }

        return "The crop scanner currently validates the upload only; no trained disease model is installed, so it cannot diagnose the plant.";
    }


    if (
        q.includes("weather") ||
        q.includes("rain") ||
        q.includes("पाऊस") ||
        q.includes("हवामान") ||
        q.includes("बारिश")
    ) {

        if (language === "mr") {

            return "या डेमोमध्ये हवामानाचा अंदाज उपलब्ध नाही. सिंचनाचे नियोजन करण्यापूर्वी विश्वसनीय स्थानिक अंदाज तपासा.";

        }

        if (language === "hi") {

            return "इस डेमो में मौसम का पूर्वानुमान उपलब्ध नहीं है। सिंचाई की योजना से पहले विश्वसनीय स्थानीय पूर्वानुमान देखें।";

        }

        return "Live weather is unavailable in this demo. Check a trusted local forecast and the field before changing irrigation.";
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

        return "मी नियम-आधारित कृषी डेमो सहाय्यक आहे. सर्वसाधारण माहिती विचारा आणि पिकाविषयी निर्णय स्थानिक पातळीवर तपासा.";

    }

    if (language === "hi") {

        return "मैं नियम-आधारित कृषि डेमो सहायक हूं। सामान्य जानकारी पूछें और फसल से जुड़े निर्णय स्थानीय स्तर पर जांचें।";

    }

        return "I am a rule-based farming assistant demo. I can offer general guidance, but I do not have verified live farm or weather data.";
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