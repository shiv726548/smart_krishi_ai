from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.routers.sensors import SYSTEM_STATE

router = APIRouter(prefix="/api/assistant", tags=["AI Farming Assistant"])

class ChatQuery(BaseModel):
    message: str
    language: str = "en" # en, hi, mr
    crop_name: Optional[str] = "Tomato"

# Smart Knowledge Graph responses for agronomy & IoT telemetry
RESPONSES_KNOWLEDGE = {
    "en": {
        "yellow": "Leaves usually turn yellow due to Nitrogen deficiency, overwatering, or fungal infections like Early Blight. Check if soil moisture is above 80% or apply 1% Urea solution as foliar spray.",
        "water": "Based on live IoT sensors, current soil moisture is {moisture}%. Minimum required is {min_moisture}%. {irrigation_advice}",
        "fertilizer": "For {crop}, apply NPK 19:19:19 during early growth, and NPK 0:52:34 or Potash during flowering to boost yield and disease resistance.",
        "pump": "Current pump status is {pump_status}. You can control it manually from the app home screen.",
        "weather": "Current temperature is {temp}°C and humidity is {humidity}%. Keep an eye on rain forecast before irrigating.",
        "default": "I am your Smart Krishi AI Farming Assistant! You can ask me about leaf yellowing, crop irrigation, fertilizer recommendations, pest control, or current field moisture."
    },
    "hi": {
        "yellow": "पत्तियां आमतौर पर नाइट्रोजन की कमी, अधिक सिंचाई या अगेती झुलसा (Early Blight) जैसी बीमारी के कारण पीली पड़ती हैं। यूरिया 1% या वर्मीकंपोस्ट डालें।",
        "water": "लाइव आईओटी सेंसर के अनुसार, आपकी मिट्टी में नमी {moisture}% है। {irrigation_advice_hi}",
        "fertilizer": "{crop} के लिए शुरुआती विकास में NPK 19:19:19 और फूल आने पर Potash या NPK 0:52:34 का प्रयोग करें।",
        "pump": "वर्तमान में पंप {pump_status_hi} है। आप मोबाइल ऐप से इसे चालू या बंद कर सकते हैं।",
        "weather": "वर्तमान तापमान {temp}°C और आर्द्रता {humidity}% है।",
        "default": "नमस्ते! मैं आपका स्मार्ट कृषि AI सहायक हूँ। आप मुझसे फसल स्वास्थ्य, सिंचाई, खाद और बीमारियों के बारे में पूछ सकते हैं।"
    },
    "mr": {
        "yellow": "पाने सामान्यतः नत्राची (Nitrogen) कमतरता, जास्त पाणी किंवा करपा रोगामुळे पिवळी पडतात. १% युरिया फवारणी करा किंवा गांडूळ खत द्या.",
        "water": "सध्या मातीतील ओलावा {moisture}% आहे. {irrigation_advice_mr}",
        "fertilizer": "{crop} पिकासाठी सुरुवातीला NPK १९:१९:१९ आणि फुलधारणेच्या वेळी पोटॅश किंवा ०:५२:३४ द्या.",
        "pump": "सध्या पाण्याचा पंप {pump_status_mr} आहे.",
        "weather": "सध्याचे तापमान {temp}°C आणि हवामानातील आद्रता {humidity}% आहे.",
        "default": "नमस्कार! मी तुमचा स्मार्ट कृषी AI सहाय्यक आहे. मला शेती, पाणी व्यवस्थापन आणि रोगांबद्दल प्रश्न विचारा."
    }
}

@router.post("/chat")
def ask_assistant(query: ChatQuery):
    """
    Multilingual AI Chatbot supporting English, Hindi, Marathi with contextual IoT state integration.
    """
    msg = query.message.lower()
    lang = query.language if query.language in ["en", "hi", "mr"] else "en"
    crop = query.crop_name or "Tomato"

    moisture = SYSTEM_STATE["soil_moisture"]
    min_m = SYSTEM_STATE["min_moisture_threshold"]
    pump_on = SYSTEM_STATE["pump_status"]
    temp = SYSTEM_STATE["temperature"]
    humidity = SYSTEM_STATE["humidity"]

    # Irrigation Context
    if moisture < min_m:
        irrig_en = "Moisture is low! Irrigation is recommended today."
        irrig_hi = "नमी कम है! आज सिंचाई की आवश्यकता है।"
        irrig_mr = "ओलावा कमी आहे! आज पिकाला पाणी देणे आवश्यक आहे."
    else:
        irrig_en = "Moisture level is optimal. No extra watering required right now."
        irrig_hi = "नमी पर्याप्त है। अभी अतिरिक्त सिंचाई की आवश्यकता नहीं है।"
        irrig_mr = "मातीत पुरेसा ओलावा आहे. सध्या अतिरिक्त पाण्याची गरज नाही."

    kn = RESPONSES_KNOWLEDGE[lang]

    if "yellow" in msg or "पीली" in msg or "पिवळ" in msg or "leaf" in msg:
        reply = kn["yellow"]
    elif "water" in msg or "irrigate" in msg or "सिंचाई" in msg or "पानी" in msg or "पाणी" in msg:
        reply = kn["water"].format(
            moisture=moisture,
            min_moisture=min_m,
            irrigation_advice=irrig_en,
            irrigation_advice_hi=irrig_hi,
            irrigation_advice_mr=irrig_mr
        )
    elif "fertilizer" in msg or "fertiliser" in msg or "खाद" in msg or "खत" in msg:
        reply = kn["fertilizer"].format(crop=crop)
    elif "pump" in msg or "motor" in msg or "पंप" in msg or "मोटर" in msg:
        reply = kn["pump"].format(
            pump_status="ON (Running)" if pump_on else "OFF",
            pump_status_hi="चालू (ON)" if pump_on else "बंद (OFF)",
            pump_status_mr="चालू आहे" if pump_on else "बंद आहे"
        )
    elif "weather" in msg or "temp" in msg or "मौसम" in msg or "हवामान" in msg:
        reply = kn["weather"].format(temp=temp, humidity=humidity)
    else:
        reply = kn["default"]

    return {
        "status": "success",
        "query": query.message,
        "language": lang,
        "reply": reply,
        "audio_supported": True
    }
