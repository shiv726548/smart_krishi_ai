/*
 * Smart Krishi AI - ESP32 Firmware
 * Features:
 * - Sensors: Capacitive Soil Moisture, DHT22 (Temp & Humidity), Battery Voltage
 * - Actuators: 5V Relay Water Pump Controller
 * - Connectivity: WiFi HTTP POST Telemetry & Control Polling
 * - Safety: local emergency override if disconnected & 30-min auto pump shutdown watchdog
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <DHT.h>
#include "config.h"

#define DHTTYPE DHT22

DHT dht(DHT_PIN, DHTTYPE);

// Device State Variables
float currentMoisture = 0.0;
float currentTemp = 0.0;
float currentHumidity = 0.0;
float batteryPercentage = 95.0;
bool pumpState = false;
unsigned long pumpStartTime = 0;
unsigned long lastTelemetryTime = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("==========================================");
  Serial.println("Smart Krishi AI - ESP32 IoT Node Booting...");
  Serial.println("==========================================");

  // Initialize Pin Modes
  pinMode(RELAY_PUMP_PIN, OUTPUT);
  pinMode(STATUS_LED_PIN, OUTPUT);
  digitalWrite(RELAY_PUMP_PIN, HIGH); // Relay off (Active LOW)
  digitalWrite(STATUS_LED_PIN, LOW);

  // Initialize Sensors
  dht.begin();
  analogReadResolution(12); // ESP32 12-bit ADC (0 - 4095)

  // Connect to WiFi
  connectWiFi();
}

void loop() {
  // Check WiFi Connection
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }

  // 1. Read Sensors
  readSensors();

  // 2. Safety Watchdog Check
  checkSafetyWatchdog();

  // 3. Periodic Cloud Telemetry & Remote Control Sync
  unsigned long now = millis();
  if (now - lastTelemetryTime >= TELEMETRY_INTERVAL_MS) {
    lastTelemetryTime = now;
    sendTelemetryAndSyncControl();
  }

  delay(100);
}

void connectWiFi() {
  Serial.print("Connecting to WiFi: ");
  Serial.println(WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    digitalWrite(STATUS_LED_PIN, !digitalRead(STATUS_LED_PIN)); // Blink while connecting
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    digitalWrite(STATUS_LED_PIN, HIGH);
    Serial.println("\nWiFi Connected Successfully!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    digitalWrite(STATUS_LED_PIN, LOW);
    Serial.println("\nWiFi Connection Failed! Operating in Offline Fallback Mode.");
    offlineEmergencyControl();
  }
}

void readSensors() {
  // Read Soil Moisture
  int rawMoisture = analogRead(SOIL_MOISTURE_PIN);
  currentMoisture = map(rawMoisture, AIR_VAL, WATER_VAL, 0, 100);
  currentMoisture = constrain(currentMoisture, 0.0, 100.0);

  // Read DHT22
  float t = dht.readTemperature();
  float h = dht.readHumidity();
  if (!isnan(t)) currentTemp = t;
  if (!isnan(h)) currentHumidity = h;

  // Read Battery Voltage (Voltage Divider on Pin 35)
  int rawBattery = analogRead(BATTERY_ADC_PIN);
  float batteryVolt = (rawBattery / 4095.0) * 3.3 * 2.0; // 1:1 divider
  batteryPercentage = constrain(((batteryVolt - 3.2) / (4.2 - 3.2)) * 100.0, 0.0, 100.0);
}

void checkSafetyWatchdog() {
  // If pump has been running continuously for longer than MAX_PUMP_RUN_MS (30 mins)
  if (pumpState && (millis() - pumpStartTime > MAX_PUMP_RUN_MS)) {
    Serial.println("CRITICAL ALERT: Maximum Pump Run Time Exceeded (30 Mins). Auto Shutdown Triggered!");
    setPumpState(false);
  }
}

void offlineEmergencyControl() {
  // Fallback if cloud is unreachable: local automatic irrigation based on hardcoded thresholds
  if (currentMoisture < DEFAULT_MIN_MOISTURE && !pumpState) {
    Serial.println("[OFFLINE MODE] Moisture Low (<40%). Starting Pump.");
    setPumpState(true);
  } else if (currentMoisture >= DEFAULT_MAX_MOISTURE && pumpState) {
    Serial.println("[OFFLINE MODE] Moisture Optimal (>=70%). Stopping Pump.");
    setPumpState(false);
  }
}

void sendTelemetryAndSyncControl() {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.begin(TELEMETRY_URL);
  http.addHeader("Content-Type", "application/json");

  // Create JSON Payload
  StaticJsonDocument<256> doc;
  doc["device_id"] = "ESP32_KRISHI_01";
  doc["soil_moisture"] = currentMoisture;
  doc["temperature"] = currentTemp;
  doc["humidity"] = currentHumidity;
  doc["battery_level"] = batteryPercentage;

  String jsonString;
  serializeJson(doc, jsonString);

  Serial.println("\n[HTTP POST Telemetry] Sending sensor data to Cloud...");
  int httpCode = http.POST(jsonString);

  if (httpCode > 0) {
    String response = http.getString();
    Serial.print("Cloud Response Code: ");
    Serial.println(httpCode);

    // Parse Cloud Pump Command
    StaticJsonDocument<256> respDoc;
    DeserializationError err = deserializeJson(respDoc, response);
    if (!err && respDoc.containsKey("pump_status")) {
      bool desiredPumpState = respDoc["pump_status"];
      if (desiredPumpState != pumpState) {
        Serial.print("Cloud Command Received -> Pump State Change to: ");
        Serial.println(desiredPumpState ? "ON" : "OFF");
        setPumpState(desiredPumpState);
      }
    }
  } else {
    Serial.print("HTTP POST Failed, error: ");
    Serial.println(http.errorToString(httpCode));
    offlineEmergencyControl();
  }

  http.end();
}

void setPumpState(bool state) {
  pumpState = state;
  if (pumpState) {
    digitalWrite(RELAY_PUMP_PIN, LOW); // Active LOW relay ON
    pumpStartTime = millis();
    Serial.println(">>> PUMP HARDWARE TURNED ON <<<");
  } else {
    digitalWrite(RELAY_PUMP_PIN, HIGH); // Active LOW relay OFF
    Serial.println(">>> PUMP HARDWARE TURNED OFF <<<");
  }
}
