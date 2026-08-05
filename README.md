# 🌾 Smart Krishi AI (स्मार्ट कृषि AI)
> **AI-Powered Mobile & IoT Smart Agriculture System for Crop Health Monitoring & Automated Irrigation**

---

## 📌 Project Overview
**Smart Krishi AI** is a complete, production-ready smart farming system that combines Mobile Applications, Deep Learning Computer Vision, Multilingual Conversational AI, and ESP32 IoT hardware sensors to empower farmers.

### 🌟 Key Deliverables Included
1. **Farmer Mobile Application (Flutter)**: Full Flutter mobile app codebase with Auth, Home Dashboard, AI Scanner, Multilingual Voice Assistant, Crop Schedule Manager, and Weather Module.
2. **Interactive Web Application & Mobile Simulator**: Beautiful glassmorphic Web UI with live metric controls and mobile simulator.
3. **AI Plant Health Engine (PyTorch)**: Computer vision pipeline detecting diseases and nutrient deficiencies across 6 primary crops (*Tomato, Potato, Rice, Wheat, Cotton, Corn*).
4. **IoT Soil & Environmental Monitoring (ESP32)**: Hardware firmware for telemetry collection (*Soil Moisture, Temperature, Humidity, Battery level*).
5. **Automatic Irrigation Controller**: Active LOW Relay controller with moisture threshold rules and 30-minute safety watchdog.
6. **Cloud Backend API (Python FastAPI)**: Robust REST API with SQLite/PostgreSQL database models and real-time state management.
7. **Circuit Schematic & Wokwi Simulation**: Detailed wiring tables and Mermaid circuit diagrams.
8. **Testing & Documentation**: PyTest automated suite, system architecture, and farmer user manual in English & Hindi.

---

## 📂 Project Repository Structure

```
smart_krishi_ai/
├── README.md                           # Master README & Cloud Deployment Guide
├── ARCHITECTURE.md                     # System Architecture & Component Specifications
├── TESTING_AND_USER_MANUAL.md          # Comprehensive Testing & Farmer User Manual
│
├── mobile_app/                         # Flutter Mobile Application
│   ├── pubspec.yaml                    # Flutter dependencies
│   └── lib/
│       ├── main.dart                   # Entrypoint & navigation
│       ├── models/                     # Sensor, Crop, and AI result models
│       ├── services/                   # HTTP API services
│       └── screens/                    # Flutter UI Screens (Dashboard, Scanner, Assistant, etc.)
│
├── web_app/                            # Live Interactive Web & Mobile Simulator App
│   ├── index.html                      # Glassmorphic Web UI
│   ├── app.js                          # JavaScript client & Web Speech API integration
│   └── styles.css                      # Styling rules
│
├── backend/                            # FastAPI Python Backend & Deep Learning
│   ├── main.py                         # FastAPI server entrypoint
│   ├── database.py                     # Database connection
│   ├── models.py                       # SQLAlchemy ORM models
│   ├── routers/                        # API Routers (auth, sensors, ai, assistant, crops, weather)
│   └── ai_engine/                      # PyTorch CNN model pipeline & disease knowledgebase
│
├── iot_firmware/                       # ESP32 IoT Node Firmware & Hardware
│   ├── smart_krishi_esp32.ino          # Arduino/C++ firmware
│   ├── config.h                        # WiFi & pin config header
│   └── CIRCUIT_SCHEMATIC.md            # Hardware wiring & pinout diagrams
│
└── tests/                              # Automated PyTest Test Suite
    ├── test_api.py
    └── test_ai_pipeline.py
```

---

## ⚡ Quick Start Guide

### 1. Launch FastAPI Backend & Web App
```bash
cd /home/pc-no18/Downloads/smart_krishi_ai
python3 backend/main.py
```
- **REST API Docs**: `http://localhost:8000/docs`
- **Web App & Mobile Simulator**: `http://localhost:8000/app`

### 2. Run Automated PyTest Suite
```bash
PYTHONPATH=. pytest tests/test_api.py tests/test_ai_pipeline.py
```

### 3. ESP32 Firmware Setup
1. Open `iot_firmware/smart_krishi_esp32.ino` in Arduino IDE.
2. Edit `iot_firmware/config.h` to set your WiFi credentials and backend server IP.
3. Flash to ESP32 DevKit v1.

---

## 🚀 Cloud Deployment (Docker)

To deploy the backend server to cloud platforms (AWS, GCP, DigitalOcean):

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir fastapi uvicorn torch torchvision pillow pydantic sqlalchemy python-multipart
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📄 License
Released under the MIT License. Developed for Smart Agriculture & IoT Technology Advancement.
