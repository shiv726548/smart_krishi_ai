# Smart Krishi AI

A student/demo agriculture project with a FastAPI backend, a browser dashboard, Flutter mobile source, and optional ESP32 firmware.

## Current implementation status

- **Authentication:** password hashes use scrypt; login returns a signed, expiring bearer token. Existing SHA-256 password hashes are upgraded after a successful login.
- **Farm data:** crop records require sign-in and are scoped to the signed-in user. Sensor reads and controls additionally require the configured farm-owner account.
- **Sensors:** values are unavailable until an authenticated ESP32 sends telemetry. The browser dashboard uses local demo sliders and does not submit them as device readings.
- **Plant scans:** image uploads are checked for supported format and size. There are no trained model weights in this repository, so the API explicitly reports that no diagnosis was generated.
- **Old scan history:** records created by the earlier heuristic are flagged as unverified; their old confidence values are not presented.
- **Weather:** live weather is not configured. The API and clients show an unavailable state rather than invented conditions.
- **Pump:** server-side and firmware controls are disabled by default. Enabling them requires explicit local configuration on both sides and verified hardware.
- **Assistant:** the included assistant is rule-based, not a generative AI model; its farm-specific endpoints require the owner account.

These safeguards make the demo honest and safer to present; they do not make the system production-ready or validate agricultural advice.

## Run the backend and web dashboard

Requires Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
export JWT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
export CORS_ORIGINS="http://localhost:8000,http://127.0.0.1:8000"
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000/app` for the demo dashboard or `http://localhost:8000/docs` for the API.

The first registration returns a `user_id` and access token. To enable private farm-owner endpoints in that local session, restart the server with `FARM_OWNER_USER_ID` set to that account's ID. Set `JWT_SECRET_KEY` to a stable, private random value before registering if tokens should survive server restarts. Do not commit `.env`, credentials, or device tokens.

SQLite is used by default. Set `DATABASE_URL` to a database URL only when you have configured that database. The app does not apply schema migrations automatically.

## Run tests

```bash
python -m pytest -q
```

The tests use a temporary SQLite database and verify authentication, crop ownership, device-token checks, pump-off defaults, upload validation, and honest unavailable states. They do not test real ESP32 hardware, a trained model, a live weather provider, or production deployment.

## Flutter mobile app

The mobile source is under `mobile_app/`. Its API base URL defaults to `http://10.0.2.2:8000` for the Android emulator. For an iOS simulator or a phone on your network, pass the appropriate reachable backend URL:

```bash
cd mobile_app
flutter pub get
flutter run --dart-define=API_BASE_URL=http://YOUR_COMPUTER_LAN_IP:8000
```

The access token is held in memory for the current app session; sign in again after restarting the app. Hardware controls remain unavailable unless the server and firmware are explicitly configured.

## Optional ESP32 setup

The tracked configuration contains no Wi-Fi credentials. Copy `iot_firmware/secrets_local.h.example` to `iot_firmware/secrets_local.h`, fill in local values, and keep that file out of Git. The backend's `IOT_DEVICE_TOKEN` must match the firmware's `DEVICE_API_TOKEN`.

Keep `PUMP_CONTROL_ENABLED` set to `false` on the server and `0` in firmware unless the owner has verified the relay, pump, water supply, thresholds, and emergency stop. To opt in later, both settings must be changed deliberately. Remote deployments should use HTTPS.

## Remaining limitations

- A suitable trained plant-disease model, its license, weights, and validation data still need to be selected and integrated.
- A legitimate weather provider is not connected; therefore there is no weather-based irrigation recommendation.
- Farm state currently represents one configured device, not a multi-farm/device tenancy system.
- No public deployment was performed. Hosting, TLS, database backups, device provisioning, and operational safety require separate setup.
