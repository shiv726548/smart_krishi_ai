from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from backend.routers.sensors import SYSTEM_STATE
from backend.models import User
from backend.security import require_farm_owner

router = APIRouter(prefix="/api/assistant", tags=["AI Farming Assistant"])

class ChatQuery(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    language: str = "en" # en, hi, mr
    crop_name: Optional[str] = Field(default=None, max_length=80)

# Smart Knowledge Graph responses for agronomy & IoT telemetry
RESPONSES_KNOWLEDGE = {
    "en": {
        "yellow": "Leaf yellowing has several possible causes and cannot be diagnosed from text alone. Check moisture and drainage, inspect both sides of leaves, and consult a local agricultural expert before treatment.",
        "water": "Authenticated field-sensor soil moisture is {moisture}%. The configured threshold is {min_moisture}%. {irrigation_advice}",
        "fertilizer": "Fertilizer needs depend on crop stage, a soil test, and local guidance. No soil-test data is available here; do not choose a product or dose based only on this demo.",
        "pump": "Current pump status is {pump_status}.",
        "weather": "A weather forecast is unavailable because no weather service is configured. Check a trusted local forecast before planning irrigation.",
        "temperature": "Authenticated field-sensor readings: {temp}°C and {humidity}% humidity. These are not a weather forecast.",
        "default": "I am a rule-based farming assistant demo. Ask for general guidance, but verify crop-specific decisions locally."
    },
    "hi": {
        "yellow": "पत्तियों का पीला होना कई कारणों से हो सकता है; केवल पाठ से निदान नहीं किया जा सकता। नमी और जल-निकासी जांचें, पत्तियों के दोनों ओर देखें और उपचार से पहले स्थानीय कृषि विशेषज्ञ से सलाह लें।",
        "water": "प्रमाणित खेत-सेंसर की मिट्टी नमी रीडिंग {moisture}% है। निर्धारित सीमा {min_moisture}% है। {irrigation_advice_hi}",
        "fertilizer": "उर्वरक की जरूरत फसल की अवस्था, मिट्टी की जांच और स्थानीय सलाह पर निर्भर करती है। यहां मिट्टी की जांच का डेटा नहीं है; केवल इस डेमो के आधार पर कोई उत्पाद या मात्रा न चुनें।",
        "pump": "पंप की वर्तमान स्थिति {pump_status_hi} है।",
        "weather": "मौसम पूर्वानुमान उपलब्ध नहीं है क्योंकि कोई मौसम सेवा कॉन्फ़िगर नहीं है। सिंचाई की योजना से पहले विश्वसनीय स्थानीय पूर्वानुमान देखें।",
        "temperature": "प्रमाणित खेत-सेंसर रीडिंग: {temp}°C और आर्द्रता {humidity}%. यह मौसम पूर्वानुमान नहीं है।",
        "default": "मैं नियम-आधारित कृषि डेमो सहायक हूँ। सामान्य जानकारी के लिए पूछें और फसल-विशिष्ट फैसलों की स्थानीय पुष्टि करें।"
    },
    "mr": {
        "yellow": "पाने पिवळी पडण्याची अनेक कारणे असू शकतात; फक्त मजकुरावरून निदान करता येत नाही. मातीतील ओलावा व निचरा तपासा, पानांच्या दोन्ही बाजू पाहा आणि उपचारापूर्वी स्थानिक कृषी तज्ज्ञांचा सल्ला घ्या.",
        "water": "प्रमाणित शेत-सेन्सरनुसार मातीतील ओलावा {moisture}% आहे. ठरवलेली मर्यादा {min_moisture}% आहे. {irrigation_advice_mr}",
        "fertilizer": "खताची गरज पिकाची अवस्था, माती परीक्षण आणि स्थानिक सल्ल्यावर अवलंबून असते. येथे माती परीक्षण उपलब्ध नाही; या डेमोवरून उत्पादन किंवा मात्रा ठरवू नका.",
        "pump": "पंपाची सध्याची स्थिती {pump_status_mr} आहे.",
        "weather": "हवामानाचा अंदाज उपलब्ध नाही कारण हवामान सेवा जोडलेली नाही. सिंचनाचे नियोजन करण्यापूर्वी विश्वसनीय स्थानिक अंदाज तपासा.",
        "temperature": "प्रमाणित शेत-सेन्सर रीडिंग: {temp}°C आणि आर्द्रता {humidity}%. हा हवामानाचा अंदाज नाही.",
        "default": "मी नियम-आधारित कृषी डेमो सहायक आहे. सर्वसाधारण मार्गदर्शन विचारा आणि पिकाविषयी निर्णय स्थानिक पातळीवर तपासा."
    }
}

@router.post("/chat")
def ask_assistant(query: ChatQuery, _: User = Depends(require_farm_owner)):
    """
    Multilingual AI Chatbot supporting English, Hindi, Marathi with contextual IoT state integration.
    """
    msg = query.message.lower()
    lang = query.language if query.language in ["en", "hi", "mr"] else "en"
    moisture = SYSTEM_STATE["soil_moisture"]
    min_m = SYSTEM_STATE["min_moisture_threshold"]
    pump_on = SYSTEM_STATE["pump_status"]
    temp = SYSTEM_STATE["temperature"]
    humidity = SYSTEM_STATE["humidity"]
    has_live_data = SYSTEM_STATE["data_source"] == "device"

    # Irrigation Context
    if not has_live_data:
        irrig_en = "No verified live sensor reading is available. Check the field before irrigating."
        irrig_hi = "कोई सत्यापित लाइव सेंसर रीडिंग उपलब्ध नहीं है। सिंचाई से पहले खेत की जांच करें।"
        irrig_mr = "सत्यापित थेट सेन्सर रीडिंग उपलब्ध नाही. पाणी देण्यापूर्वी शेत तपासा."
    elif moisture < min_m:
        irrig_en = "The reading is below the configured threshold; verify sensor calibration and field conditions before irrigating."
        irrig_hi = "रीडिंग निर्धारित सीमा से कम है; सिंचाई से पहले सेंसर और खेत की स्थिति जांचें।"
        irrig_mr = "रीडिंग ठरवलेल्या मर्यादेपेक्षा कमी आहे; पाणी देण्यापूर्वी सेन्सर व शेताची स्थिती तपासा."
    else:
        irrig_en = "The reading is not below the configured threshold; verify crop needs and field conditions before deciding."
        irrig_hi = "रीडिंग निर्धारित सीमा से कम नहीं है; फैसला करने से पहले फसल की जरूरत और खेत की स्थिति जांचें।"
        irrig_mr = "रीडिंग ठरवलेल्या मर्यादेपेक्षा कमी नाही; निर्णयापूर्वी पिकाची गरज व शेताची स्थिती तपासा."

    kn = RESPONSES_KNOWLEDGE[lang]

    if "yellow" in msg or "पीली" in msg or "पिवळ" in msg or "leaf" in msg:
        reply = kn["yellow"]
    elif "water" in msg or "irrigate" in msg or "सिंचाई" in msg or "पानी" in msg or "पाणी" in msg:
        if has_live_data:
            reply = kn["water"].format(
                moisture=moisture,
                min_moisture=min_m,
                irrigation_advice=irrig_en,
                irrigation_advice_hi=irrig_hi,
                irrigation_advice_mr=irrig_mr
            )
        else:
            reply = irrig_en if lang == "en" else irrig_hi if lang == "hi" else irrig_mr
    elif "fertilizer" in msg or "fertiliser" in msg or "खाद" in msg or "खत" in msg:
        reply = kn["fertilizer"]
    elif "pump" in msg or "motor" in msg or "पंप" in msg or "मोटर" in msg:
        if not has_live_data:
            reply = (
                "Pump status is unknown until authenticated live device data arrives."
                if lang == "en"
                else "प्रमाणित लाइव डिवाइस डेटा आने तक पंप की स्थिति अज्ञात है।"
                if lang == "hi"
                else "प्रमाणित थेट डिव्हाइस डेटा येईपर्यंत पंपाची स्थिती अज्ञात आहे."
            )
        else:
            reply = kn["pump"].format(
                pump_status="ON" if pump_on else "OFF",
                pump_status_hi="चालू" if pump_on else "बंद",
                pump_status_mr="चालू" if pump_on else "बंद"
            )
    elif "weather" in msg or "rain" in msg or "मौसम" in msg or "हवामान" in msg or "बारिश" in msg or "पाऊस" in msg:
        reply = kn["weather"]
    elif "temp" in msg or "humidity" in msg or "आर्द्रता" in msg or "तापमान" in msg:
        if has_live_data:
            reply = kn["temperature"].format(temp=temp, humidity=humidity)
        else:
            reply = (
                "No verified field-sensor reading is available."
                if lang == "en"
                else "प्रमाणित खेत-सेंसर रीडिंग उपलब्ध नहीं है।"
                if lang == "hi"
                else "प्रमाणित शेत-सेन्सर रीडिंग उपलब्ध नाही."
            )
    else:
        reply = kn["default"]

    return {
        "status": "success",
        "query": query.message,
        "language": lang,
        "reply": reply,
        "audio_supported": False,
        "assistant_mode": "rule_based",
    }
