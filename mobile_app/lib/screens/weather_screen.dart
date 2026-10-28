import 'package:flutter/material.dart';

import '../services/api_service.dart';

class WeatherScreen extends StatefulWidget {
  const WeatherScreen({Key? key}) : super(key: key);

  @override
  _WeatherScreenState createState() => _WeatherScreenState();
}

class _WeatherScreenState extends State<WeatherScreen> {
  bool _isLoading = true;
  String _message =
      'Live weather is not configured. No forecast or rain probability is being reported.';

  @override
  void initState() {
    super.initState();
    _loadWeather();
  }

  Future<void> _loadWeather() async {
    final weather = await ApiService.fetchWeather();
    if (!mounted) return;
    setState(() {
      _isLoading = false;
      _message = weather == null
          ? 'Weather service could not be reached. No forecast is available.'
          : (weather['irrigation_recommendation']?['advice'] ??
              'No verified weather forecast is available.');
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1E293B),
        title: const Text(
          "Farm Weather",
          style: TextStyle(color: Colors.white),
        ),
        actions: [
          IconButton(
            tooltip: 'Refresh',
            onPressed: _isLoading ? null : _loadWeather,
            icon: const Icon(Icons.refresh),
          ),
        ],
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Container(
            width: double.infinity,
            padding: const EdgeInsets.all(22),
            decoration: BoxDecoration(
              color: const Color(0xFF1E293B),
              borderRadius: BorderRadius.circular(18),
              border: Border.all(color: Colors.amberAccent.withOpacity(0.7)),
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(
                  _isLoading ? Icons.cloud_sync : Icons.cloud_off,
                  size: 58,
                  color: Colors.amberAccent,
                ),
                const SizedBox(height: 16),
                Text(
                  _isLoading ? 'Checking weather availability…' : 'Forecast unavailable',
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 10),
                Text(
                  _message,
                  textAlign: TextAlign.center,
                  style: const TextStyle(color: Colors.white70, height: 1.4),
                ),
                const SizedBox(height: 12),
                const Text(
                  'Do not use this screen to make irrigation decisions. Check a trusted local forecast and the field directly.',
                  textAlign: TextAlign.center,
                  style: TextStyle(color: Colors.white54, fontSize: 12),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
