class AIResultModel {
  final bool available;
  final String crop;
  final String? diseaseDetected;
  final String healthStatus;
  final int? confidencePercentage;
  final String? cause;
  final String? symptoms;
  final List<String> suggestedActions;
  final String? chemicalTreatment;
  final String? organicTreatment;
  final String message;

  AIResultModel({
    required this.available,
    required this.crop,
    required this.diseaseDetected,
    required this.healthStatus,
    required this.confidencePercentage,
    required this.cause,
    required this.symptoms,
    required this.suggestedActions,
    required this.chemicalTreatment,
    required this.organicTreatment,
    required this.message,
  });

  factory AIResultModel.fromJson(Map<String, dynamic> json) {
    final diag = (json['diagnosis'] ?? json) as Map<String, dynamic>;
    final confidence = diag['confidence_percentage'];
    return AIResultModel(
      available: diag['available'] == true,
      crop: diag['crop'] ?? 'Unknown Crop',
      diseaseDetected: diag['disease_detected'] as String?,
      healthStatus: diag['health_status'] ?? 'Unavailable',
      confidencePercentage: confidence is num ? confidence.toInt() : null,
      cause: diag['cause'] as String?,
      symptoms: diag['symptoms'] as String?,
      suggestedActions: List<String>.from(diag['suggested_actions'] ?? []),
      chemicalTreatment: diag['chemical_treatment'] as String?,
      organicTreatment: diag['organic_treatment'] as String?,
      message: diag['message'] ?? 'No diagnosis was generated.',
    );
  }
}
