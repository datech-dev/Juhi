import 'package:flutter/material.dart';
import '../tokens/colors.dart';

class CompanionAvatar extends StatelessWidget {
  final String name;
  final double size;
  final bool isOnline;

  const CompanionAvatar({
    super.key,
    required this.name,
    this.size = 40.0,
    this.isOnline = true,
  });

  @override
  Widget build(BuildContext context) {
    final initial = name.isNotEmpty ? name[0].toUpperCase() : 'J';

    return Stack(
      children: [
        Container(
          width: size,
          height: size,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            gradient: const LinearGradient(
              colors: [JuhiColors.lavender500, JuhiColors.rose500],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
            boxShadow: [
              BoxShadow(
                color: JuhiColors.lavender500.withValues(alpha: 0.3),
                blurRadius: 8,
                offset: const Offset(0, 2),
              ),
            ],
          ),
          child: Center(
            child: Text(
              initial,
              style: TextStyle(
                color: Colors.white,
                fontWeight: FontWeight.bold,
                fontSize: size * 0.45,
              ),
            ),
          ),
        ),
        if (isOnline)
          Positioned(
            right: 0,
            bottom: 0,
            child: Container(
              width: size * 0.28,
              height: size * 0.28,
              decoration: BoxDecoration(
                color: const Color(0xFF4CAF50),
                shape: BoxShape.circle,
                border: Border.all(
                  color: Theme.of(context).scaffoldBackgroundColor,
                  width: 2,
                ),
              ),
            ),
          ),
      ],
    );
  }
}
