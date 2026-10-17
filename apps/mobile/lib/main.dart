import 'package:flutter/material.dart';
import 'app/app.dart';
import 'core/api/api_client.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize API client with dev mock token by default
  final apiClient = JuhiApiClient(
    baseUrl: const String.fromEnvironment(
      'API_BASE_URL',
      defaultValue: "https://juhi.zetalink.cloud/api/v1",
    ),
    initialToken: "test-user-mobile-client",
  );

  runApp(JuhiApp(apiClient: apiClient));
}
