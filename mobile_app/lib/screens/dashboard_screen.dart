import 'package:flutter/material.dart';
import '../models/sensor_model.dart';
import '../services/api_service.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({Key? key}) : super(key: key);

  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  SensorDataModel? _sensorData;
  bool _isLoading = true;
  bool _isTogglingPump = false;

  @override
  void initState() {
    super.initState();
    _loadTelemetry();
  }

  Future<void> _loadTelemetry() async {
    final data = await ApiService.fetchLatestSensorData();
    if (mounted) {
      setState(() {
        _sensorData = data;
        _isLoading = false;
      });
    }
  }

  Future<void> _togglePump(bool currentStatus) async {
    setState(() => _isTogglingPump = true);
    final success = await ApiService.togglePump(!currentStatus);
    if (success) {
      await _loadTelemetry();
    }
    setState(() => _isTogglingPump = false);
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading || _sensorData == null) {
      return const Scaffold(
        backgroundColor: Color(0xFF0F172A),
        body: Center(child: CircularProgressIndicator(color: Colors.greenAccent)),
      );
    }

    final s = _sensorData!;

    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1E293B),
        title: Row(
          children: const [
            Icon(Icons.eco, color: Colors.greenAccent),
            SizedBox(width: 8),
            Text("Smart Krishi Dashboard", style: TextStyle(color: Colors.white, fontSize: 18)),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh, color: Colors.greenAccent),
            onPressed: _loadTelemetry,
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: _loadTelemetry,
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Crop Banner
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: [Colors.green.shade900, Colors.teal.shade800],
                  ),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.agriculture, size: 40, color: Colors.white),
                    const SizedBox(width: 12),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: const [
                        Text("Active Crop: Tomato (Hybrid)", style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                        Text("Growth Stage: Flowering (Day 42)", style: TextStyle(color: Colors.white70, fontSize: 14)),
                      ],
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 20),

              // Sensor Metric Cards Grid
              const Text("Real-Time IoT Field Telemetry", style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
              const SizedBox(height: 12),

              GridView.count(
                crossAxisCount: 2,
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                childAspectRatio: 1.4,
                crossAxisSpacing: 12,
                mainAxisSpacing: 12,
                children: [
                  _buildMetricCard("Soil Moisture", "${s.soilMoisture.toStringAsFixed(1)}%", Icons.water_drop, s.soilMoisture < 40 ? Colors.redAccent : Colors.lightBlueAccent),
                  _buildMetricCard("Temperature", "${s.temperature.toStringAsFixed(1)} °C", Icons.thermostat, Colors.orangeAccent),
                  _buildMetricCard("Air Humidity", "${s.humidity.toStringAsFixed(1)}%", Icons.cloud, Colors.tealAccent),
                  _buildMetricCard("Sensor Battery", "${s.batteryLevel.toStringAsFixed(0)}%", Icons.battery_charging_full, Colors.greenAccent),
                ],
              ),

              const SizedBox(height: 20),

              // Automatic Irrigation Pump Control Box
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: const Color(0xFF1E293B),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: s.pumpStatus ? Colors.greenAccent : Colors.white10),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.all(12),
                          decoration: BoxDecoration(
                            color: s.pumpStatus ? Colors.green.withOpacity(0.2) : Colors.red.withOpacity(0.2),
                            shape: BoxShape.circle,
                          ),
                          child: Icon(Icons.power_settings_new, color: s.pumpStatus ? Colors.greenAccent : Colors.redAccent, size: 28),
                        ),
                        const SizedBox(width: 12),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text("Water Pump Controller", style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
                            Text(
                              s.pumpStatus ? "Pump Status: ON (Irrigating)" : "Pump Status: OFF (Standby)",
                              style: TextStyle(color: s.pumpStatus ? Colors.greenAccent : Colors.white60, fontSize: 13),
                            ),
                          ],
                        ),
                      ],
                    ),
                    ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: s.pumpStatus ? Colors.redAccent : Colors.green.shade600,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                      onPressed: _isTogglingPump ? null : () => _togglePump(s.pumpStatus),
                      child: _isTogglingPump
                          ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                          : Text(s.pumpStatus ? "STOP" : "START", style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 20),

              // Alerts & AI Recommendations Section
              const Text("System Alerts & AI Advice", style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
              const SizedBox(height: 12),

              if (s.alerts.isNotEmpty)
                ...s.alerts.map((alert) => Container(
                      margin: const EdgeInsets.only(bottom: 8),
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: Colors.amber.shade900.withOpacity(0.3),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: Colors.amber.shade600),
                      ),
                      child: Row(
                        children: [
                          const Icon(Icons.warning_amber, color: Colors.amberAccent),
                          const SizedBox(width: 8),
                          Expanded(child: Text(alert, style: const TextStyle(color: Colors.white, fontSize: 13))),
                        ],
                      ),
                    )),

              Container(
                padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(
                  color: Colors.indigo.shade900.withOpacity(0.4),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.indigoAccent),
                ),
                child: Row(
                  children: const [
                    Icon(Icons.psychology, color: Colors.cyanAccent, size: 28),
                    SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        "AI Recommendation: Optimal moisture target is 40-70%. Maintain light morning irrigation schedule.",
                        style: TextStyle(color: Colors.white, fontSize: 13),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildMetricCard(String title, String value, IconData icon, Color color) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: const Color(0xFF1E293B),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.white10),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(title, style: const TextStyle(color: Colors.white60, fontSize: 12)),
              Icon(icon, color: color, size: 20),
            ],
          ),
          const SizedBox(height: 8),
          Text(value, style: TextStyle(color: color, fontSize: 20, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }
}
