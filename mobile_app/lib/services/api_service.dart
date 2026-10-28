import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/sensor_model.dart';
import '../models/crop_model.dart';
import '../models/ai_result_model.dart';

class ApiService {
  static const String baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://10.0.2.2:8000',
  );
  static String? accessToken;
  static int? currentUserId;

  static Map<String, String> get _authHeaders => {
        if (accessToken != null) 'Authorization': 'Bearer $accessToken',
      };

  static Future<Map<String, dynamic>> authenticate({
    required bool register,
    required String phoneNumber,
    required String password,
    String fullName = '',
    String location = '',
    String language = 'en',
  }) async {
    final path = register ? '/api/auth/register' : '/api/auth/login';
    final payload = <String, dynamic>{
      'phone_number': phoneNumber.trim(),
      'password': password,
      if (register) ...{
        'full_name': fullName.trim(),
        'location': location,
        'preferred_language': language,
      },
    };
    final response = await http
        .post(
          Uri.parse('$baseUrl$path'),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode(payload),
        )
        .timeout(const Duration(seconds: 15));
    final data = jsonDecode(response.body) as Map<String, dynamic>;
    if (response.statusCode < 200 || response.statusCode >= 300) {
      throw Exception(data['detail'] ?? 'Authentication failed');
    }
    accessToken = data['token'] as String?;
    currentUserId = (data['user_id'] as num?)?.toInt();
    if (accessToken == null || currentUserId == null) {
      throw Exception('The server returned an incomplete login response');
    }
    return data;
  }

  static Future<SensorDataModel> fetchLatestSensorData() async {
    try {
      final response = await http
          .get(Uri.parse('$baseUrl/api/sensors/latest'), headers: _authHeaders)
          .timeout(const Duration(seconds: 10));
      if (response.statusCode == 200) {
        return SensorDataModel.fromJson(jsonDecode(response.body));
      }
    } catch (e) {
      // Return an explicit unavailable state; do not invent sensor readings.
    }
    return SensorDataModel(
      deviceId: 'ESP32_KRISHI_01',
      soilMoisture: 0,
      temperature: 0,
      humidity: 0,
      nitrogen: 0,
      phosphorus: 0,
      potassium: 0,
      pumpStatus: false,
      batteryLevel: 0,
      alerts: ['No authenticated live sensor reading is available.'],
      dataSource: 'unavailable',
      pumpEnabled: false,
    );
  }

  static Future<bool> togglePump(bool turnOn) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/sensors/pump/toggle'),
        headers: {'Content-Type': 'application/json', ..._authHeaders},
        body: jsonEncode({
          'device_id': 'ESP32_KRISHI_01',
          'action': turnOn ? 'ON' : 'OFF',
          'reason': 'Farmer mobile app manual toggle'
        }),
      );
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }

  static Future<AIResultModel?> scanPlantDisease(String filePath, String cropType, String lang) async {
    try {
      var request = http.MultipartRequest('POST', Uri.parse('$baseUrl/api/ai/scan-plant'));
      request.headers.addAll(_authHeaders);
      request.fields['crop_type'] = cropType;
      request.fields['language'] = lang;
      request.files.add(await http.MultipartFile.fromPath('file', filePath));

      var streamedResponse = await request.send();
      var response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        return AIResultModel.fromJson(jsonDecode(response.body));
      }
    } catch (e) {
      return null;
    }
    return null;
  }

  static Future<String> askAiAssistant(
    String query,
    String lang, {
    String? cropName,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/assistant/chat'),
        headers: {'Content-Type': 'application/json', ..._authHeaders},
        body: jsonEncode({
          'message': query,
          'language': lang,
          if (cropName != null && cropName.trim().isNotEmpty)
            'crop_name': cropName.trim(),
        }),
      );
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['reply'] ?? 'Assistant error';
      }
    } catch (e) {
      return 'The assistant is unavailable. Check your connection and sign-in.';
    }
    return 'Could not connect to AI server. Please check internet connection.';
  }

  static Future<List<CropModel>?> fetchUserCrops(int userId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/crops/user/$userId'),
        headers: _authHeaders,
      );
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final List cropsJson = data['crops'] ?? [];
        return cropsJson.map((item) => CropModel.fromJson(item)).toList();
      }
    } catch (e) {
      return null;
    }
    return null;
  }

  static Future<bool> addCrop({
    required String cropName,
    required String variety,
    required String sowingDate,
    required double fieldSizeAcres,
    required String farmLocation,
    required String growthStage,
  }) async {
    try {
      final response = await http
          .post(
            Uri.parse('$baseUrl/api/crops/add'),
            headers: {'Content-Type': 'application/json', ..._authHeaders},
            body: jsonEncode({
              'crop_name': cropName,
              'variety': variety,
              'sowing_date': sowingDate,
              'field_size_acres': fieldSizeAcres,
              'farm_location': farmLocation,
              'growth_stage': growthStage,
            }),
          )
          .timeout(const Duration(seconds: 10));
      return response.statusCode == 200;
    } catch (_) {
      return false;
    }
  }

  static Future<Map<String, dynamic>?> fetchWeather(
      {String location = 'Maharashtra, India'}) async {
    try {
      final uri = Uri.parse('$baseUrl/api/weather/current')
          .replace(queryParameters: {'location': location});
      final response =
          await http.get(uri).timeout(const Duration(seconds: 10));
      if (response.statusCode == 200) {
        return jsonDecode(response.body) as Map<String, dynamic>;
      }
    } catch (_) {
      return null;
    }
    return null;
  }
}
