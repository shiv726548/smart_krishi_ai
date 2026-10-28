/*
 * Smart Krishi AI - ESP32 Firmware Configuration Header
 * Hardware Target: ESP32 DevKit v1 / ESP32-WROOM-32
 *
 * Put local Wi-Fi credentials and the device token in secrets_local.h.
 * That file is ignored by Git and must never be committed.
 */

#ifndef SMART_KRISHI_CONFIG_H
#define SMART_KRISHI_CONFIG_H

#if defined(__has_include)
#if __has_include("secrets_local.h")
#include "secrets_local.h"
#endif
#endif

#ifndef WIFI_SSID
#define WIFI_SSID ""
#endif

#ifndef WIFI_PASS
#define WIFI_PASS ""
#endif

#ifndef DEVICE_API_TOKEN
#define DEVICE_API_TOKEN ""
#endif

// Hardware pump commands are deliberately disabled until the owner verifies
// the pump, relay wiring, limits, and the matching server-side opt-in.
#ifndef PUMP_CONTROL_ENABLED
#define PUMP_CONTROL_ENABLED 0
#endif

// Replace with the backend's local address or an HTTPS deployment URL.
#define SERVER_HOST     "http://192.168.1.100:8000"
#define TELEMETRY_URL   SERVER_HOST "/api/sensors/telemetry"
#define PUMP_STATUS_URL SERVER_HOST "/api/sensors/latest"

// Hardware pin definition
#define SOIL_MOISTURE_PIN 34
#define DHT_PIN           4
#define RELAY_PUMP_PIN    26
#define STATUS_LED_PIN    2
#define BATTERY_ADC_PIN   35

// Calibration parameters for the capacitive soil moisture sensor
#define AIR_VAL      3200
#define WATER_VAL    1400

// Offline thresholds are used only when pump control is explicitly enabled.
#define DEFAULT_MIN_MOISTURE  40.0
#define DEFAULT_MAX_MOISTURE  70.0

// Safety watchdog and telemetry interval
#define MAX_PUMP_RUN_MS       (30 * 60 * 1000UL)
#define TELEMETRY_INTERVAL_MS 10000

#endif // SMART_KRISHI_CONFIG_H
