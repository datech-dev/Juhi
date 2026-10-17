import 'package:flutter/material.dart';
import '../core/api/api_client.dart';
import '../design_system/theme/app_theme.dart';
import '../features/chat/presentation/chat_screen.dart';

class JuhiApp extends StatelessWidget {
  final JuhiApiClient apiClient;

  const JuhiApp({super.key, required this.apiClient});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Juhi AI Companion',
      debugShowCheckedModeBanner: false,
      theme: JuhiTheme.lightTheme,
      darkTheme: JuhiTheme.darkTheme,
      themeMode: ThemeMode.dark, // Default to Dark Plum theme per design system
      home: ChatScreen(apiClient: apiClient),
    );
  }
}
