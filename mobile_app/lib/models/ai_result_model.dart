class AIResultModel {
  final String crop;
  final String diseaseDetected;
  final String healthStatus;
  final int confidencePercentage;
  final String cause;
  final String symptoms;
  final List<String> suggestedActions;
  final String chemicalTreatment;
  final String organicTreatment;

  AIResultModel({
    required this.crop,
    required this.diseaseDetected,
    required this.healthStatus,
    required this.confidencePercentage,
    required this.cause,
    required this.symptoms,
    required this.suggestedActions,
    required this.chemicalTreatment,
    required this.organicTreatment,
  });

  factory AIResultModel.fromJson(Map<String, dynamic> json) {
    final diag = json['diagnosis'] ?? json;
    return AIResultModel(
      crop: diag['crop'] ?? 'Unknown Crop',
      diseaseDetected: diag['disease_detected'] ?? 'Unknown',
      healthStatus: diag['health_status'] ?? 'Healthy',
      confidencePercentage: (diag['confidence_percentage'] ?? 90).toInt(),
      cause: diag['cause'] ?? '',
      symptoms: diag['symptoms'] ?? '',
      suggestedActions: List<String>.from(diag['suggested_actions'] ?? []),
      chemicalTreatment: diag['chemical_treatment'] ?? 'N/A',
      organicTreatment: diag['organic_treatment'] ?? 'N/A',
    );
  }
}
