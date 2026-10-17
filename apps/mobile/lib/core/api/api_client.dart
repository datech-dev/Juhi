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
