import 'package:flutter/material.dart';

class WeatherScreen extends StatefulWidget {
  const WeatherScreen({Key? key}) : super(key: key);

  @override
  _WeatherScreenState createState() => _WeatherScreenState();
}

class _WeatherScreenState extends State<WeatherScreen> {
  final List<Map<String, dynamic>> _forecast = [
    {"day": "Today", "temp": "28.5°C", "condition": "Partly Cloudy", "rain": "35%", "icon": Icons.cloud},
    {"day": "Tomorrow", "temp": "26.0°C", "condition": "Moderate Rain", "rain": "80%", "icon": Icons.water_drop},
    {"day": "Thursday", "temp": "25.5°C", "condition": "Heavy Rain", "rain": "90%", "icon": Icons.thunderstorm},
    {"day": "Friday", "temp": "29.0°C", "condition": "Sunny", "rain": "15%", "icon": Icons.wb_sunny},
    {"day": "Saturday", "temp": "31.0°C", "condition": "Clear Sky", "rain": "5%", "icon": Icons.wb_sunny},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1E293B),
        title: const Text("Farm Weather & Rain Forecast", style: TextStyle(color: Colors.white)),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Current Weather Card
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [Colors.blue.shade900, Colors.teal.shade900],
                ),
                borderRadius: BorderRadius.circular(20),
              ),
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: const [
                          Text("Maharashtra, India", style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                          Text("Live Weather Telemetry", style: TextStyle(color: Colors.white60, fontSize: 12)),
                        ],
                      ),
                      const Icon(Icons.cloud, size: 48, color: Colors.lightBlueAccent),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: const [
                      _WeatherStat(label: "Temperature", value: "28.5 °C"),
                      _WeatherStat(label: "Humidity", value: "68 %"),
                      _WeatherStat(label: "Rain Chance", value: "35 %"),
                    ],
                  )
                ],
              ),
            ),
            const SizedBox(height: 20),

            // Weather-Based Smart Irrigation Recommendation
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.amber.shade900.withOpacity(0.3),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: Colors.amber.shade500),
              ),
              child: Row(
                children: const [
                  Icon(Icons.water_damage, color: Colors.amberAccent, size: 32),
                  SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      "Rain Expected Tomorrow (80% chance). Automated system will temporarily postpone pump activation to save water and energy.",
                      style: TextStyle(color: Colors.white, fontSize: 13),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),

            // 5-Day Forecast List
            const Text("5-Day Rain & Weather Forecast", style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),

            ..._forecast.map((item) => Container(
                  margin: const EdgeInsets.only(bottom: 8),
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(
                    color: const Color(0xFF1E293B),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Row(
                    children: [
                      Icon(item["icon"] as IconData, color: Colors.cyanAccent),
                      const SizedBox(width: 12),
                      SizedBox(
                        width: 90,
                        child: Text(item["day"], style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                      ),
                      Expanded(
                        child: Text(item["condition"], style: const TextStyle(color: Colors.white70, fontSize: 13)),
                      ),
                      Text("Rain: ${item['rain']}", style: const TextStyle(color: Colors.lightBlueAccent, fontWeight: FontWeight.bold)),
                    ],
                  ),
                ))
          ],
        ),
      ),
    );
  }
}

class _WeatherStat extends StatelessWidget {
  final String label;
  final String value;
  const _WeatherStat({Key? key, required this.label, required this.value}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(label, style: const TextStyle(color: Colors.white60, fontSize: 12)),
        const SizedBox(height: 4),
        Text(value, style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
      ],
    );
  }
}
