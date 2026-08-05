import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/sensor_model.dart';
import '../models/crop_model.dart';
import '../models/ai_result_model.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:8000'; // Replace with Cloud URL

  static Future<SensorDataModel> fetchLatestSensorData() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/api/sensors/latest'));
      if (response.statusCode == 200) {
        return SensorDataModel.fromJson(jsonDecode(response.body));
      }
    } catch (e) {
      print('Sensor API Error: $e');
    }
    // Default fallback values if backend is offline
    return SensorDataModel(
      deviceId: 'ESP32_KRISHI_01',
      soilMoisture: 38.5,
      temperature: 28.2,
      humidity: 64.0,
      nitrogen: 45.0,
      phosphorus: 25.0,
      potassium: 60.0,
      pumpStatus: false,
      batteryLevel: 94.0,
      alerts: ['Soil moisture is low (38.5%). Automated irrigation standby.'],
    );
  }

  static Future<bool> togglePump(bool turnOn) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/sensors/pump/toggle'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'device_id': 'ESP32_KRISHI_01',
          'action': turnOn ? 'ON' : 'OFF',
          'reason': 'Farmer mobile app manual toggle'
        }),
      );
      return response.statusCode == 200;
    } catch (e) {
      print('Pump toggle error: $e');
      return false;
    }
  }

  static Future<AIResultModel?> scanPlantDisease(String filePath, String cropType, String lang) async {
    try {
      var request = http.MultipartRequest('POST', Uri.parse('$baseUrl/api/ai/scan-plant'));
      request.fields['crop_type'] = cropType;
      request.fields['language'] = lang;
      request.fields['user_id'] = '1';
      request.files.add(await http.MultipartFile.fromPath('file', filePath));

      var streamedResponse = await request.send();
      var response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        return AIResultModel.fromJson(jsonDecode(response.body));
      }
    } catch (e) {
      print('Plant scan API error: $e');
    }
    return null;
  }

  static Future<String> askAiAssistant(String query, String lang, String cropName) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/assistant/chat'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'message': query,
          'language': lang,
          'crop_name': cropName,
        }),
      );
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['reply'] ?? 'Assistant error';
      }
    } catch (e) {
      print('Assistant API error: $e');
    }
    return 'Could not connect to AI server. Please check internet connection.';
  }

  static Future<List<CropModel>> fetchUserCrops(int userId) async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/api/crops/user/$userId'));
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final List cropsJson = data['crops'] ?? [];
        return cropsJson.map((item) => CropModel.fromJson(item)).toList();
      }
    } catch (e) {
      print('Crops API error: $e');
    }
    return [];
  }
}
