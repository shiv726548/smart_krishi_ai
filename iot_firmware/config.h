/*
 * Smart Krishi AI - ESP32 Firmware Configuration Header
 * Hardware Target: ESP32 DevKit v1 / ESP32-WROOM-32
 */

#ifndef SMART_KRISHI_CONFIG_H
#define SMART_KRISHI_CONFIG_H

// WiFi Credentials
#define WIFI_SSID       "Smart_Krishi_Farm_WiFi"
#define WIFI_PASS       "FarmerSmart2026"

// Server Configuration
#define SERVER_HOST     "http://192.168.1.100:8000" // Replace with Cloud Server IP / Domain
#define TELEMETRY_URL   SERVER_HOST "/api/sensors/telemetry"
#define PUMP_STATUS_URL SERVER_HOST "/api/sensors/latest"

// Hardware Pin Definition
#define SOIL_MOISTURE_PIN 34   // Analog Input Pin for Capacitive Moisture Sensor v1.2
#define DHT_PIN           4    // Digital Pin for DHT22 Temperature & Humidity Sensor
#define RELAY_PUMP_PIN    26   // Digital Output Pin for 5V Relay Module (Active LOW)
#define STATUS_LED_PIN    2    // Built-in LED Pin for Status Indication
#define BATTERY_ADC_PIN   35   // Analog Input for Solar Battery Voltage Divider

// Calibration Parameters for Capacitive Soil Moisture Sensor v1.2
// Measured raw ADC values (0 - 4095 on ESP32)
#define AIR_VAL      3200   // Raw reading in dry air (0% moisture)
#define WATER_VAL    1400   // Raw reading in submerged water (100% moisture)

// Local Offline Fallback Thresholds (If Cloud Connection Fails)
#define DEFAULT_MIN_MOISTURE  40.0 // %
#define DEFAULT_MAX_MOISTURE  70.0 // %

// Safety Watchdog Parameters
#define MAX_PUMP_RUN_MS       (30 * 60 * 1000UL) // Max 30 minutes continuous run
#define TELEMETRY_INTERVAL_MS 10000              // Send sensor telemetry every 10 sec

#endif // SMART_KRISHI_CONFIG_H
