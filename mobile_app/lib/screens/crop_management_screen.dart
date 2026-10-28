import 'package:flutter/material.dart';

import '../models/crop_model.dart';
import '../services/api_service.dart';

class CropManagementScreen extends StatefulWidget {
  const CropManagementScreen({Key? key}) : super(key: key);

  @override
  _CropManagementScreenState createState() => _CropManagementScreenState();
}

class _CropManagementScreenState extends State<CropManagementScreen> {
  List<CropModel> _crops = [];
  bool _isLoading = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _loadCrops();
  }

  Future<void> _loadCrops() async {
    final userId = ApiService.currentUserId;
    if (userId == null) {
      if (mounted) {
        setState(() {
          _isLoading = false;
          _errorMessage = 'Sign in to view your saved crops.';
        });
      }
      return;
    }
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });
    final crops = await ApiService.fetchUserCrops(userId);
    if (!mounted) return;
    setState(() {
      if (crops == null) {
        _errorMessage = 'Could not load your crops. Check your connection and sign-in.';
      } else {
        _crops = crops;
      }
      _isLoading = false;
    });
  }

  Future<void> _showAddCropDialog() async {
    String cropName = 'Tomato';
    String growthStage = 'Seedling';
    String? formError;
    final varietyController = TextEditingController();
    final dateController = TextEditingController(
      text: DateTime.now().toIso8601String().split('T').first,
    );
    final areaController = TextEditingController();
    final locationController = TextEditingController();

    final added = await showDialog<bool>(
      context: context,
      builder: (dialogContext) => StatefulBuilder(
        builder: (context, setDialogState) => AlertDialog(
          backgroundColor: const Color(0xFF1E293B),
          title: const Text(
            'Add crop profile',
            style: TextStyle(color: Colors.white),
          ),
          content: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                DropdownButtonFormField<String>(
                  value: cropName,
                  decoration: const InputDecoration(labelText: 'Crop'),
                  items: const ['Tomato', 'Potato', 'Rice', 'Wheat', 'Cotton', 'Corn']
                      .map((name) => DropdownMenuItem(
                            value: name,
                            child: Text(name),
                          ))
                      .toList(),
                  onChanged: (value) {
                    if (value != null) setDialogState(() => cropName = value);
                  },
                ),
                TextField(
                  controller: varietyController,
                  decoration: const InputDecoration(labelText: 'Variety'),
                ),
                TextField(
                  controller: dateController,
                  keyboardType: TextInputType.datetime,
                  decoration: const InputDecoration(
                    labelText: 'Sowing date (YYYY-MM-DD)',
                  ),
                ),
                TextField(
                  controller: areaController,
                  keyboardType: const TextInputType.numberWithOptions(decimal: true),
                  decoration: const InputDecoration(labelText: 'Field size (acres)'),
                ),
                TextField(
                  controller: locationController,
                  decoration: const InputDecoration(labelText: 'Farm location / field'),
                ),
                DropdownButtonFormField<String>(
                  value: growthStage,
                  decoration: const InputDecoration(labelText: 'Growth stage'),
                  items: const [
                    'Seedling',
                    'Vegetative',
                    'Flowering',
                    'Fruiting',
                    'Harvest',
                  ]
                      .map((stage) => DropdownMenuItem(
                            value: stage,
                            child: Text(stage),
                          ))
                      .toList(),
                  onChanged: (value) {
                    if (value != null) setDialogState(() => growthStage = value);
                  },
                ),
                if (formError != null) ...[
                  const SizedBox(height: 8),
                  Text(formError!, style: const TextStyle(color: Colors.redAccent)),
                ],
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(dialogContext, false),
              child: const Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () async {
                final acres = double.tryParse(areaController.text);
                final date = DateTime.tryParse(dateController.text);
                if (acres == null || acres <= 0 || date == null) {
                  setDialogState(() {
                    formError = 'Enter a valid date and a field size greater than zero.';
                  });
                  return;
                }
                final success = await ApiService.addCrop(
                  cropName: cropName,
                  variety: varietyController.text.trim(),
                  sowingDate: dateController.text.trim(),
                  fieldSizeAcres: acres,
                  farmLocation: locationController.text.trim(),
                  growthStage: growthStage,
                );
                if (success && dialogContext.mounted) {
                  Navigator.pop(dialogContext, true);
                } else {
                  setDialogState(() {
                    formError = 'Could not save this crop. Check sign-in and backend status.';
                  });
                }
              },
              child: const Text('Save crop'),
            ),
          ],
        ),
      ),
    );

    varietyController.dispose();
    dateController.dispose();
    areaController.dispose();
    locationController.dispose();
    if (added == true) await _loadCrops();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1E293B),
        title: const Text('Crop Management', style: TextStyle(color: Colors.white)),
        actions: [
          IconButton(
            tooltip: 'Refresh crops',
            onPressed: _isLoading ? null : _loadCrops,
            icon: const Icon(Icons.refresh),
          ),
          IconButton(
            tooltip: 'Add crop',
            icon: const Icon(Icons.add_circle, color: Colors.greenAccent, size: 28),
            onPressed: _showAddCropDialog,
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator(color: Colors.greenAccent))
          : _errorMessage != null
              ? Center(
                  child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: Text(
                      _errorMessage!,
                      textAlign: TextAlign.center,
                      style: const TextStyle(color: Colors.white70),
                    ),
                  ),
                )
              : _crops.isEmpty
                  ? Center(
                      child: Padding(
                        padding: const EdgeInsets.all(24),
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            const Icon(Icons.grass, size: 54, color: Colors.greenAccent),
                            const SizedBox(height: 12),
                            const Text(
                              'No crop profiles saved yet.',
                              style: TextStyle(color: Colors.white, fontSize: 16),
                            ),
                            const SizedBox(height: 12),
                            ElevatedButton.icon(
                              onPressed: _showAddCropDialog,
                              icon: const Icon(Icons.add),
                              label: const Text('Add a crop'),
                            ),
                          ],
                        ),
                      ),
                    )
                  : RefreshIndicator(
                      onRefresh: _loadCrops,
                      child: ListView.builder(
                        padding: const EdgeInsets.all(16),
                        itemCount: _crops.length,
                        itemBuilder: (context, index) => _cropCard(_crops[index]),
                      ),
                    ),
    );
  }

  Widget _cropCard(CropModel crop) {
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
              Expanded(
                child: Text(
                  crop.cropName,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              Text(crop.growthStage, style: const TextStyle(color: Colors.greenAccent)),
            ],
          ),
          const Divider(color: Colors.white10, height: 20),
          _cropMetaRow('Variety', crop.variety),
          _cropMetaRow('Sowing date', crop.sowingDate),
          _cropMetaRow('Field', crop.farmLocation),
          _cropMetaRow('Field size', '${crop.fieldSizeAcres} acres'),
          _cropMetaRow(
            'Default moisture range',
            '${crop.targetMoistureMin}%–${crop.targetMoistureMax}%',
          ),
          if (crop.schedule.isNotEmpty) ...[
            const SizedBox(height: 12),
            const Text(
              'Generic planning prompts — confirm locally',
              style: TextStyle(
                color: Colors.greenAccent,
                fontWeight: FontWeight.bold,
              ),
            ),
            ...crop.schedule.take(4).map((item) {
              final task = item is Map ? item['task']?.toString() : null;
              final day = item is Map ? item['day']?.toString() : null;
              return Text(
                '• ${day ?? ''}: ${task ?? ''}',
                style: const TextStyle(color: Colors.white70, fontSize: 12),
              );
            }),
          ],
        ],
      ),
    );
  }

  Widget _cropMetaRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 4),
      child: Row(
        children: [
          SizedBox(
            width: 120,
            child: Text(
              '$label:',
              style: const TextStyle(color: Colors.white54, fontSize: 13),
            ),
          ),
          Expanded(
            child: Text(
              value,
              style: const TextStyle(color: Colors.white, fontSize: 13),
            ),
          ),
        ],
      ),
    );
  }
}
