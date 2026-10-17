import 'package:flutter/material.dart';
import '../tokens/colors.dart';
import '../tokens/spacing.dart';

class JuhiTheme {
  JuhiTheme._();

  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      scaffoldBackgroundColor: JuhiColors.surfaceDark,
      primaryColor: JuhiColors.lavender500,
      colorScheme: const ColorScheme.dark(
        primary: JuhiColors.lavender500,
        secondary: JuhiColors.rose500,
        surface: JuhiColors.surfaceDark,
        onSurface: JuhiColors.textDarkPrimary,
        onPrimary: Colors.white,
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: JuhiColors.surfaceDark,
        foregroundColor: JuhiColors.textDarkPrimary,
        elevation: 0,
        centerTitle: false,
      ),
      cardTheme: const CardThemeData(
        color: JuhiColors.surfaceDarkCard,
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: JuhiRadius.mdRadius,
        ),
      ),
      textTheme: const TextTheme(
        headlineMedium: TextStyle(
          color: JuhiColors.textDarkPrimary,
          fontWeight: FontWeight.w600,
          fontSize: 24,
        ),
        titleLarge: TextStyle(
          color: JuhiColors.textDarkPrimary,
          fontWeight: FontWeight.w600,
          fontSize: 18,
        ),
        bodyLarge: TextStyle(
          color: JuhiColors.textDarkPrimary,
          fontSize: 16,
          height: 1.4,
        ),
        bodyMedium: TextStyle(
          color: JuhiColors.textDarkSecondary,
          fontSize: 14,
          height: 1.4,
        ),
        bodySmall: TextStyle(
          color: JuhiColors.textDarkMuted,
          fontSize: 12,
        ),
      ),
    );
  }

  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      scaffoldBackgroundColor: JuhiColors.surfaceLight,
      primaryColor: JuhiColors.lavender600,
      colorScheme: const ColorScheme.light(
        primary: JuhiColors.lavender600,
        secondary: JuhiColors.rose500,
        surface: JuhiColors.surfaceLight,
        onSurface: JuhiColors.textLightPrimary,
        onPrimary: Colors.white,
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: JuhiColors.surfaceLight,
        foregroundColor: JuhiColors.textLightPrimary,
        elevation: 0,
        centerTitle: false,
      ),
      cardTheme: const CardThemeData(
        color: JuhiColors.surfaceLightCard,
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: JuhiRadius.mdRadius,
        ),
      ),
      textTheme: const TextTheme(
        headlineMedium: TextStyle(
          color: JuhiColors.textLightPrimary,
          fontWeight: FontWeight.w600,
          fontSize: 24,
        ),
        titleLarge: TextStyle(
          color: JuhiColors.textLightPrimary,
          fontWeight: FontWeight.w600,
          fontSize: 18,
        ),
        bodyLarge: TextStyle(
          color: JuhiColors.textLightPrimary,
          fontSize: 16,
          height: 1.4,
        ),
        bodyMedium: TextStyle(
          color: JuhiColors.textLightSecondary,
          fontSize: 14,
          height: 1.4,
        ),
        bodySmall: TextStyle(
          color: JuhiColors.textLightMuted,
          fontSize: 12,
        ),
      ),
    );
  }
}
