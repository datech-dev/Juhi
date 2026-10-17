import 'package:flutter/material.dart';

/// Design tokens for Juhi "Warm Modern Companion" color palette
/// Ref: docs/DESIGN_SYSTEM.md Section 3
class JuhiColors {
  JuhiColors._();

  // Primitive Plum Palette
  static const Color plum950 = Color(0xFF24142F);
  static const Color plum900 = Color(0xFF321B43);
  static const Color plum800 = Color(0xFF48265D);
  static const Color plum700 = Color(0xFF60337A);

  // Primitive Lavender Accent Palette
  static const Color lavender600 = Color(0xFF8358C7);
  static const Color lavender500 = Color(0xFF9A72DE);
  static const Color lavender400 = Color(0xFFAF8DF2);
  static const Color lavender100 = Color(0xFFE9E0FA);

  // Primitive Rose Accent Palette
  static const Color rose500 = Color(0xFFE87A90);
  static const Color rose400 = Color(0xFFF296A9);
  static const Color rose100 = Color(0xFFFDE8EC);

  // Semantic Surfaces - Dark Mode (Primary)
  static const Color surfaceDark = Color(0xFF191024);
  static const Color surfaceDarkCard = Color(0xFF29183B);
  static const Color surfaceDarkElevated = Color(0xFF3A2352);

  // Semantic Surfaces - Light Mode
  static const Color surfaceLight = Color(0xFFFBF9FC);
  static const Color surfaceLightCard = Color(0xFFFFFFFF);
  static const Color surfaceLightElevated = Color(0xFFF2ECF7);

  // Text Colors
  static const Color textDarkPrimary = Color(0xFFF5EEFA);
  static const Color textDarkSecondary = Color(0xFFC7B8D6);
  static const Color textDarkMuted = Color(0xFFA695B5);

  static const Color textLightPrimary = Color(0xFF1E1226);
  static const Color textLightSecondary = Color(0xFF5A496B);
  static const Color textLightMuted = Color(0xFF877499);

  // Chat Bubble Colors
  static const Color userBubbleDark = Color(0xFF8358C7);
  static const Color companionBubbleDark = Color(0xFF2E1A42);

  static const Color userBubbleLight = Color(0xFF9A72DE);
  static const Color companionBubbleLight = Color(0xFFF0E8F8);
}
