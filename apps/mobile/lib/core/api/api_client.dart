import 'dart:convert';
import 'package:http/http.dart' as http;
import 'api_error.dart';

class JuhiApiClient {
  final String baseUrl;
  String? _authToken;

  JuhiApiClient({
    this.baseUrl = "http://localhost:8000/api/v1",
    String? initialToken,
  }) : _authToken = initialToken;

  void setAuthToken(String token) {
    _authToken = token;
  }

  Map<String, String> _buildHeaders() {
    final headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
    if (_authToken != null) {
      headers['Authorization'] = 'Bearer $_authToken';
    }
    return headers;
  }

  Future<Map<String, dynamic>> syncUser() async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/sync'),
      headers: _buildHeaders(),
    );
    return _handleResponse(response);
  }

  Future<List<dynamic>> getConversations() async {
    final response = await http.get(
      Uri.parse('$baseUrl/conversations'),
      headers: _buildHeaders(),
    );
    final data = _handleResponse(response);
    if (data is List) return data;
    return (data as Map<String, dynamic>)['items'] ?? [];
  }

  Future<Map<String, dynamic>> createConversation({String? title}) async {
    final response = await http.post(
      Uri.parse('$baseUrl/conversations'),
      headers: _buildHeaders(),
      body: jsonEncode({'title': title ?? 'Chat with Juhi'}),
    );
    return _handleResponse(response);
  }

  Future<List<dynamic>> getMessages(String conversationId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/conversations/$conversationId/messages'),
      headers: _buildHeaders(),
    );
    final dynamic data = _handleResponse(response);
    if (data is List) return data;
    return [];
  }

  Future<Map<String, dynamic>> sendMessage({
    required String conversationId,
    required String text,
    required String idempotencyKey,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/conversations/$conversationId/messages'),
      headers: _buildHeaders(),
      body: jsonEncode({
        'text': text,
        'idempotency_key': idempotencyKey,
      }),
    );
    return _handleResponse(response);
  }

  Future<Map<String, dynamic>> generateImage({
    required String prompt,
    String? conversationId,
    String? model,
    int? width,
    int? height,
    String? idempotencyKey,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/images/generate'),
      headers: _buildHeaders(),
      body: jsonEncode({
        'prompt': prompt,
        if (conversationId != null) 'conversation_id': conversationId,
        'model': model ?? 'fluently-xl',
        'width': width ?? 1024,
        'height': height ?? 1024,
        if (idempotencyKey != null) 'idempotency_key': idempotencyKey,
      }),
    );
    return _handleResponse(response);
  }

  Future<Map<String, dynamic>> getJobStatus(String jobId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/jobs/$jobId'),
      headers: _buildHeaders(),
    );
    return _handleResponse(response);
  }

  Future<Map<String, dynamic>> getMediaAsset(String assetId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/media/$assetId'),
      headers: _buildHeaders(),
    );
    return _handleResponse(response);
  }

  Future<List<dynamic>> listMediaAssets() async {
    final response = await http.get(
      Uri.parse('$baseUrl/media'),
      headers: _buildHeaders(),
    );
    final data = _handleResponse(response);
    if (data is List) return data;
    return [];
  }

  Future<Map<String, dynamic>> getDefaultCompanion() async {
    final response = await http.get(
      Uri.parse('$baseUrl/companions/default'),
      headers: _buildHeaders(),
    );
    return _handleResponse(response);
  }

  Future<Map<String, dynamic>> updateCompanionProfile({
    required String id,
    String? displayName,
    String? relationshipMode,
    String? companionGenderPresentation,
    Map<String, dynamic>? personalityOverrides,
  }) async {
    final response = await http.put(
      Uri.parse('$baseUrl/companions/$id'),
      headers: _buildHeaders(),
      body: jsonEncode({
        if (displayName != null) 'display_name': displayName,
        if (relationshipMode != null) 'relationship_mode': relationshipMode,
        if (companionGenderPresentation != null)
          'companion_gender_presentation': companionGenderPresentation,
        if (personalityOverrides != null)
          'personality_overrides': personalityOverrides,
      }),
    );
    return _handleResponse(response);
  }

  Future<List<dynamic>> getMemories({String? search}) async {
    final uri = Uri.parse('$baseUrl/memory').replace(
      queryParameters:
          search != null && search.isNotEmpty ? {'q': search} : null,
    );
    final response = await http.get(uri, headers: _buildHeaders());
    final data = _handleResponse(response);
    if (data is List) return data;
    return [];
  }

  Future<Map<String, dynamic>> createMemory({
    required String contentText,
    String memoryType = 'profile_fact',
    int importance = 3,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/memory'),
      headers: _buildHeaders(),
      body: jsonEncode({
        'content_text': contentText,
        'memory_type': memoryType,
        'importance': importance,
      }),
    );
    return _handleResponse(response);
  }

  Future<void> deleteMemory(String id) async {
    final response = await http.delete(
      Uri.parse('$baseUrl/memory/$id'),
      headers: _buildHeaders(),
    );
    _handleResponse(response);
  }

  Future<void> clearAllMemories() async {
    final response = await http.delete(
      Uri.parse('$baseUrl/memory'),
      headers: _buildHeaders(),
    );
    _handleResponse(response);
  }

  Future<Map<String, dynamic>> recordConsent({
    required String purpose,
    String decision = 'granted',
    String noticeVersion = 'v1.0',
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/users/me/consent'),
      headers: _buildHeaders(),
      body: jsonEncode({
        'purpose': purpose,
        'decision': decision,
        'notice_version': noticeVersion,
      }),
    );
    return _handleResponse(response);
  }

  Future<Map<String, dynamic>> getCreditBalance() async {
    final response = await http.get(
      Uri.parse('$baseUrl/billing/balance'),
      headers: _buildHeaders(),
    );
    return _handleResponse(response);
  }

  Future<List<dynamic>> getCreditLedger({int limit = 50}) async {
    final response = await http.get(
      Uri.parse('$baseUrl/billing/ledger?limit=$limit'),
      headers: _buildHeaders(),
    );
    final data = _handleResponse(response);
    return data is List ? data : [];
  }

  Future<Map<String, dynamic>> createStoryConversation({
    required String scenarioKey,
    String? title,
    String? scenarioPrompt,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/conversations/story'),
      headers: _buildHeaders(),
      body: jsonEncode({
        'scenario_key': scenarioKey,
        if (title != null) 'title': title,
        if (scenarioPrompt != null) 'scenario_prompt': scenarioPrompt,
      }),
    );
    return _handleResponse(response);
  }

  Future<Map<String, dynamic>> exportUserData() async {
    final response = await http.get(
      Uri.parse('$baseUrl/users/me/export'),
      headers: _buildHeaders(),
    );
    return _handleResponse(response);
  }

  Future<Map<String, dynamic>> deleteAccount() async {
    final response = await http.delete(
      Uri.parse('$baseUrl/users/me'),
      headers: _buildHeaders(),
    );
    return _handleResponse(response);
  }

  Future<Map<String, dynamic>> synthesizeSpeech({
    required String text,
    String voiceId = 'juhi-warm',
    double speed = 1.0,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/audio/speak'),
      headers: _buildHeaders(),
      body: jsonEncode({
        'text': text,
        'voice_id': voiceId,
        'speed': speed,
      }),
    );
    return _handleResponse(response);
  }

  Future<Map<String, dynamic>> speakMessage({
    required String conversationId,
    required String messageId,
    String voiceId = 'juhi-warm',
    double speed = 1.0,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/audio/conversations/$conversationId/messages/$messageId/speak'),
      headers: _buildHeaders(),
      body: jsonEncode({
        'voice_id': voiceId,
        'speed': speed,
      }),
    );
    return _handleResponse(response);
  }

  dynamic _handleResponse(http.Response response) {
    final dynamic decoded = jsonDecode(utf8.decode(response.bodyBytes));
    if (response.statusCode >= 200 && response.statusCode < 300) {
      return decoded;
    } else {
      if (decoded is Map<String, dynamic>) {
        throw JuhiApiError.fromJson(decoded);
      }
      throw JuhiApiError(
        code: 'HTTP_${response.statusCode}',
        message: 'Request failed with status: ${response.statusCode}',
      );
    }
  }
}
