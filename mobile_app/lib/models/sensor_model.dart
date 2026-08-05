class SensorDataModel {
  final String deviceId;
  final double soilMoisture;
  final double temperature;
  final double humidity;
  final double nitrogen;
  final double phosphorus;
  final double potassium;
  final bool pumpStatus;
  final double batteryLevel;
  final List<String> alerts;

  SensorDataModel({
    required this.deviceId,
    required this.soilMoisture,
    required this.temperature,
    required this.humidity,
    required this.nitrogen,
    required this.phosphorus,
    required this.potassium,
    required this.pumpStatus,
    required this.batteryLevel,
    required this.alerts,
  });

  factory SensorDataModel.fromJson(Map<String, dynamic> json) {
    final data = json['data'] ?? json;
    return SensorDataModel(
      deviceId: data['device_id'] ?? 'ESP32_KRISHI_01',
      soilMoisture: (data['soil_moisture'] ?? 0.0).toDouble(),
      temperature: (data['temperature'] ?? 0.0).toDouble(),
      humidity: (data['humidity'] ?? 0.0).toDouble(),
      nitrogen: (data['nitrogen'] ?? 45.0).toDouble(),
      phosphorus: (data['phosphorus'] ?? 25.0).toDouble(),
      potassium: (data['potassium'] ?? 60.0).toDouble(),
      pumpStatus: data['pump_status'] ?? false,
      batteryLevel: (data['battery_level'] ?? 95.0).toDouble(),
      alerts: List<String>.from(data['alerts'] ?? []),
    );
  }
}
