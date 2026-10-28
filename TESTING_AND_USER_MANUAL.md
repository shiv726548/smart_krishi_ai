# Testing and safe demo guide

## Start the API and web dashboard

From the repository root, create a virtual environment and install `requirements.txt`, then set a private `JWT_SECRET_KEY` and run:

```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

- Dashboard: `http://localhost:8000/app`
- API documentation: `http://localhost:8000/docs`
- Tests: `python -m pytest -q`

Use `/api/auth/register` in the API docs to create a test farmer. The response includes an access token. Set `FARM_OWNER_USER_ID` to the returned account ID and restart the server before using owner-only sensor endpoints.

## What the demo does and does not do

- Browser slider values are simulated and are not sent to the ESP32 endpoint.
- The scanner validates supported image uploads but cannot diagnose a plant until trained weights are added. It does not return an invented disease or confidence score.
- Historical entries created by the previous heuristic are labelled unverified and must not be treated as diagnoses.
- Weather is marked unavailable because no live provider is configured. Check a trusted local forecast before making irrigation decisions.
- Pump control is disabled by default in both the API and firmware. No physical device should be connected or controlled unless the owner separately verifies the hardware and opts in on both sides.
- The built-in assistant uses fixed rules and general guidance; it is not a generative AI system or a substitute for local agricultural advice.

## Flutter app

The Flutter source is in `mobile_app/`. See the repository README for the `flutter pub get` and `flutter run` commands and how to set `API_BASE_URL`.

## Hardware secrets and safety

Copy `iot_firmware/secrets_local.h.example` to the ignored `iot_firmware/secrets_local.h` for local Wi-Fi/device configuration. Never commit that local file. The server and firmware device tokens must match. The public Git history may contain old Wi-Fi credentials; rotate them before connecting hardware.
