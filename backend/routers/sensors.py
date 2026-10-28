import os
from datetime import datetime, timedelta, timezone
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import IrrigationLog, SensorData, User
from backend.security import require_device_token, require_farm_owner

router = APIRouter(prefix="/api/sensors", tags=["IoT Sensors & Irrigation"])


def pump_control_is_enabled() -> bool:
    return os.getenv("PUMP_CONTROL_ENABLED", "false").strip().lower() in {
        "1", "true", "yes", "on"
    }


SYSTEM_STATE = {
    "device_id": "ESP32_KRISHI_01",
    "soil_moisture": None,
    "temperature": None,
    "humidity": None,
    "nitrogen": None,
    "phosphorus": None,
    "potassium": None,
    "pump_status": False,
    "pump_turned_on_at": None,
    "battery_level": None,
    "min_moisture_threshold": 40.0,
    "max_moisture_threshold": 70.0,
    "max_pump_duration_minutes": 30,
    "manual_override": False,
    "pump_enabled": False,
    "data_source": "unavailable",
    "last_reading_at": None,
    "alerts": ["No authenticated sensor reading has been received."],
}


class TelemetryPayload(BaseModel):
    device_id: str = Field(default="ESP32_KRISHI_01", min_length=1, max_length=80)
    soil_moisture: float = Field(ge=0, le=100)
    temperature: float = Field(ge=-40, le=85)
    humidity: float = Field(ge=0, le=100)
    nitrogen: float | None = Field(default=None, ge=0, le=10000)
    phosphorus: float | None = Field(default=None, ge=0, le=10000)
    potassium: float | None = Field(default=None, ge=0, le=10000)
    battery_level: float | None = Field(default=None, ge=0, le=100)


class PumpControlPayload(BaseModel):
    device_id: str = Field(default="ESP32_KRISHI_01", min_length=1, max_length=80)
    action: Literal["ON", "OFF"]
    reason: str = Field(default="Manual farmer override", max_length=200)


class ThresholdConfigPayload(BaseModel):
    min_moisture_threshold: float = Field(ge=0, le=100)
    max_moisture_threshold: float = Field(ge=0, le=100)


@router.post("/telemetry")
def receive_telemetry(
    payload: TelemetryPayload,
    db: Session = Depends(get_db),
    _: None = Depends(require_device_token),
):
    """Accept telemetry only from a device configured with a shared secret."""
    now = datetime.now(timezone.utc)
    SYSTEM_STATE.update(
        {
            "device_id": payload.device_id,
            "soil_moisture": payload.soil_moisture,
            "temperature": payload.temperature,
            "humidity": payload.humidity,
            "battery_level": payload.battery_level,
            "data_source": "device",
            "last_reading_at": now,
            "pump_enabled": pump_control_is_enabled(),
        }
    )
    for key in ("nitrogen", "phosphorus", "potassium"):
        value = getattr(payload, key)
        if value is not None:
            SYSTEM_STATE[key] = value

    alerts = []
    if payload.battery_level is not None and payload.battery_level < 20:
        alerts.append("Sensor battery is below 20%; check its power supply.")

    pump_enabled = pump_control_is_enabled()
    if not pump_enabled:
        # Fail closed: never return an ON command to the hardware by default.
        SYSTEM_STATE["pump_status"] = False
        SYSTEM_STATE["pump_turned_on_at"] = None
        SYSTEM_STATE["manual_override"] = False
    else:
        current_moisture = payload.soil_moisture
        min_threshold = SYSTEM_STATE["min_moisture_threshold"]
        max_threshold = SYSTEM_STATE["max_moisture_threshold"]

        if SYSTEM_STATE["pump_status"] and SYSTEM_STATE["pump_turned_on_at"]:
            elapsed = now - SYSTEM_STATE["pump_turned_on_at"]
            if elapsed > timedelta(minutes=SYSTEM_STATE["max_pump_duration_minutes"]):
                SYSTEM_STATE["pump_status"] = False
                SYSTEM_STATE["pump_turned_on_at"] = None
                SYSTEM_STATE["manual_override"] = False
                alerts.append("Safety timeout: pump command stopped after 30 minutes.")
                db.add(
                    IrrigationLog(
                        device_id=payload.device_id,
                        trigger_type="SAFETY_TIMEOUT",
                        action="TURN_OFF",
                        soil_moisture_at_trigger=current_moisture,
                        duration_seconds=1800,
                    )
                )

        if not SYSTEM_STATE["manual_override"]:
            if current_moisture < min_threshold and not SYSTEM_STATE["pump_status"]:
                SYSTEM_STATE["pump_status"] = True
                SYSTEM_STATE["pump_turned_on_at"] = now
                alerts.append(
                    f"Soil moisture is below the configured threshold ({min_threshold}%)."
                )
                db.add(
                    IrrigationLog(
                        device_id=payload.device_id,
                        trigger_type="AUTO_MOISTURE_LOW",
                        action="TURN_ON",
                        soil_moisture_at_trigger=current_moisture,
                    )
                )
            elif current_moisture >= max_threshold and SYSTEM_STATE["pump_status"]:
                started_at = SYSTEM_STATE["pump_turned_on_at"]
                duration = int((now - started_at).total_seconds()) if started_at else 0
                SYSTEM_STATE["pump_status"] = False
                SYSTEM_STATE["pump_turned_on_at"] = None
                alerts.append(
                    f"Soil moisture reached the configured upper threshold ({max_threshold}%)."
                )
                db.add(
                    IrrigationLog(
                        device_id=payload.device_id,
                        trigger_type="AUTO_MOISTURE_OPTIMAL",
                        action="TURN_OFF",
                        soil_moisture_at_trigger=current_moisture,
                        duration_seconds=duration,
                    )
                )

    SYSTEM_STATE["alerts"] = alerts
    db.add(
        SensorData(
            device_id=payload.device_id,
            soil_moisture=payload.soil_moisture,
            temperature=payload.temperature,
            humidity=payload.humidity,
            nitrogen=payload.nitrogen,
            phosphorus=payload.phosphorus,
            potassium=payload.potassium,
            pump_status=SYSTEM_STATE["pump_status"],
            battery_level=payload.battery_level,
            timestamp=now,
        )
    )
    db.commit()
    return {
        "status": "success",
        "data_source": "device",
        "pump_status": SYSTEM_STATE["pump_status"],
        "pump_enabled": pump_enabled,
        "alerts": alerts,
    }


@router.get("/latest")
def get_latest_sensor_data(_: User = Depends(require_farm_owner)):
    return {
        "status": "success" if SYSTEM_STATE["data_source"] == "device" else "unavailable",
        "data": SYSTEM_STATE,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.post("/pump/toggle")
def toggle_pump(
    payload: PumpControlPayload,
    db: Session = Depends(get_db),
    _: User = Depends(require_farm_owner),
):
    if not pump_control_is_enabled():
        raise HTTPException(
            status_code=503,
            detail="Pump control is disabled. Configure and verify the hardware before enabling it.",
        )
    if SYSTEM_STATE["data_source"] != "device":
        raise HTTPException(
            status_code=503,
            detail="Pump control requires a recent authenticated device reading",
        )

    desired_on = payload.action == "ON"
    now = datetime.now(timezone.utc)
    SYSTEM_STATE["pump_status"] = desired_on
    SYSTEM_STATE["manual_override"] = desired_on
    SYSTEM_STATE["pump_turned_on_at"] = now if desired_on else None
    db.add(
        IrrigationLog(
            device_id=payload.device_id,
            trigger_type="MANUAL_FARMER_APP",
            action="TURN_ON" if desired_on else "TURN_OFF",
            soil_moisture_at_trigger=SYSTEM_STATE["soil_moisture"] or 0.0,
        )
    )
    db.commit()
    return {
        "status": "success",
        "pump_status": SYSTEM_STATE["pump_status"],
        "manual_override": SYSTEM_STATE["manual_override"],
    }


@router.post("/thresholds")
def set_thresholds(
    payload: ThresholdConfigPayload,
    _: User = Depends(require_farm_owner),
):
    if payload.min_moisture_threshold >= payload.max_moisture_threshold:
        raise HTTPException(
            status_code=422,
            detail="Minimum moisture threshold must be lower than the maximum",
        )
    SYSTEM_STATE["min_moisture_threshold"] = payload.min_moisture_threshold
    SYSTEM_STATE["max_moisture_threshold"] = payload.max_moisture_threshold
    return {
        "status": "success",
        "thresholds": {
            "min": payload.min_moisture_threshold,
            "max": payload.max_moisture_threshold,
        },
    }
