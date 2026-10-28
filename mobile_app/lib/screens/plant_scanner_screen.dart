import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import '../models/ai_result_model.dart';
import '../services/api_service.dart';

class PlantScannerScreen extends StatefulWidget {
  const PlantScannerScreen({Key? key}) : super(key: key);

  @override
  _PlantScannerScreenState createState() => _PlantScannerScreenState();
}

class _PlantScannerScreenState extends State<PlantScannerScreen> {
  String selectedCrop = "Tomato";
  bool isScanning = false;
  String? statusMessage;
  XFile? selectedImage;
  AIResultModel? scanResult;

  final ImagePicker _picker = ImagePicker();
  final List<String> supportedCrops = [
    "Tomato",
    "Potato",
    "Rice",
    "Wheat",
    "Cotton",
    "Corn",
  ];

  Future<void> _selectAndScan(ImageSource source) async {
    try {
      final image = await _picker.pickImage(source: source, imageQuality: 85);
      if (image == null || !mounted) return;
      setState(() {
        selectedImage = image;
        scanResult = null;
        statusMessage = null;
        isScanning = true;
      });
      final result = await ApiService.scanPlantDisease(
        image.path,
        selectedCrop,
        'en',
      );
      if (!mounted) return;
      setState(() {
        scanResult = result;
        isScanning = false;
        if (result == null) {
          statusMessage =
              'Could not reach the server. Sign in and check the backend connection.';
        } else if (!result.available) {
          statusMessage = result.message;
        }
      });
    } catch (_) {
      if (!mounted) return;
      setState(() {
        isScanning = false;
        statusMessage = 'The image could not be uploaded. Try a JPEG, PNG, or WebP under 5 MB.';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1E293B),
        title: const Text(
          "Plant Health Scanner",
          style: TextStyle(color: Colors.white),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Select crop type",
              style: TextStyle(
                color: Colors.white,
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            SizedBox(
              height: 40,
              child: ListView(
                scrollDirection: Axis.horizontal,
                children: supportedCrops.map((crop) {
                  final isSelected = crop == selectedCrop;
                  return Padding(
                    padding: const EdgeInsets.only(right: 8),
                    child: ChoiceChip(
                      label: Text(
                        crop,
                        style: TextStyle(
                          color: isSelected ? Colors.black : Colors.white,
                        ),
                      ),
                      selected: isSelected,
                      selectedColor: Colors.greenAccent,
                      backgroundColor: const Color(0xFF1E293B),
                      onSelected: (selected) {
                        if (selected) setState(() => selectedCrop = crop);
                      },
                    ),
                  );
                }).toList(),
              ),
            ),
            const SizedBox(height: 20),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(18),
              decoration: BoxDecoration(
                color: const Color(0xFF1E293B),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: Colors.greenAccent.withOpacity(0.5)),
              ),
              child: Column(
                children: [
                  if (selectedImage != null)
                    ClipRRect(
                      borderRadius: BorderRadius.circular(12),
                      child: Image.file(
                        File(selectedImage!.path),
                        height: 180,
                        width: double.infinity,
                        fit: BoxFit.cover,
                      ),
                    )
                  else
                    const Icon(
                      Icons.eco_outlined,
                      size: 56,
                      color: Colors.greenAccent,
                    ),
                  const SizedBox(height: 12),
                  const Text(
                    "Choose a leaf photo to validate the upload.",
                    style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 4),
                  const Text(
                    "JPEG, PNG, or WebP; maximum 5 MB.",
                    style: TextStyle(color: Colors.white60, fontSize: 12),
                  ),
                  const SizedBox(height: 16),
                  Wrap(
                    spacing: 10,
                    runSpacing: 8,
                    alignment: WrapAlignment.center,
                    children: [
                      ElevatedButton.icon(
                        onPressed: isScanning
                            ? null
                            : () => _selectAndScan(ImageSource.camera),
                        icon: const Icon(Icons.photo_camera),
                        label: const Text("Take photo"),
                      ),
                      OutlinedButton.icon(
                        onPressed: isScanning
                            ? null
                            : () => _selectAndScan(ImageSource.gallery),
                        icon: const Icon(Icons.image),
                        label: const Text("Choose from gallery"),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            if (isScanning) ...[
              const SizedBox(height: 22),
              const Center(
                child: Column(
                  children: [
                    CircularProgressIndicator(color: Colors.greenAccent),
                    SizedBox(height: 10),
                    Text(
                      "Validating and uploading image…",
                      style: TextStyle(color: Colors.greenAccent),
                    ),
                  ],
                ),
              ),
            ],
            if (statusMessage != null && !isScanning) ...[
              const SizedBox(height: 20),
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.amber.shade900.withOpacity(0.25),
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(color: Colors.amberAccent),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      "Diagnosis unavailable",
                      style: TextStyle(
                        color: Colors.amberAccent,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 6),
                    Text(
                      statusMessage!,
                      style: const TextStyle(color: Colors.white),
                    ),
                    const SizedBox(height: 6),
                    const Text(
                      "No disease label or confidence score was generated. Ask a local agricultural specialist if the plant is at risk.",
                      style: TextStyle(color: Colors.white70, fontSize: 12),
                    ),
                  ],
                ),
              ),
            ],
            if (scanResult?.available == true) ...[
              const SizedBox(height: 20),
              _availableResult(scanResult!),
            ],
          ],
        ),
      ),
    );
  }

  Widget _availableResult(AIResultModel result) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF1E293B),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            "${result.crop} diagnosis",
            style: const TextStyle(
              color: Colors.white,
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
          ),
          if (result.confidencePercentage != null)
            Text("Confidence: ${result.confidencePercentage}%"),
          const Divider(color: Colors.white24),
          _rowDetail("Detected issue:", result.diseaseDetected ?? "Unavailable"),
          _rowDetail("Health status:", result.healthStatus),
          if (result.symptoms != null) _rowDetail("Symptoms:", result.symptoms!),
          ...result.suggestedActions.map((action) => Text("• $action")),
        ],
      ),
    );
  }

  Widget _rowDetail(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 6),
      child: Text(
        "$label $value",
        style: const TextStyle(color: Colors.white70),
      ),
    );
  }
}
