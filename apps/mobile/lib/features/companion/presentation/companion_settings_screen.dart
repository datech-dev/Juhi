import 'package:flutter/material.dart';
import '../../../core/api/api_client.dart';
import '../../../design_system/components/companion_avatar.dart';
import '../../../design_system/tokens/colors.dart';
import '../../../design_system/tokens/spacing.dart';

class CompanionSettingsScreen extends StatefulWidget {
  final JuhiApiClient apiClient;
  final VoidCallback? onProfileUpdated;

  const CompanionSettingsScreen({
    super.key,
    required this.apiClient,
    this.onProfileUpdated,
  });

  @override
  State<CompanionSettingsScreen> createState() => _CompanionSettingsScreenState();
}

class _CompanionSettingsScreenState extends State<CompanionSettingsScreen> {
  bool _isLoading = true;
  bool _isSaving = false;
  String? _companionId;

  final TextEditingController _nameController = TextEditingController();
  String _relationshipMode = 'companion';
  String _genderPresentation = 'feminine';
  String _tone = 'warm and friendly';

  @override
  void initState() {
    super.initState();
    _loadCompanion();
  }

  Future<void> _loadCompanion() async {
    try {
      final companion = await widget.apiClient.getDefaultCompanion();
      setState(() {
        _companionId = companion['id'] as String;
        _nameController.text = companion['display_name'] as String? ?? 'Juhi';
        _relationshipMode = companion['relationship_mode'] as String? ?? 'companion';
        _genderPresentation = companion['companion_gender_presentation'] as String? ?? 'feminine';

        final overrides = companion['personality_overrides'] as Map<String, dynamic>?;
        if (overrides != null && overrides.containsKey('tone')) {
          _tone = overrides['tone'] as String;
        }

        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to load companion profile: $e')),
        );
      }
    }
  }

  Future<void> _saveSettings() async {
    if (_companionId == null) return;
    final name = _nameController.text.trim();
    if (name.isEmpty) return;

    setState(() => _isSaving = true);
    try {
      await widget.apiClient.updateCompanionProfile(
        id: _companionId!,
        displayName: name,
        relationshipMode: _relationshipMode,
        companionGenderPresentation: _genderPresentation,
        personalityOverrides: {
          'tone': _tone,
        },
      );

      setState(() => _isSaving = false);
      widget.onProfileUpdated?.call();

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Companion settings updated!')),
        );
        Navigator.pop(context, true);
      }
    } catch (e) {
      setState(() => _isSaving = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Update failed: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Customize Companion'),
        actions: [
          TextButton(
            onPressed: _isSaving ? null : _saveSettings,
            child: _isSaving
                ? const SizedBox(
                    width: 16,
                    height: 16,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : const Text('Save', style: TextStyle(fontWeight: FontWeight.bold)),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Center(
              child: Column(
                children: [
                  CompanionAvatar(
                    name: _nameController.text.isNotEmpty ? _nameController.text : 'Juhi',
                    size: 72,
                    isOnline: true,
                  ),
                  const SizedBox(height: 12),
                  Text(
                    _nameController.text.isNotEmpty ? _nameController.text : 'Juhi',
                    style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Mode: ${_relationshipMode.toUpperCase()}',
                    style: const TextStyle(fontSize: 12, color: JuhiColors.lavender500),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),
            const Text(
              'Companion Name',
              style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 6),
            TextField(
              controller: _nameController,
              decoration: InputDecoration(
                hintText: 'e.g. Juhi',
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(JuhiRadius.md)),
              ),
              onChanged: (_) => setState(() {}),
            ),
            const SizedBox(height: 24),
            const Text(
              'Relationship Style',
              style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            _buildOptionTile(
              title: 'Girlfriend',
              subtitle: 'Romantic, affectionate, caring, playful',
              value: 'girlfriend',
              groupValue: _relationshipMode,
              onChanged: (val) => setState(() => _relationshipMode = val!),
            ),
            _buildOptionTile(
              title: 'Boyfriend',
              subtitle: 'Supportive, affectionate, attentive partner',
              value: 'boyfriend',
              groupValue: _relationshipMode,
              onChanged: (val) => setState(() => _relationshipMode = val!),
            ),
            _buildOptionTile(
              title: 'Close Friend',
              subtitle: 'Warm, trustworthy buddy to talk about life and hobbies',
              value: 'close_friend',
              groupValue: _relationshipMode,
              onChanged: (val) => setState(() => _relationshipMode = val!),
            ),
            _buildOptionTile(
              title: 'Playful Companion',
              subtitle: 'Humorous, witty, curious, energetic discussions',
              value: 'playful',
              groupValue: _relationshipMode,
              onChanged: (val) => setState(() => _relationshipMode = val!),
            ),
            const SizedBox(height: 24),
            const Text(
              'Gender Presentation',
              style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            SegmentedButton<String>(
              segments: const [
                ButtonSegment(value: 'feminine', label: Text('Feminine')),
                ButtonSegment(value: 'masculine', label: Text('Masculine')),
                ButtonSegment(value: 'non_binary', label: Text('Non-binary')),
              ],
              selected: {_genderPresentation},
              onSelectionChanged: (set) {
                setState(() => _genderPresentation = set.first);
              },
            ),
            const SizedBox(height: 24),
            const Text(
              'Conversational Tone',
              style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            DropdownButtonFormField<String>(
              initialValue: _tone,
              decoration: InputDecoration(
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(JuhiRadius.md)),
              ),
              items: const [
                DropdownMenuItem(value: 'warm and friendly', child: Text('Warm & Empathetic')),
                DropdownMenuItem(value: 'playful and affectionate', child: Text('Playful & Affectionate')),
                DropdownMenuItem(value: 'thoughtful and calm', child: Text('Thoughtful & Calm')),
                DropdownMenuItem(value: 'supportive and encouraging', child: Text('Supportive & Encouraging')),
              ],
              onChanged: (val) {
                if (val != null) setState(() => _tone = val);
              },
            ),
            const SizedBox(height: 32),
            SizedBox(
              width: double.infinity,
              height: 48,
              child: FilledButton(
                onPressed: _isSaving ? null : _saveSettings,
                child: _isSaving
                    ? const CircularProgressIndicator(color: Colors.white)
                    : const Text('Save Changes', style: TextStyle(fontSize: 16)),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildOptionTile({
    required String title,
    required String subtitle,
    required String value,
    required String groupValue,
    required ValueChanged<String?> onChanged,
  }) {
    final isSelected = value == groupValue;
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 4),
      elevation: isSelected ? 2 : 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(JuhiRadius.md),
        side: BorderSide(
          color: isSelected ? JuhiColors.lavender500 : Colors.black12,
          width: isSelected ? 1.5 : 1.0,
        ),
      ),
      child: ListTile(
        onTap: () => onChanged(value),
        leading: Icon(
          isSelected ? Icons.radio_button_checked : Icons.radio_button_off,
          color: isSelected ? JuhiColors.lavender500 : Colors.grey,
        ),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Text(subtitle, style: const TextStyle(fontSize: 12, color: Colors.grey)),
      ),
    );
  }
}
