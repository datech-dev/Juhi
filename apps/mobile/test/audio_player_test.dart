import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:juhi_mobile/design_system/components/audio_player.dart';
import 'package:juhi_mobile/design_system/components/chat_bubble.dart';

void main() {
  group('AudioMessagePlayer Component Tests', () {
    testWidgets('renders play button, waveform, and formatted duration', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: Center(
              child: AudioMessagePlayer(
                durationSeconds: 15.0,
                isUser: false,
              ),
            ),
          ),
        ),
      );

      // Verify play icon is displayed initially
      expect(find.byIcon(Icons.play_arrow_rounded), findsOneWidget);
      expect(find.text('0:15'), findsOneWidget);

      // Tap play button
      await tester.tap(find.byIcon(Icons.play_arrow_rounded));
      await tester.pump();

      // Verify now shows pause icon
      expect(find.byIcon(Icons.pause_rounded), findsOneWidget);

      // Tap pause button to stop animation before disposal
      await tester.tap(find.byIcon(Icons.pause_rounded));
      await tester.pump();
      expect(find.byIcon(Icons.play_arrow_rounded), findsOneWidget);
    });
  });

  group('ChatBubble Audio Integration Tests', () {
    testWidgets('renders speaker button when companion message has onSpeakTap and no audio', (tester) async {
      bool speakTapped = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: ChatBubble(
              text: 'Namaste! How can I help you today?',
              isUser: false,
              onSpeakTap: () {
                speakTapped = true;
              },
            ),
          ),
        ),
      );

      expect(find.text('Namaste! How can I help you today?'), findsOneWidget);
      expect(find.byIcon(Icons.volume_up_rounded), findsOneWidget);

      await tester.tap(find.byIcon(Icons.volume_up_rounded));
      await tester.pump();

      expect(speakTapped, isTrue);
    });

    testWidgets('shows loading spinner when isSpeaking is true', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: ChatBubble(
              text: 'Synthesizing voice...',
              isUser: false,
              isSpeaking: true,
            ),
          ),
        ),
      );

      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('renders AudioMessagePlayer when audioBase64 is provided', (tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: ChatBubble(
              text: 'Listen to this audio note',
              isUser: false,
              audioBase64: 'UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA=',
              durationSeconds: 8.0,
            ),
          ),
        ),
      );

      expect(find.byType(AudioMessagePlayer), findsOneWidget);
      expect(find.text('0:08'), findsOneWidget);
      expect(find.byIcon(Icons.play_arrow_rounded), findsOneWidget);
    });
  });
}
