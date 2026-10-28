import io
import hashlib

import pytest
from fastapi.testclient import TestClient
from PIL import Image
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from backend.database import Base, get_db
from backend.main import app
from backend.models import AIDiagnosis, User
from backend.routers.sensors import SYSTEM_STATE


@pytest.fixture()
def client(tmp_path, monkeypatch):
    test_engine = create_engine(
        f"sqlite:///{tmp_path / 'test.sqlite3'}",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    test_session = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = test_session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    monkeypatch.delenv("FARM_OWNER_USER_ID", raising=False)
    monkeypatch.delenv("IOT_DEVICE_TOKEN", raising=False)
    monkeypatch.setenv("PUMP_CONTROL_ENABLED", "false")
    SYSTEM_STATE.update(
        {
            "soil_moisture": None,
            "temperature": None,
            "humidity": None,
            "pump_status": False,
            "pump_turned_on_at": None,
            "data_source": "unavailable",
            "pump_enabled": False,
            "last_reading_at": None,
            "alerts": ["No authenticated sensor reading has been received."],
            "manual_override": False,
        }
    )
    with TestClient(app) as test_client:
        yield test_client, test_engine
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


def register(client, phone_number):
    response = client.post(
        "/api/auth/register",
        json={
            "full_name": "Test Farmer",
            "phone_number": phone_number,
            "password": "test-password-123",
            "preferred_language": "en",
        },
    )
    assert response.status_code == 200, response.text
    return response.json()


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_root_and_weather_report_real_availability(client):
    test_client, _ = client
    assert test_client.get("/").status_code == 200

    weather = test_client.get("/api/weather/current")
    assert weather.status_code == 200
    assert weather.json()["status"] == "unavailable"
    assert weather.json()["current"] is None
    assert weather.json()["forecast"] == []


def test_request_size_limit_rejects_oversized_body(client):
    test_client, _ = client
    response = test_client.post(
        "/api/auth/login",
        content=b"{}",
        headers={"Content-Length": str(6 * 1024 * 1024 + 1)},
    )
    assert response.status_code == 413


def test_auth_hashes_passwords_and_issues_signed_access_tokens(client):
    test_client, engine = client
    registration = register(test_client, "+919000000001")
    assert registration["token_type"] == "bearer"
    assert registration["token"].count(".") == 2
    with Session(engine) as db:
        user = db.query(User).filter_by(phone_number="+919000000001").one()
        assert user.hashed_password.startswith("scrypt$")

    login = test_client.post(
        "/api/auth/login",
        json={"phone_number": "+919000000001", "password": "test-password-123"},
    )
    assert login.status_code == 200
    assert login.json()["token"] != f"mock-jwt-token-user-{registration['user_id']}"

    invalid_login = test_client.post(
        "/api/auth/login",
        json={"phone_number": "+919000000001", "password": "wrong-password"},
    )
    assert invalid_login.status_code == 401


def test_legacy_sha256_password_is_upgraded_after_login(client):
    test_client, engine = client
    legacy_digest = hashlib.sha256(b"legacy-password-123").hexdigest()
    with Session(engine) as db:
        db.add(
            User(
                full_name="Legacy Test",
                phone_number="+919000000009",
                hashed_password=legacy_digest,
            )
        )
        db.commit()

    response = test_client.post(
        "/api/auth/login",
        json={
            "phone_number": "+919000000009",
            "password": "legacy-password-123",
        },
    )
    assert response.status_code == 200
    with Session(engine) as db:
        upgraded = db.query(User).filter_by(phone_number="+919000000009").one()
        assert upgraded.hashed_password.startswith("scrypt$")


def test_private_crops_require_auth_and_enforce_ownership(client):
    test_client, _ = client
    farmer_a = register(test_client, "+919000000002")
    farmer_b = register(test_client, "+919000000003")

    assert test_client.get(f"/api/crops/user/{farmer_a['user_id']}").status_code == 401
    created = test_client.post(
        "/api/crops/add",
        headers=auth_headers(farmer_a["token"]),
        json={"crop_name": "Tomato", "sowing_date": "2026-10-01"},
    )
    assert created.status_code == 200
    own_crops = test_client.get(
        f"/api/crops/user/{farmer_a['user_id']}",
        headers=auth_headers(farmer_a["token"]),
    )
    assert own_crops.status_code == 200
    assert own_crops.json()["count"] == 1

    other_crops = test_client.get(
        f"/api/crops/user/{farmer_a['user_id']}",
        headers=auth_headers(farmer_b["token"]),
    )
    assert other_crops.status_code == 403


def test_telemetry_requires_device_secret_and_cannot_start_pump_by_default(
    client, monkeypatch
):
    test_client, _ = client
    farmer = register(test_client, "+919000000004")
    monkeypatch.setenv("FARM_OWNER_USER_ID", str(farmer["user_id"]))
    payload = {
        "device_id": "ESP32_TEST",
        "soil_moisture": 10,
        "temperature": 24,
        "humidity": 50,
    }

    assert test_client.post("/api/sensors/telemetry", json=payload).status_code == 503
    monkeypatch.setenv("IOT_DEVICE_TOKEN", "test-only-device-token")
    denied = test_client.post(
        "/api/sensors/telemetry",
        json=payload,
        headers={"X-Device-Token": "wrong"},
    )
    assert denied.status_code == 401

    accepted = test_client.post(
        "/api/sensors/telemetry",
        json=payload,
        headers={"X-Device-Token": "test-only-device-token"},
    )
    assert accepted.status_code == 200
    assert accepted.json()["data_source"] == "device"
    assert accepted.json()["pump_status"] is False

    latest = test_client.get(
        "/api/sensors/latest",
        headers=auth_headers(farmer["token"]),
    )
    assert latest.status_code == 200
    assert latest.json()["data"]["data_source"] == "device"


def test_pump_control_is_owner_only_and_disabled_by_default(client, monkeypatch):
    test_client, _ = client
    farmer = register(test_client, "+919000000005")
    other_farmer = register(test_client, "+919000000006")
    monkeypatch.setenv("FARM_OWNER_USER_ID", str(farmer["user_id"]))

    payload = {"action": "ON", "device_id": "ESP32_TEST"}
    denied = test_client.post(
        "/api/sensors/pump/toggle",
        json=payload,
        headers=auth_headers(other_farmer["token"]),
    )
    assert denied.status_code == 403

    disabled = test_client.post(
        "/api/sensors/pump/toggle",
        json=payload,
        headers=auth_headers(farmer["token"]),
    )
    assert disabled.status_code == 503
    assert SYSTEM_STATE["pump_status"] is False


def test_assistant_does_not_invent_weather_or_pump_state(client, monkeypatch):
    test_client, _ = client
    farmer = register(test_client, "+919000000011")
    monkeypatch.setenv("FARM_OWNER_USER_ID", str(farmer["user_id"]))

    weather = test_client.post(
        "/api/assistant/chat",
        headers=auth_headers(farmer["token"]),
        json={"message": "What is the weather and rain forecast?", "language": "en"},
    )
    pump = test_client.post(
        "/api/assistant/chat",
        headers=auth_headers(farmer["token"]),
        json={"message": "Is the pump running?", "language": "en"},
    )

    assert weather.status_code == 200
    assert "forecast is unavailable" in weather.json()["reply"]
    assert pump.status_code == 200
    assert "status is unknown" in pump.json()["reply"]
    assert pump.json()["assistant_mode"] == "rule_based"


def test_threshold_order_and_measurement_bounds_are_validated(client, monkeypatch):
    test_client, _ = client
    farmer = register(test_client, "+919000000007")
    monkeypatch.setenv("FARM_OWNER_USER_ID", str(farmer["user_id"]))
    response = test_client.post(
        "/api/sensors/thresholds",
        headers=auth_headers(farmer["token"]),
        json={"min_moisture_threshold": 75, "max_moisture_threshold": 30},
    )
    assert response.status_code == 422

    monkeypatch.setenv("IOT_DEVICE_TOKEN", "test-only-device-token")
    invalid_telemetry = test_client.post(
        "/api/sensors/telemetry",
        headers={"X-Device-Token": "test-only-device-token"},
        json={
            "soil_moisture": 140,
            "temperature": 23,
            "humidity": 50,
        },
    )
    assert invalid_telemetry.status_code == 422


def test_image_upload_is_validated_and_returns_no_fake_result(client):
    test_client, _ = client
    farmer = register(test_client, "+919000000008")
    headers = auth_headers(farmer["token"])

    invalid_type = test_client.post(
        "/api/ai/scan-plant",
        headers=headers,
        files={"file": ("leaf.txt", b"not an image", "text/plain")},
    )
    assert invalid_type.status_code == 415

    image = Image.new("RGB", (32, 32), color=(50, 140, 70))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    response = test_client.post(
        "/api/ai/scan-plant",
        headers=headers,
        data={"crop_type": "Tomato", "language": "en"},
        files={"file": ("leaf.jpg", buffer.getvalue(), "image/jpeg")},
    )
    assert response.status_code == 200
    diagnosis = response.json()["diagnosis"]
    assert response.json()["status"] == "unavailable"
    assert diagnosis["available"] is False
    assert diagnosis["disease_detected"] is None
    assert diagnosis["confidence_percentage"] is None


def test_legacy_scan_history_is_marked_unverified(client):
    test_client, engine = client
    farmer = register(test_client, "+919000000010")
    with Session(engine) as db:
        db.add(
            AIDiagnosis(
                user_id=farmer["user_id"],
                crop_type="Tomato",
                disease_detected="Early Blight",
                confidence=94,
                health_status="Diseased",
                suggested_actions="Old demo advice",
            )
        )
        db.commit()

    history = test_client.get(
        f"/api/ai/history/{farmer['user_id']}",
        headers=auth_headers(farmer["token"]),
    )
    assert history.status_code == 200
    old_record = history.json()["history"][0]
    assert old_record["confidence"] is None
    assert old_record["health_status"] == "Unverified"
    assert "not a diagnosis" in old_record["disease"]
