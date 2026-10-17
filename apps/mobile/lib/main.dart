import 'package:flutter/material.dart';
import 'app/app.dart';
import 'core/api/api_client.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize API client with dev mock token by default
  final apiClient = JuhiApiClient(
    baseUrl: "http://localhost:8000/api/v1",
    initialToken: "test-user-mobile-client",
  );

  runApp(JuhiApp(apiClient: apiClient));
}
