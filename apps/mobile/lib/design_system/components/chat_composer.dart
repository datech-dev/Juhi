import 'package:flutter/material.dart';
import '../tokens/colors.dart';
import '../tokens/spacing.dart';

class ChatComposer extends StatefulWidget {
  final Function(String text) onSend;
  final VoidCallback? onVoiceTap;
  final bool isSending;

  const ChatComposer({
    super.key,
    required this.onSend,
    this.onVoiceTap,
    this.isSending = false,
  });

  @override
  State<ChatComposer> createState() => _ChatComposerState();
}

class _ChatComposerState extends State<ChatComposer> {
  final TextEditingController _controller = TextEditingController();
  bool _canSend = false;

  @override
  void initState() {
    super.initState();
    _controller.addListener(() {
      final canSend = _controller.text.trim().isNotEmpty;
      if (canSend != _canSend) {
        setState(() {
          _canSend = canSend;
        });
      }
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _handleSend() {
    final text = _controller.text.trim();
    if (text.isNotEmpty && !widget.isSending) {
      widget.onSend(text);
      _controller.clear();
    }
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: JuhiSpacing.md,
        vertical: JuhiSpacing.xs,
      ),
      decoration: BoxDecoration(
        color: isDark ? JuhiColors.surfaceDarkCard : JuhiColors.surfaceLightCard,
        border: Border(
          top: BorderSide(
            color: isDark
                ? JuhiColors.plum800.withValues(alpha: 0.3)
                : JuhiColors.lavender100.withValues(alpha: 0.5),
            width: 1,
          ),
        ),
      ),
      child: SafeArea(
        child: Row(
          children: [
            Expanded(
              child: Container(
                decoration: BoxDecoration(
                  color: isDark
                      ? JuhiColors.surfaceDarkElevated
                      : JuhiColors.surfaceLightElevated,
                  borderRadius: BorderRadius.circular(JuhiRadius.pill),
                ),
                padding: const EdgeInsets.symmetric(horizontal: JuhiSpacing.md),
                child: TextField(
                  controller: _controller,
                  textCapitalization: TextCapitalization.sentences,
                  minLines: 1,
                  maxLines: 4,
                  decoration: const InputDecoration(
                    hintText: "Message Juhi... (Type in English, Hindi, Tamil...)",
                    hintStyle: TextStyle(
                      fontSize: 14,
                      color: JuhiColors.textDarkMuted,
                    ),
                    border: InputBorder.none,
                    isDense: true,
                    contentPadding: EdgeInsets.symmetric(vertical: 12),
                  ),
                  onSubmitted: (_) => _handleSend(),
                ),
              ),
            ),
            const SizedBox(width: JuhiSpacing.xs),
            IconButton(
              icon: widget.isSending
                  ? const SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : Icon(
                      _canSend ? Icons.send_rounded : Icons.mic_rounded,
                      color: _canSend
                          ? JuhiColors.lavender500
                          : JuhiColors.textDarkMuted,
                    ),
              onPressed: _canSend ? _handleSend : widget.onVoiceTap,
            ),
          ],
        ),
      ),
    );
  }
}
