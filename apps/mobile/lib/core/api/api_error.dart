class JuhiApiError implements Exception {
  final String code;
  final String message;
  final Map<String, dynamic>? details;

  JuhiApiError({
    required this.code,
    required this.message,
    this.details,
  });

  factory JuhiApiError.fromJson(Map<String, dynamic> json) {
    final error = json['error'] as Map<String, dynamic>?;
    return JuhiApiError(
      code: error?['code'] as String? ?? 'UNKNOWN_ERROR',
      message: error?['message'] as String? ?? 'An unexpected error occurred.',
      details: error?['details'] as Map<String, dynamic>?,
    );
  }

  @override
  String toString() => 'JuhiApiError($code): $message';
}
