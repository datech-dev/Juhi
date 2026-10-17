import 'package:flutter/material.dart';

class JuhiSpacing {
  JuhiSpacing._();

  static const double xxs = 4.0;
  static const double xs = 8.0;
  static const double sm = 12.0;
  static const double md = 16.0;
  static const double lg = 24.0;
  static const double xl = 32.0;
  static const double xxl = 48.0;
}

class JuhiRadius {
  JuhiRadius._();

  static const double sm = 8.0;
  static const double md = 16.0;
  static const double lg = 24.0;
  static const double pill = 999.0;

  static const BorderRadius smRadius = BorderRadius.all(Radius.circular(sm));
  static const BorderRadius mdRadius = BorderRadius.all(Radius.circular(md));
  static const BorderRadius lgRadius = BorderRadius.all(Radius.circular(lg));
  static const BorderRadius pillRadius = BorderRadius.all(Radius.circular(pill));
}
