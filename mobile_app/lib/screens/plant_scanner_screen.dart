import 'package:flutter/material.dart';

class PlantScannerScreen extends StatefulWidget {
  const PlantScannerScreen({Key? key}) : super(key: key);

  @override
  _PlantScannerScreenState createState() => _PlantScannerScreenState();
}

class _PlantScannerScreenState extends State<PlantScannerScreen> {
  String selectedCrop = "Tomato";
  bool isScanning = false;
  Map<String, dynamic>? scanResult;

  final List<String> supportedCrops = ["Tomato", "Potato", "Rice", "Wheat", "Cotton", "Corn"];

  void _runMockScan() {
    setState(() => isScanning = true);
    Future.delayed(const Duration(seconds: 2), () {
      setState(() {
        isScanning = false;
        scanResult = {
          "crop": selectedCrop,
          "disease_detected": selectedCrop == "Tomato" ? "Early Blight" : "Leaf Spot",
          "health_status": "Diseased",
          "confidence": 92,
          "cause": "Fungal infection by Alternaria solani",
          "symptoms": "Concentric target-board ring spots on lower leaves with yellow halos.",
          "suggested_actions": [
            "Prune infected lower leaves and safely burn or discard them.",
            "Avoid overhead leaf sprinkling; irrigate near root zone.",
            "Fungicide spray: Mancozeb (75% WP) at 2g/liter of water.",
            "Organic spray: Neem oil solution (5ml/liter)."
          ],
          "chemical_treatment": "Mancozeb 75 WP (2g/L) or Copper Oxychloride 3g/L",
          "organic_treatment": "Neem Seed Kernel Extract 5% or Trichoderma viride"
        };
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1E293B),
        title: const Text("AI Plant Health Scanner", style: TextStyle(color: Colors.white)),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Crop Selector
            const Text("Select Crop Type:", style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            SizedBox(
              height: 40,
              child: ListView(
                scrollDirection: Axis.horizontal,
                children: supportedCrops.map((crop) {
                  final isSel = crop == selectedCrop;
                  return Padding(
                    padding: const EdgeInsets.only(right: 8.0),
                    child: ChoiceChip(
                      label: Text(crop, style: TextStyle(color: isSel ? Colors.black : Colors.white)),
                      selected: isSel,
                      selectedColor: Colors.greenAccent,
                      backgroundColor: const Color(0xFF1E293B),
                      onSelected: (val) {
                        if (val) setState(() => selectedCrop = crop);
                      },
                    ),
                  );
                }).toList(),
              ),
            ),
            const SizedBox(height: 20),

            // Camera Scanner Box
            Container(
              width: double.infinity,
              height: 220,
              decoration: BoxDecoration(
                color: const Color(0xFF1E293B),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: Colors.greenAccent.withOpacity(0.5), width: 2),
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.camera_alt, size: 60, color: Colors.greenAccent.withOpacity(0.8)),
                  const SizedBox(height: 12),
                  const Text("Capture or Upload Plant/Leaf Photo", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 4),
                  const Text("Supports Tomato, Potato, Rice, Wheat, Cotton, Corn", style: TextStyle(color: Colors.white54, fontSize: 12)),
                  const SizedBox(height: 16),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      ElevatedButton.icon(
                        style: ElevatedButton.styleFrom(backgroundColor: Colors.green.shade600),
                        icon: const Icon(Icons.photo_camera, color: Colors.white),
                        label: const Text("Take Photo", style: TextStyle(color: Colors.white)),
                        onPressed: isScanning ? null : _runMockScan,
                      ),
                      const SizedBox(width: 12),
                      OutlinedButton.icon(
                        style: OutlinedButton.styleFrom(side: const BorderSide(color: Colors.greenAccent)),
                        icon: const Icon(Icons.image, color: Colors.greenAccent),
                        label: const Text("Upload Gallery", style: TextStyle(color: Colors.greenAccent)),
                        onPressed: isScanning ? null : _runMockScan,
                      ),
                    ],
                  )
                ],
              ),
            ),

            if (isScanning) ...[
              const SizedBox(height: 30),
              const Center(
                child: Column(
                  children: [
                    CircularProgressIndicator(color: Colors.greenAccent),
                    SizedBox(height: 12),
                    Text("PyTorch Computer Vision AI Analyzing Plant Leaf...", style: TextStyle(color: Colors.greenAccent)),
                  ],
                ),
              )
            ],

            // Display Results
            if (scanResult != null && !isScanning) ...[
              const SizedBox(height: 24),
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: const Color(0xFF1E293B),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: Colors.amberAccent),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text("${scanResult!['crop']} Diagnosis", style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                          decoration: BoxDecoration(
                            color: Colors.amber.shade800,
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Text("Confidence: ${scanResult!['confidence']}%", style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold)),
                        )
                      ],
                    ),
                    const Divider(color: Colors.white24, height: 20),
                    _rowDetail("Detected Issue:", scanResult!['disease_detected'], Colors.amberAccent),
                    _rowDetail("Health Status:", scanResult!['health_status'], Colors.redAccent),
                    _rowDetail("Symptoms:", scanResult!['symptoms'], Colors.white70),
                    const SizedBox(height: 12),
                    const Text("Suggested Remedial Actions:", style: TextStyle(color: Colors.greenAccent, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 6),
                    ...List<String>.from(scanResult!['suggested_actions']).map((act) => Padding(
                          padding: const EdgeInsets.only(bottom: 4),
                          child: Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Text("• ", style: TextStyle(color: Colors.greenAccent, fontWeight: FontWeight.bold)),
                              Expanded(child: Text(act, style: const TextStyle(color: Colors.white, fontSize: 13))),
                            ],
                          ),
                        )),
                    const SizedBox(height: 12),
                    _rowDetail("Chemical Remedy:", scanResult!['chemical_treatment'], Colors.white),
                    _rowDetail("Organic Remedy:", scanResult!['organic_treatment'], Colors.greenAccent),
                  ],
                ),
              )
            ]
          ],
        ),
      ),
    );
  }

  Widget _rowDetail(String label, String value, Color valColor) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 6),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(width: 130, child: Text(label, style: const TextStyle(color: Colors.white60, fontSize: 13, fontWeight: FontWeight.bold))),
          Expanded(child: Text(value, style: TextStyle(color: valColor, fontSize: 13, fontWeight: FontWeight.w500))),
        ],
      ),
    );
  }
}
