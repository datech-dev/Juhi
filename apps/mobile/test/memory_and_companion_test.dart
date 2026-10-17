import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:juhi_mobile/core/api/api_client.dart';
import 'package:juhi_mobile/features/companion/presentation/companion_settings_screen.dart';
import 'package:juhi_mobile/features/memory/presentation/memory_screen.dart';

class MockJuhiApiClient extends JuhiApiClient {
  bool deletedMemory = false;
  bool updatedCompanion = false;

  @override
  Future<List<dynamic>> getMemories({String? search}) async {
    return [
      {
        'id': 'mem-1',
        'content_text': 'Loves filter coffee in Bangalore',
        'memory_type': 'preference',
        'importance': 4,
        'scope': 'real_life',
      },
      {
        'id': 'mem-2',
        'content_text': 'Software engineer working in tech',
        'memory_type': 'profile_fact',
        'importance': 3,
        'scope': 'real_life',
      },
    ];
  }

  @override
  Future<void> deleteMemory(String memoryId) async {
    deletedMemory = true;
  }

  @override
  Future<Map<String, dynamic>> getDefaultCompanion() async {
    return {
      'id': 'comp-1',
      'display_name': 'Juhi',
      'relationship_mode': 'girlfriend',
      'companion_gender_presentation': 'feminine',
      'personality_overrides': {'tone': 'warm and friendly'},
    };
  }

  @override
  Future<Map<String, dynamic>> updateCompanionProfile({
    required String id,
    String? displayName,
    String? relationshipMode,
    String? companionGenderPresentation,
    Map<String, dynamic>? personalityOverrides,
  }) async {
    updatedCompanion = true;
    return {
      'id': id,
      'display_name': displayName ?? 'Juhi',
      'relationship_mode': relationshipMode ?? 'girlfriend',
      'companion_gender_presentation': companionGenderPresentation ?? 'feminine',
    };
  }
}

void main() {
  testWidgets('MemoryScreen displays remembered facts and categories', (WidgetTester tester) async {
    final mockClient = MockJuhiApiClient();

    await tester.pumpWidget(
      MaterialApp(
        home: MemoryScreen(apiClient: mockClient),
      ),
    );

    // Initial loading
    expect(find.byType(CircularProgressIndicator), findsOneWidget);

    // Pump to resolve async future
    await tester.pumpAndSettle();

    // Verify memories are displayed
    expect(find.text('What Juhi Remembers'), findsOneWidget);
    expect(find.text('Loves filter coffee in Bangalore'), findsOneWidget);
    expect(find.text('Software engineer working in tech'), findsOneWidget);
    expect(find.text('PREFERENCE'), findsOneWidget);
    expect(find.text('PROFILE_FACT'), findsOneWidget);
  });

  testWidgets('CompanionSettingsScreen loads profile and allows editing name and mode', (WidgetTester tester) async {
    final mockClient = MockJuhiApiClient();

    await tester.pumpWidget(
      MaterialApp(
        home: CompanionSettingsScreen(apiClient: mockClient),
      ),
    );

    // Pump to resolve default companion fetch
    await tester.pumpAndSettle();

    expect(find.text('Customize Companion'), findsOneWidget);
    expect(find.text('Juhi'), findsWidgets);
    expect(find.text('Girlfriend'), findsOneWidget);
    expect(find.text('Boyfriend'), findsOneWidget);
    expect(find.text('Close Friend'), findsOneWidget);
    expect(find.text('Playful Companion'), findsOneWidget);

    // Tap on Boyfriend option
    await tester.tap(find.text('Boyfriend'));
    await tester.pumpAndSettle();

    // Tap Save button
    await tester.tap(find.text('Save'));
    await tester.pumpAndSettle();

    expect(mockClient.updatedCompanion, isTrue);
  });
}
