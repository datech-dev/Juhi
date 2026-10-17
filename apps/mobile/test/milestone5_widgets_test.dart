import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:juhi_mobile/core/api/api_client.dart';
import 'package:juhi_mobile/features/account/presentation/account_screen.dart';
import 'package:juhi_mobile/features/onboarding/presentation/onboarding_dialog.dart';
import 'package:juhi_mobile/features/story/presentation/story_picker_sheet.dart';

class Milestone5MockClient extends JuhiApiClient {
  final List<String> recordedConsents = [];
  bool storyCreated = false;
  bool dataExported = false;
  bool accountDeleted = false;

  @override
  Future<Map<String, dynamic>> syncUser() async {
    return {
      'id': 'user-123',
      'display_name': 'Dhinesh',
      'age_assurance_status': 'verified_adult',
    };
  }

  @override
  Future<Map<String, dynamic>> recordConsent({
    required String purpose,
    String decision = 'granted',
    String noticeVersion = 'v1.0',
  }) async {
    recordedConsents.add(purpose);
    return {'status': 'success', 'purpose': purpose, 'decision': decision};
  }

  @override
  Future<Map<String, dynamic>> getCreditBalance() async {
    return {
      'user_id': 'user-123',
      'available_balance': 100,
      'reserved_balance': 0,
      'credit_unit': 'credits',
      'tier': 'free',
      'rate_cards': {'image_generation': 10, 'voice_minute': 5},
    };
  }

  @override
  Future<List<dynamic>> getCreditLedger({int limit = 50}) async {
    return [
      {
        'id': 'led-1',
        'credit_account_id': 'acc-1',
        'entry_type': 'grant',
        'available_delta': 100,
        'reserved_delta': 0,
        'reason': 'welcome_bonus',
        'created_at': DateTime.now().toIsoformatString(),
      },
    ];
  }

  @override
  Future<Map<String, dynamic>> createStoryConversation({
    required String scenarioKey,
    String? title,
    String? scenarioPrompt,
  }) async {
    storyCreated = true;
    return {
      'id': 'story-conv-1',
      'conversation_type': 'roleplay',
      'title': title ?? 'Story',
    };
  }

  @override
  Future<Map<String, dynamic>> exportUserData() async {
    dataExported = true;
    return {
      'user': {'id': 'user-123', 'display_name': 'Dhinesh'},
      'preferences': {'ui_language': 'en'},
      'memories': [{'content_text': 'Likes coffee'}],
      'conversations': [],
      'credits': {'available_balance': 100},
    };
  }

  @override
  Future<Map<String, dynamic>> deleteAccount() async {
    accountDeleted = true;
    return {'status': 'deleted'};
  }
}

extension DateTimeIso on DateTime {
  String toIsoformatString() => toIso8601String();
}

void main() {
  testWidgets('OnboardingDialog records AI disclosure and age consent', (WidgetTester tester) async {
    final mockClient = Milestone5MockClient();
    bool completed = false;

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: OnboardingDialog(
            apiClient: mockClient,
            onCompleted: () => completed = true,
          ),
        ),
      ),
    );

    expect(find.text('Welcome to Juhi'), findsOneWidget);
    expect(find.text('AI Companion Disclosure'), findsOneWidget);
    expect(find.text('I confirm that I am 18 years of age or older.'), findsOneWidget);

    // Button should be disabled until age is confirmed
    final buttonFinder = find.widgetWithText(FilledButton, 'Agree & Continue');
    expect(tester.widget<FilledButton>(buttonFinder).onPressed, isNull);

    // Tap checkbox
    await tester.tap(find.byType(CheckboxListTile));
    await tester.pumpAndSettle();

    // Now button is enabled
    expect(tester.widget<FilledButton>(buttonFinder).onPressed, isNotNull);

    // Tap submit
    await tester.tap(buttonFinder);
    await tester.pumpAndSettle();

    expect(mockClient.recordedConsents, contains('ai_companion_disclosure'));
    expect(mockClient.recordedConsents, contains('age_verification_18_plus'));
    expect(mockClient.recordedConsents, contains('memory_storage_consent'));
    expect(completed, isTrue);
  });

  testWidgets('StoryPickerSheet displays scenarios and initiates story session', (WidgetTester tester) async {
    final mockClient = Milestone5MockClient();
    Map<String, dynamic>? startedStory;

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: StoryPickerSheet(
            apiClient: mockClient,
            onStoryStarted: (conv) => startedStory = conv,
          ),
        ),
      ),
    );

    expect(find.text('Choose a Story Scenario'), findsOneWidget);
    expect(find.text('Rainy Cafe in Bangalore'), findsOneWidget);
    expect(find.text('Stargazing at Nandi Hills'), findsOneWidget);
    expect(find.text('Antique Mystery Bookstore'), findsOneWidget);
    expect(find.text('Orbital Space Station'), findsOneWidget);

    // Tap on Rainy Cafe scenario
    await tester.tap(find.text('Rainy Cafe in Bangalore'));
    await tester.pumpAndSettle();

    expect(mockClient.storyCreated, isTrue);
    expect(startedStory?['id'], equals('story-conv-1'));
  });

  testWidgets('AccountScreen displays wallet balance, ledger, and data export action', (WidgetTester tester) async {
    final mockClient = Milestone5MockClient();

    await tester.pumpWidget(
      MaterialApp(
        home: AccountScreen(apiClient: mockClient),
      ),
    );

    await tester.pumpAndSettle();

    expect(find.text('Hi, Dhinesh'), findsOneWidget);
    expect(find.text('100'), findsOneWidget);
    expect(find.text('Juhi Credits Wallet'), findsOneWidget);
    expect(find.text('Credit Activity History'), findsOneWidget);
    expect(find.text('+100 credits'), findsOneWidget);
    expect(find.text('Export My Data'), findsOneWidget);
    expect(find.text('Delete Account Forever'), findsOneWidget);

    // Tap Export My Data
    await tester.tap(find.text('Export My Data'));
    await tester.pumpAndSettle();

    expect(mockClient.dataExported, isTrue);
    expect(find.text('Data Export Ready'), findsOneWidget);
  });
}
