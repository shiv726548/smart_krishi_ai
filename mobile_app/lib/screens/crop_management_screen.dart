import 'package:flutter/material.dart';

class CropManagementScreen extends StatefulWidget {
  const CropManagementScreen({Key? key}) : super(key: key);

  @override
  _CropManagementScreenState createState() => _CropManagementScreenState();
}

class _CropManagementScreenState extends State<CropManagementScreen> {
  final List<Map<String, dynamic>> _myCrops = [
    {
      "id": 1,
      "name": "Tomato",
      "variety": "Abhinav Hybrid",
      "sowing_date": "2026-06-15",
      "location": "North Field Sector A",
      "size": 2.5,
      "stage": "Flowering & Fruiting",
      "target_moisture": "40% - 70%"
    },
    {
      "id": 2,
      "name": "Cotton",
      "variety": "Bt Cotton BG-II",
      "sowing_date": "2026-05-20",
      "location": "South Plot B",
      "size": 4.0,
      "stage": "Boll Formation",
      "target_moisture": "45% - 65%"
    }
  ];

  void _showAddCropDialog() {
    String name = "Rice";
    String location = "East Plot C";
    double size = 3.0;

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: const Color(0xFF1E293B),
        title: const Text("Register New Crop", style: TextStyle(color: Colors.white)),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              decoration: const InputDecoration(labelText: "Crop Name", labelStyle: TextStyle(color: Colors.white70)),
              style: const TextStyle(color: Colors.white),
              onChanged: (val) => name = val,
            ),
            TextField(
              decoration: const InputDecoration(labelText: "Farm Location / Plot Name", labelStyle: TextStyle(color: Colors.white70)),
              style: const TextStyle(color: Colors.white),
              onChanged: (val) => location = val,
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text("Cancel", style: TextStyle(color: Colors.white54)),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.green.shade600),
            onPressed: () {
              setState(() {
                _myCrops.add({
                  "id": DateTime.now().millisecondsSinceEpoch,
                  "name": name,
                  "variety": "Standard Hybrid",
                  "sowing_date": "2026-08-01",
                  "location": location,
                  "size": size,
                  "stage": "Seedling",
                  "target_moisture": "40% - 70%"
                });
              });
              Navigator.pop(ctx);
            },
            child: const Text("Add Crop", style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1E293B),
        title: const Text("Crop Management", style: TextStyle(color: Colors.white)),
        actions: [
          IconButton(
            icon: const Icon(Icons.add_circle, color: Colors.greenAccent, size: 28),
            onPressed: _showAddCropDialog,
          )
        ],
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: _myCrops.length,
        itemBuilder: (context, index) {
          final crop = _myCrops[index];
          return Container(
            margin: const EdgeInsets.only(bottom: 16),
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: const Color(0xFF1E293B),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: Colors.green.shade700),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Row(
                      children: [
                        const Icon(Icons.grass, color: Colors.greenAccent, size: 24),
                        const SizedBox(width: 8),
                        Text(crop["name"], style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                      ],
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: Colors.teal.shade800,
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Text(crop["stage"], style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold)),
                    )
                  ],
                ),
                const Divider(color: Colors.white10, height: 20),
                _cropMetaRow("Variety:", crop["variety"]),
                _cropMetaRow("Sowing Date:", crop["sowing_date"]),
                _cropMetaRow("Farm Location:", crop["location"]),
                _cropMetaRow("Field Size:", "${crop["size"]} Acres"),
                _cropMetaRow("Target Moisture:", crop["target_moisture"]),
                const SizedBox(height: 12),
                const Text("Upcoming Growth Schedule & Care Reminders:", style: TextStyle(color: Colors.greenAccent, fontSize: 13, fontWeight: FontWeight.bold)),
                const SizedBox(height: 6),
                const Text("• Day 45: Top dress 25kg/acre Urea & inspect lower leaves for blights.", style: TextStyle(color: Colors.white70, fontSize: 12)),
                const Text("• Day 60: Spray NPK 0:52:34 for enhanced flowering & yield.", style: TextStyle(color: Colors.white70, fontSize: 12)),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _cropMetaRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 4),
      child: Row(
        children: [
          SizedBox(width: 120, child: Text(label, style: const TextStyle(color: Colors.white54, fontSize: 13))),
          Expanded(child: Text(value, style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.w500))),
        ],
      ),
    );
  }
}
