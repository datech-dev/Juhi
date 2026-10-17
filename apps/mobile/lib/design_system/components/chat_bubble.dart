import 'dart:convert';
import 'package:flutter/material.dart';
import '../tokens/colors.dart';
import '../tokens/spacing.dart';

class ChatBubble extends StatelessWidget {
  final String text;
  final bool isUser;
  final String? time;
  final String? imageBase64;

  const ChatBubble({
    super.key,
    required this.text,
    required this.isUser,
    this.time,
    this.imageBase64,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final backgroundColor = isUser
        ? (isDark ? JuhiColors.userBubbleDark : JuhiColors.userBubbleLight)
        : (isDark ? JuhiColors.companionBubbleDark : JuhiColors.companionBubbleLight);

    final textColor = isUser
        ? Colors.white
        : (isDark ? JuhiColors.textDarkPrimary : JuhiColors.textLightPrimary);

    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(
          horizontal: JuhiSpacing.md,
          vertical: JuhiSpacing.xs,
        ),
        padding: const EdgeInsets.symmetric(
          horizontal: JuhiSpacing.md,
          vertical: JuhiSpacing.sm,
        ),
        constraints: BoxConstraints(
          maxWidth: MediaQuery.of(context).size.width * 0.78,
        ),
        decoration: BoxDecoration(
          color: backgroundColor,
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(JuhiRadius.md),
            topRight: const Radius.circular(JuhiRadius.md),
            bottomLeft: Radius.circular(isUser ? JuhiRadius.md : 4.0),
            bottomRight: Radius.circular(isUser ? 4.0 : JuhiRadius.md),
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.04),
              blurRadius: 4,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Column(
          crossAxisAlignment:
              isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: [
            if (imageBase64 != null) ...[
              ClipRRect(
                borderRadius: BorderRadius.circular(JuhiRadius.sm),
                child: Image.memory(
                  base64Decode(imageBase64!),
                  fit: BoxFit.cover,
                  errorBuilder: (context, error, stackTrace) => Container(
                    height: 120,
                    color: Colors.black12,
                    child: const Center(
                      child: Icon(Icons.broken_image_rounded, color: Colors.grey),
                    ),
                  ),
                ),
              ),
              if (text.isNotEmpty) const SizedBox(height: 8),
            ],
            if (text.isNotEmpty)
              Text(
                text,
                style: TextStyle(
                  color: textColor,
                  fontSize: 15.0,
                  height: 1.4,
                ),
              ),
            if (time != null) ...[
              const SizedBox(height: 4),
              Text(
                time!,
                style: TextStyle(
                  color: isUser
                      ? Colors.white.withValues(alpha: 0.7)
                      : (isDark ? JuhiColors.textDarkMuted : JuhiColors.textLightMuted),
                  fontSize: 11.0,
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
