import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:juhi_mobile/design_system/components/companion_avatar.dart';
import 'package:juhi_mobile/design_system/components/chat_bubble.dart';
import 'package:juhi_mobile/design_system/components/chat_composer.dart';

void main() {
  testWidgets('CompanionAvatar renders initial and online status', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: CompanionAvatar(name: 'Juhi', size: 40, isOnline: true),
        ),
      ),
    );

    expect(find.text('J'), findsOneWidget);
  });

  testWidgets('ChatBubble displays user and companion messages', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: Column(
            children: [
              ChatBubble(text: 'Hello Juhi!', isUser: true, time: '10:00 AM'),
              ChatBubble(text: 'Vanakkam! Kaise ho?', isUser: false, time: '10:01 AM'),
            ],
          ),
        ),
      ),
    );

    expect(find.text('Hello Juhi!'), findsOneWidget);
    expect(find.text('Vanakkam! Kaise ho?'), findsOneWidget);
    expect(find.text('10:00 AM'), findsOneWidget);
    expect(find.text('10:01 AM'), findsOneWidget);
  });

  testWidgets('ChatComposer sends message when send button tapped', (WidgetTester tester) async {
    String? sentText;

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: ChatComposer(
            onSend: (text) {
              sentText = text;
            },
          ),
        ),
      ),
    );

    // Verify hint text
    expect(find.byType(TextField), findsOneWidget);

    // Enter text
    await tester.enterText(find.byType(TextField), 'Testing message');
    await tester.pump();

    // Tap send icon
    await tester.tap(find.byIcon(Icons.send_rounded));
    await tester.pump();

    expect(sentText, equals('Testing message'));
  });

  testWidgets('ChatBubble displays image when imageBase64 is provided', (WidgetTester tester) async {
    // 1x1 transparent png in base64
    const mockB64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==';

    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: ChatBubble(
            text: 'Here is your photo!',
            isUser: false,
            time: '10:02 AM',
            imageBase64: mockB64,
          ),
        ),
      ),
    );

    expect(find.text('Here is your photo!'), findsOneWidget);
    expect(find.byType(Image), findsOneWidget);
  });
}
