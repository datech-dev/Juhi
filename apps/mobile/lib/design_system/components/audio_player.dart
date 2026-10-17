import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import '../tokens/colors.dart';
import '../tokens/radii.dart';

class AudioMessagePlayer extends StatefulWidget {
  final String? audioBase64;
  final double durationSeconds;
  final bool isUser;

  const AudioMessagePlayer({
    super.key,
    this.audioBase64,
    this.durationSeconds = 3.0,
    this.isUser = false,
  });

  @override
  State<AudioMessagePlayer> createState() => _AudioMessagePlayerState();
}

class _AudioMessagePlayerState extends State<AudioMessagePlayer>
    with SingleTickerProviderStateMixin {
  bool _isPlaying = false;
  late AnimationController _waveController;
  Timer? _playbackTimer;

  @override
  void initState() {
    super.initState();
    _waveController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 600),
    );
  }

  @override
  void dispose() {
    _playbackTimer?.cancel();
    _waveController.dispose();
    super.dispose();
  }

  void _togglePlayback() {
    _playbackTimer?.cancel();
    setState(() {
      _isPlaying = !_isPlaying;
      if (_isPlaying) {
        _waveController.repeat(reverse: true);
      } else {
        _waveController.stop();
      }
    });

    if (_isPlaying) {
      _playbackTimer = Timer(
        Duration(milliseconds: (widget.durationSeconds * 1000).toInt()),
        () {
          if (mounted) {
            setState(() {
              _isPlaying = false;
              _waveController.stop();
            });
          }
        },
      );
    }
  }

  String _formatDuration(double seconds) {
    final int mins = seconds ~/ 60;
    final int secs = (seconds % 60).toInt();
    return '$mins:${secs.toString().padLeft(2, '0')}';
  }

  @override
  Widget build(BuildContext context) {
    final primaryColor = widget.isUser ? Colors.white : JuhiColors.lavender500;
    final secondaryColor = widget.isUser ? Colors.white70 : Colors.grey;

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: widget.isUser
            ? Colors.white.withValues(alpha: 0.15)
            : JuhiColors.lavender500.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(JuhiRadius.md),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Play/Pause button
          GestureDetector(
            onTap: _togglePlayback,
            child: Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                color: primaryColor,
                shape: BoxShape.circle,
              ),
              child: Icon(
                _isPlaying ? Icons.pause_rounded : Icons.play_arrow_rounded,
                color: widget.isUser ? JuhiColors.userBubbleDark : Colors.white,
                size: 20,
              ),
            ),
          ),
          const SizedBox(width: 10),

          // Animated Waveform
          AnimatedBuilder(
            animation: _waveController,
            builder: (context, _) {
              return Row(
                children: List.generate(8, (i) {
                  final randomFactor = sin((i + 1) * 0.8 + (_isPlaying ? _waveController.value * 4 : 0)).abs();
                  final height = _isPlaying ? (8.0 + randomFactor * 14.0) : 8.0;
                  return Container(
                    margin: const EdgeInsets.symmetric(horizontal: 1.5),
                    width: 3,
                    height: height,
                    decoration: BoxDecoration(
                      color: _isPlaying ? primaryColor : secondaryColor.withValues(alpha: 0.5),
                      borderRadius: BorderRadius.circular(2),
                    ),
                  );
                }),
              );
            },
          ),
          const SizedBox(width: 10),

          // Duration Label
          Text(
            _formatDuration(widget.durationSeconds),
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w600,
              color: secondaryColor,
            ),
          ),
        ],
      ),
    );
  }
}
