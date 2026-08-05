# Smart Krishi AI - End-to-End System Architecture

## 1. System Vision & Architecture Diagram

**Smart Krishi AI** is an intelligent, end-to-end mobile and IoT smart farming platform designed to automate crop health monitoring, micro-climate sensing, multilingual AI farming assistance, and precision irrigation management.

```mermaid
graph TD
    subgraph Farmer Mobile & Web Client
        APP["Flutter Mobile App / Web App UI"]
        SCANNER["AI Plant Camera Scanner"]
        BOT["Multilingual Speech & Chat Assistant"]
        DASHBOARD["Live Sensor Dashboard & Pump Toggle"]
    end

    subgraph Cloud Backend (FastAPI Python)
        API["FastAPI REST & Telemetry Server"]
        AUTH_ROUTER["Auth Router (/api/auth)"]
        SENSOR_ROUTER["Sensor Ingestion (/api/sensors)"]
        AI_ROUTER["Vision AI Router (/api/ai)"]
        ASSISTANT_ROUTER["Assistant Router (/api/assistant)"]
        CROP_ROUTER["Crop Manager (/api/crops)"]
        WEATHER_ROUTER["Weather Advisor (/api/weather)"]
        DB[(SQLite / PostgreSQL Database)]
    end

    subgraph Deep Learning Engine
        PYTORCH["PyTorch CNN & Vision Pipeline"]
        KNOWLEDGE["Multilingual Disease Knowledgebase (EN, HI, MR)"]
    end

    subgraph IoT Field Hardware
        ESP32["ESP32 Microcontroller Node"]
        SOIL["Capacitive Soil Moisture v1.2"]
        DHT["DHT22 Temp & Humidity Sensor"]
        RELAY["5V Optocoupler Relay Module"]
        PUMP["12V DC Submersible Water Pump"]
    end

    %% Interactions
    APP -->|REST API Requests| API
    SCANNER -->|Upload Leaf Photo| AI_ROUTER
    BOT -->|Text & Speech Query| ASSISTANT_ROUTER
    DASHBOARD -->|Manual Pump Toggle| SENSOR_ROUTER
    
    API --> DB
    AI_ROUTER --> PYTORCH
    PYTORCH --> KNOWLEDGE

    ESP32 -->|HTTP POST Telemetry (10s)| SENSOR_ROUTER
    SENSOR_ROUTER -->|Return Pump ON/OFF State| ESP32
    ESP32 --> SOIL
    ESP32 --> DHT
    ESP32 -->|Active LOW Trigger| RELAY
    RELAY --> PUMP
```

---

## 2. Component Specifications

### 2.1 Mobile Application (Flutter)
- **Framework**: Flutter 3.x / Dart
- **Screens**:
  1. **Farmer Authentication**: Phone/Password + Preferred Language selection (English, Hindi, Marathi).
  2. **Home Dashboard**: Live soil moisture, temperature, humidity, battery %, pump status, real-time alerts, and AI advice cards.
  3. **Plant Scanner**: Camera/Gallery photo upload, real-time PyTorch Computer Vision diagnosis, confidence rating, organic & chemical remedies.
  4. **AI Assistant**: Conversational agent with Voice STT & Voice TTS output in EN, HI, MR integrated with live sensor context.
  5. **Crop Management**: Crop registration, sowing dates, field size (Acres), growth stage tracker, and fertilizer schedule reminders.
  6. **Weather Module**: 5-day rain forecast and weather-driven automated irrigation postponing logic.

### 2.2 Computer Vision AI Model Pipeline
- **Framework**: PyTorch & Torchvision
- **Architecture**: `PlantHealthCNN` (Custom 4-stage Residual Convolutional Neural Network with BatchNorm & Dropout) + Heuristic Chlorosis/Necrosis Ratio Extractor.
- **Crops Supported**: Tomato, Potato, Rice, Wheat, Cotton, Corn.
- **Diseases Detected**: Early Blight, Late Blight, Leaf Curl Virus, Bacterial Leaf Blight, Blast Disease, Yellow Rust, Bollworm Damage, Fall Armyworm, Nitrogen Deficiency, and Healthy Leaf states.

### 2.3 Cloud Backend (Python FastAPI)
- **Web Server**: FastAPI + Uvicorn
- **Database**: SQLite / PostgreSQL via SQLAlchemy ORM
- **Endpoints**:
  - `POST /api/auth/register` & `POST /api/auth/login`
  - `POST /api/sensors/telemetry`: IoT payload receiver & automatic pump trigger evaluator.
  - `GET /api/sensors/latest`: Live status fetcher for mobile app.
  - `POST /api/sensors/pump/toggle`: Manual pump override.
  - `POST /api/ai/scan-plant`: Leaf image disease classification endpoint.
  - `POST /api/assistant/chat`: Multilingual agronomic assistant endpoint.
  - `GET /api/crops/user/{id}`: Crop profiles & schedules.
  - `GET /api/weather/current`: Weather telematics & rain advice.

### 2.4 IoT & Automatic Irrigation Hardware
- **MCU**: ESP32 DevKit v1
- **Sensors**: Capacitive Soil Moisture Sensor v1.2 (Corrosion resistant), DHT22 (Temp/Humidity), Solar Battery monitor.
- **Actuators**: 5V Optocoupler Relay + 12V Submersible DC Water Pump.
- **Control Rules**:
  - `IF moisture < 40% AND pump == OFF`: Trigger alert & turn ON pump.
  - `IF moisture >= 70% AND pump == ON`: Turn OFF pump.
  - `Safety Watchdog`: Maximum 30-minute continuous run auto-cutoff.
