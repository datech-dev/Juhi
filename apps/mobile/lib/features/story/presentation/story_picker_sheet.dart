import 'package:flutter/material.dart';
import '../../../core/api/api_client.dart';
import '../../../design_system/tokens/colors.dart';
import '../../../design_system/tokens/radii.dart';

class StoryScenario {
  final String key;
  final String title;
  final String description;
  final IconData icon;

  const StoryScenario({
    required this.key,
    required this.title,
    required this.description,
    required this.icon,
  });
}

class StoryPickerSheet extends StatefulWidget {
  final JuhiApiClient apiClient;
  final Function(Map<String, dynamic> conversation) onStoryStarted;

  const StoryPickerSheet({
    super.key,
    required this.apiClient,
    required this.onStoryStarted,
  });

  static const List<StoryScenario> scenarios = [
    StoryScenario(
      key: 'cafe_rain',
      title: 'Rainy Cafe in Bangalore',
      description: 'Sharing hot filter coffee while listening to gentle raindrops slide down the window.',
      icon: Icons.coffee_rounded,
    ),
    StoryScenario(
      key: 'stargazing',
      title: 'Stargazing at Nandi Hills',
      description: 'Lying under a cool blanket of stars atop the hills with warm tea and quiet conversations.',
      icon: Icons.nights_stay_rounded,
    ),
    StoryScenario(
      key: 'mystery_bookstore',
      title: 'Antique Mystery Bookstore',
      description: 'Exploring forgotten bookshelves during a sudden storm, uncovering antique postcards.',
      icon: Icons.menu_book_rounded,
    ),
    StoryScenario(
      key: 'sci_fi',
      title: 'Orbital Space Station',
      description: 'Watching a majestic purple and gold nebula shimmer from an orbital observation deck.',
      icon: Icons.rocket_launch_rounded,
    ),
  ];

  @override
  State<StoryPickerSheet> createState() => _StoryPickerSheetState();
}

class _StoryPickerSheetState extends State<StoryPickerSheet> {
  String? _loadingScenarioKey;

  Future<void> _startStory(StoryScenario scenario) async {
    setState(() => _loadingScenarioKey = scenario.key);
    try {
      final conv = await widget.apiClient.createStoryConversation(
        scenarioKey: scenario.key,
        title: scenario.title,
      );
      if (mounted) {
        Navigator.pop(context);
        widget.onStoryStarted(conv);
      }
    } catch (e) {
      setState(() => _loadingScenarioKey = null);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to start story: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 24),
      decoration: const BoxDecoration(
        borderRadius: BorderRadius.vertical(top: Radius.circular(JuhiRadius.xl)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: JuhiColors.lavender500.withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(JuhiRadius.md),
                ),
                child: const Icon(Icons.auto_stories_rounded, color: JuhiColors.lavender500),
              ),
              const SizedBox(width: 12),
              const Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Choose a Story Scenario',
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    Text(
                      'Interactive roleplay with isolated story memories',
                      style: TextStyle(fontSize: 12, color: Colors.grey),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          ...StoryPickerSheet.scenarios.map((s) {
            final isLoading = _loadingScenarioKey == s.key;
            return Card(
              margin: const EdgeInsets.symmetric(vertical: 6),
              elevation: 1,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(JuhiRadius.md),
              ),
              child: ListTile(
                onTap: isLoading ? null : () => _startStory(s),
                leading: Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: JuhiColors.lavender500.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(JuhiRadius.md),
                  ),
                  child: Icon(s.icon, color: JuhiColors.lavender500),
                ),
                title: Text(s.title, style: const TextStyle(fontWeight: FontWeight.w600)),
                subtitle: Text(
                  s.description,
                  style: const TextStyle(fontSize: 12, color: Colors.grey),
                ),
                trailing: isLoading
                    ? const SizedBox(
                        width: 18,
                        height: 18,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Icon(Icons.chevron_right_rounded),
              ),
            );
          }),
        ],
      ),
    );
  }
}
