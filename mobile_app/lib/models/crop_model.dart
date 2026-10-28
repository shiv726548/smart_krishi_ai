class CropModel {
  final int id;
  final String cropName;
  final String variety;
  final String sowingDate;
  final double fieldSizeAcres;
  final String farmLocation;
  final String growthStage;
  final double targetMoistureMin;
  final double targetMoistureMax;
  final List<dynamic> schedule;
  final List<String> tips;

  CropModel({
    required this.id,
    required this.cropName,
    required this.variety,
    required this.sowingDate,
    required this.fieldSizeAcres,
    required this.farmLocation,
    required this.growthStage,
    required this.targetMoistureMin,
    required this.targetMoistureMax,
    required this.schedule,
    required this.tips,
  });

  factory CropModel.fromJson(Map<String, dynamic> json) {
    return CropModel(
      id: json['id'] ?? 0,
      cropName: json['crop_name'] ?? 'Unknown crop',
      variety: json['variety'] ?? 'Not provided',
      sowingDate: json['sowing_date'] ?? 'Not provided',
      fieldSizeAcres: (json['field_size_acres'] ?? 0.0).toDouble(),
      farmLocation: json['farm_location'] ?? 'Not provided',
      growthStage: json['growth_stage'] ?? 'Not provided',
      targetMoistureMin: (json['target_moisture_min'] ?? 40.0).toDouble(),
      targetMoistureMax: (json['target_moisture_max'] ?? 70.0).toDouble(),
      schedule: json['schedule'] ?? [],
      tips: List<String>.from(json['tips'] ?? []),
    );
  }
}
