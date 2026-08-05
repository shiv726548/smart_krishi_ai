# Smart Krishi AI - Testing Guide & Farmer User Manual

---

## PART I: FARMER USER MANUAL (किसान उपयोग विवरण)

### 1. English Instructions

#### Step 1: Getting Started & Login
1. Open the **Smart Krishi AI** app on your phone.
2. Select your preferred language: **English**, **हिंदी (Hindi)**, or **मराठी (Marathi)**.
3. Enter your mobile number and password to log in.

#### Step 2: Monitoring Field Health (Home Dashboard)
- **Soil Moisture**: Shows how wet your field soil is in real time.
  - Below 40%: Soil is dry. The automatic pump will start.
  - 40% - 70%: Optimal soil moisture.
  - Above 70%: Soil is sufficiently watered. Pump will stop.
- **Water Pump Controller**: You can tap the **START** or **STOP** button to manually control your water pump at any time.

#### Step 3: Scanning Plant Leaves for Diseases (Plant Scanner)
1. Tap on the **Scan AI** tab at the bottom.
2. Select your crop (e.g., Tomato, Potato, Rice, Wheat, Cotton, Corn).
3. Click **Take Photo** or upload a leaf picture from your gallery.
4. The AI will detect if your plant is healthy or infected, show the confidence score, and give step-by-step chemical and organic remedies!

#### Step 4: Asking the AI Farming Assistant
1. Tap the **Assistant** tab.
2. Type or tap the **Microphone** icon to speak your question in English, Hindi, or Marathi (e.g., *"Why are my tomato leaves turning yellow?"* or *"क्या मुझे आज पानी देना चाहिए?"*).
3. The AI assistant will analyze your live soil moisture and give personalized voice and text advice!

---

### 2. हिंदी निर्देश (Farmer Instructions in Hindi)

#### चरण 1: शुरुआत और लॉगिन
1. अपने मोबाइल पर **Smart Krishi AI** ऐप खोलें।
2. अपनी पसंदीदा भाषा चुनें: **हिंदी**, **मराठी** या **English**।
3. अपना मोबाइल नंबर दर्ज करके लॉगिन करें।

#### चरण 2: खेत की नमी और पंप का नियंत्रण (होम डैशबोर्ड)
- **मिट्टी की नमी (Soil Moisture)**: यह रियल-टाइम में आपकी खेत की नमी दिखाता है।
  - 40% से कम: खेत सूखा है। ऑटोमैटिक पंप चालू हो जाएगा।
  - 40% - 70%: आदर्श नमी स्तर।
  - 70% से अधिक: पर्याप्त पानी है। पंप बंद हो जाएगा।
- **वाटर पंप बटन**: आप किसी भी समय **START** या **STOP** बटन दबाकर अपने पंप को मोबाइल से चालू/बंद कर सकते हैं।

#### चरण 3: पौधों के पत्तों की जांच (AI प्लांट स्कैनर)
1. नीचे **Scan AI** टैब पर क्लिक करें।
2. अपनी फसल चुनें (जैसे टमाटर, आलू, धान, गेहूं, कपास, मक्का)।
3. अपने कैमरे से पत्ते की फोटो खींचें या गैलरी से अपलोड करें।
4. AI मॉडल तुरंत बीमारी पहचानेगा, और आपको जैविक (Organic) और रासायनिक (Chemical) उपचार बताएगा!

#### चरण 4: AI कृषि सहायक से प्रश्न पूछें
1. **Assistant** टैब खोलें।
2. माइक बटन दबाकर बोलें (जैसे: *"मेरे टमाटर के पत्ते पीले क्यों हो रहे हैं?"* या *"आज पानी देना चाहिए या नहीं?"*)।
3. AI सहायक खेत की नमी देखकर आपको सही सलाह देगा।

---

## PART II: SYSTEM TESTING & VERIFICATION GUIDE

### 1. Running Unit Tests
To run the automated PyTest test suite for backend APIs, IoT ingestion, and PyTorch AI vision pipeline:

```bash
cd /home/pc-no18/Downloads/smart_krishi_ai
PYTHONPATH=. pytest tests/test_api.py tests/test_ai_pipeline.py
```

### 2. Testing FastAPI Backend Server
Start the backend server locally:

```bash
python3 backend/main.py
```
- Open Swagger API documentation at: `http://localhost:8000/docs`
- Open Web App Dashboard & Mobile Simulator at: `http://localhost:8000/app`

### 3. ESP32 Hardware & Circuit Testing
1. Wire components according to `iot_firmware/CIRCUIT_SCHEMATIC.md`.
2. Flash `iot_firmware/smart_krishi_esp32.ino` using Arduino IDE.
3. Open Serial Monitor at `115200 baud`.
4. Dip soil moisture sensor in dry soil (<40%) -> Verify LED/Relay turns ON and log appears in FastAPI terminal!
5. Dip sensor in water (>70%) -> Verify Relay turns OFF automatically!
