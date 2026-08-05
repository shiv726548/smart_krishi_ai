from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.database import get_db
from backend.models import SensorData, IrrigationLog, Crop, User

router = APIRouter(prefix="/api/sensors", tags=["IoT Sensors & Irrigation"])

# Global state memory for instant ESP32 polling & threshold control
SYSTEM_STATE = {
    "device_id": "ESP32_KRISHI_01",
    "soil_moisture": 32.5,  # start low for demo/triggering
    "temperature": 28.4,
    "humidity": 65.0,
    "nitrogen": 48.0,
    "phosphorus": 26.0,
    "potassium": 58.0,
    "pump_status": False,
    "pump_turned_on_at": None,
    "battery_level": 94.0,
    "min_moisture_threshold": 40.0,
    "max_moisture_threshold": 70.0,
    "max_pump_duration_minutes": 30, # Safety limit
    "manual_override": False,
    "alerts": []
}

class TelemetryPayload(BaseModel):
    device_id: str = "ESP32_KRISHI_01"
    soil_moisture: float
    temperature: float
    humidity: float
    nitrogen: Optional[float] = 45.0
    phosphorus: Optional[float] = 25.0
    potassium: Optional[float] = 60.0
    battery_level: Optional[float] = 95.0

class PumpControlPayload(BaseModel):
    device_id: str = "ESP32_KRISHI_01"
    action: str  # "ON" or "OFF"
    reason: Optional[str] = "Manual farmer override via Mobile App"

class ThresholdConfigPayload(BaseModel):
    min_moisture_threshold: float
    max_moisture_threshold: float

@router.post("/telemetry")
def receive_telemetry(payload: TelemetryPayload, db: Session = Depends(get_db)):
    """
    ESP32 posts telemetry every 10 seconds.
    Evaluates Automatic Irrigation Logic & Safety Watchdog.
    """
    global SYSTEM_STATE

    SYSTEM_STATE["soil_moisture"] = payload.soil_moisture
    SYSTEM_STATE["temperature"] = payload.temperature
    SYSTEM_STATE["humidity"] = payload.humidity
    SYSTEM_STATE["nitrogen"] = payload.nitrogen or SYSTEM_STATE["nitrogen"]
    SYSTEM_STATE["phosphorus"] = payload.phosphorus or SYSTEM_STATE["phosphorus"]
    SYSTEM_STATE["potassium"] = payload.potassium or SYSTEM_STATE["potassium"]
    SYSTEM_STATE["battery_level"] = payload.battery_level or SYSTEM_STATE["battery_level"]

    alerts = []
    
    # Low battery alert
    if SYSTEM_STATE["battery_level"] < 20.0:
        alerts.append("Warning: Sensor battery is below 20%. Please check solar charger.")

    # 1. Automatic Irrigation Rule Evaluation (if manual override is not blocking)
    current_moisture = payload.soil_moisture
    min_thresh = SYSTEM_STATE["min_moisture_threshold"]
    max_thresh = SYSTEM_STATE["max_moisture_threshold"]

    # Check safety timeout if pump is running
    if SYSTEM_STATE["pump_status"] and SYSTEM_STATE["pump_turned_on_at"]:
        elapsed = datetime.utcnow() - SYSTEM_STATE["pump_turned_on_at"]
        if elapsed > timedelta(minutes=SYSTEM_STATE["max_pump_duration_minutes"]):
            SYSTEM_STATE["pump_status"] = False
            SYSTEM_STATE["pump_turned_on_at"] = None
            SYSTEM_STATE["manual_override"] = False
            alerts.append("SAFETY TIMEOUT TRIGGERED: Water pump auto-stopped after 30 mins runtime.")
            
            # Log safety shutdown
            log = IrrigationLog(
                device_id=payload.device_id,
                trigger_type="SAFETY_TIMEOUT",
                action="TURN_OFF",
                soil_moisture_at_trigger=current_moisture,
                duration_seconds=1800
            )
            db.add(log)

    # Automatic On/Off logic
    if not SYSTEM_STATE["manual_override"]:
        if current_moisture < min_thresh and not SYSTEM_STATE["pump_status"]:
            SYSTEM_STATE["pump_status"] = True
            SYSTEM_STATE["pump_turned_on_at"] = datetime.utcnow()
            alert_msg = f"Soil moisture low ({current_moisture}% < {min_thresh}%). Automatic Irrigation Started."
            alerts.append(alert_msg)

            log = IrrigationLog(
                device_id=payload.device_id,
                trigger_type="AUTO_MOISTURE_LOW",
                action="TURN_ON",
                soil_moisture_at_trigger=current_moisture
            )
            db.add(log)

        elif current_moisture >= max_thresh and SYSTEM_STATE["pump_status"]:
            SYSTEM_STATE["pump_status"] = False
            duration = 0
            if SYSTEM_STATE["pump_turned_on_at"]:
                duration = int((datetime.utcnow() - SYSTEM_STATE["pump_turned_on_at"]).total_seconds())
            SYSTEM_STATE["pump_turned_on_at"] = None
            alert_msg = f"Soil moisture reached target level ({current_moisture}% >= {max_thresh}%). Irrigation Stopped."
            alerts.append(alert_msg)

            log = IrrigationLog(
                device_id=payload.device_id,
                trigger_type="AUTO_MOISTURE_OPTIMAL",
                action="TURN_OFF",
                soil_moisture_at_trigger=current_moisture,
                duration_seconds=duration
            )
            db.add(log)

    SYSTEM_STATE["alerts"] = alerts

    # Save telemetry record to database
    db_entry = SensorData(
        device_id=payload.device_id,
        soil_moisture=payload.soil_moisture,
        temperature=payload.temperature,
        humidity=payload.humidity,
        nitrogen=payload.nitrogen,
        phosphorus=payload.phosphorus,
        potassium=payload.potassium,
        pump_status=SYSTEM_STATE["pump_status"],
        battery_level=payload.battery_level
    )
    db.add(db_entry)
    db.commit()

    return {
        "status": "success",
        "pump_status": SYSTEM_STATE["pump_status"],
        "alerts": alerts
    }

@router.get("/latest")
def get_latest_sensor_data():
    """
    Endpoint for Mobile App & Web Dashboard to fetch real-time metrics & pump state.
    """
    return {
        "status": "success",
        "data": SYSTEM_STATE,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/pump/toggle")
def toggle_pump(payload: PumpControlPayload, db: Session = Depends(get_db)):
    """
    Manual pump control override from Farmer Mobile App.
    """
    global SYSTEM_STATE
    desired_on = (payload.action.upper() == "ON")
    
    SYSTEM_STATE["pump_status"] = desired_on
    SYSTEM_STATE["manual_override"] = True
    
    if desired_on:
        SYSTEM_STATE["pump_turned_on_at"] = datetime.utcnow()
    else:
        SYSTEM_STATE["pump_turned_on_at"] = None
        SYSTEM_STATE["manual_override"] = False # Reset override when turned off manually

    log = IrrigationLog(
        device_id=payload.device_id,
        trigger_type="MANUAL_FARMER_APP",
        action="TURN_ON" if desired_on else "TURN_OFF",
        soil_moisture_at_trigger=SYSTEM_STATE["soil_moisture"]
    )
    db.add(log)
    db.commit()

    return {
        "status": "success",
        "message": f"Water pump manually turned {'ON' if desired_on else 'OFF'}",
        "pump_status": SYSTEM_STATE["pump_status"],
        "manual_override": SYSTEM_STATE["manual_override"]
    }

@router.post("/thresholds")
def set_thresholds(payload: ThresholdConfigPayload):
    """
    Set custom soil moisture thresholds for automatic irrigation.
    """
    global SYSTEM_STATE
    SYSTEM_STATE["min_moisture_threshold"] = payload.min_moisture_threshold
    SYSTEM_STATE["max_moisture_threshold"] = payload.max_moisture_threshold
    return {
        "status": "success",
        "message": f"Soil moisture thresholds updated: Min={payload.min_moisture_threshold}%, Max={payload.max_moisture_threshold}%",
        "thresholds": {
            "min": payload.min_moisture_threshold,
            "max": payload.max_moisture_threshold
        }
    }
