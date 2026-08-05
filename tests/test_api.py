import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["app"] == "Smart Krishi AI System API"

def test_sensor_telemetry_and_auto_irrigation():
    payload = {
        "device_id": "ESP32_KRISHI_TEST",
        "soil_moisture": 32.0, # Below 40 threshold
        "temperature": 29.5,
        "humidity": 60.0
    }
    response = client.post("/api/sensors/telemetry", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["pump_status"] == True # Auto turned ON because moisture < 40%

def test_manual_pump_toggle():
    payload = {
        "device_id": "ESP32_KRISHI_TEST",
        "action": "OFF"
    }
    response = client.post("/api/sensors/pump/toggle", json=payload)
    assert response.status_code == 200
    assert response.json()["pump_status"] == False

def test_ai_assistant_chat():
    payload = {
        "message": "Why are my tomato leaves turning yellow?",
        "language": "en",
        "crop_name": "Tomato"
    }
    response = client.post("/api/assistant/chat", json=payload)
    assert response.status_code == 200
    assert "yellow" in response.json()["reply"].lower() or "nitrogen" in response.json()["reply"].lower()

def test_weather_forecast():
    response = client.get("/api/weather/current")
    assert response.status_code == 200
    assert "forecast" in response.json()
