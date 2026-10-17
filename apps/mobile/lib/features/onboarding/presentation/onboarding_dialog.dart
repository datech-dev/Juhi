import 'package:flutter/material.dart';
import '../../../core/api/api_client.dart';
import '../../../design_system/tokens/colors.dart';
import '../../../design_system/tokens/radii.dart';

class OnboardingDialog extends StatefulWidget {
  final JuhiApiClient apiClient;
  final VoidCallback onCompleted;

  const OnboardingDialog({
    super.key,
    required this.apiClient,
    required this.onCompleted,
  });

  static Future<void> showIfNeeded(BuildContext context, JuhiApiClient apiClient) async {
    await showDialog(
      context: context,
      barrierDismissible: false,
      builder: (ctx) => OnboardingDialog(
        apiClient: apiClient,
        onCompleted: () => Navigator.pop(ctx),
      ),
    );
  }

  @override
  State<OnboardingDialog> createState() => _OnboardingDialogState();
}

class _OnboardingDialogState extends State<OnboardingDialog> {
  bool _isAgeConfirmed = false;
  bool _isMemoryConsentGiven = true;
  bool _isSubmitting = false;

  Future<void> _handleAccept() async {
    if (!_isAgeConfirmed) return;

    setState(() => _isSubmitting = true);
    try {
      // 1. Record AI disclosure consent
      await widget.apiClient.recordConsent(
        purpose: 'ai_companion_disclosure',
        decision: 'granted',
      );

      // 2. Record 18+ age verification
      await widget.apiClient.recordConsent(
        purpose: 'age_verification_18_plus',
        decision: 'granted',
      );

      // 3. Record memory consent if checked
      await widget.apiClient.recordConsent(
        purpose: 'memory_storage_consent',
        decision: _isMemoryConsentGiven ? 'granted' : 'declined',
      );

      if (mounted) {
        setState(() => _isSubmitting = false);
        widget.onCompleted();
      }
    } catch (_) {
      // Still proceed if offline or demo
      if (mounted) {
        setState(() => _isSubmitting = false);
        widget.onCompleted();
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(JuhiRadius.xl)),
      insetPadding: const EdgeInsets.symmetric(horizontal: 24, vertical: 32),
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: JuhiColors.lavender500.withValues(alpha: 0.15),
                    borderRadius: BorderRadius.circular(JuhiRadius.md),
                  ),
                  child: const Icon(Icons.favorite_rounded, color: JuhiColors.lavender500),
                ),
                const SizedBox(width: 12),
                const Expanded(
                  child: Text(
                    'Welcome to Juhi',
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            const Text(
              'Before we start your journey, here are a few essential principles regarding your privacy and safety:',
              style: TextStyle(fontSize: 13, color: Colors.grey),
            ),
            const SizedBox(height: 16),
            _buildInfoRow(
              Icons.smart_toy_outlined,
              'AI Companion Disclosure',
              'Juhi is an AI companion created for supportive conversation, friendship, and roleplay. Juhi is not a human or medical professional.',
            ),
            const SizedBox(height: 12),
            _buildInfoRow(
              Icons.privacy_tip_outlined,
              'Your Data & Memory Control',
              'You control what Juhi remembers. You can inspect, edit, or delete any memories at any time from "What Juhi Remembers".',
            ),
            const SizedBox(height: 16),
            const Divider(),
            CheckboxListTile(
              contentPadding: EdgeInsets.zero,
              controlAffinity: ListTileControlAffinity.leading,
              title: const Text(
                'I confirm that I am 18 years of age or older.',
                style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600),
              ),
              value: _isAgeConfirmed,
              onChanged: (val) => setState(() => _isAgeConfirmed = val ?? false),
            ),
            SwitchListTile(
              contentPadding: EdgeInsets.zero,
              title: const Text(
                'Allow Juhi to remember my preferences & hobbies',
                style: TextStyle(fontSize: 13),
              ),
              value: _isMemoryConsentGiven,
              onChanged: (val) => setState(() => _isMemoryConsentGiven = val),
            ),
            const SizedBox(height: 20),
            SizedBox(
              width: double.infinity,
              height: 48,
              child: FilledButton(
                onPressed: _isAgeConfirmed && !_isSubmitting ? _handleAccept : null,
                style: FilledButton.styleFrom(
                  backgroundColor: JuhiColors.lavender500,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(JuhiRadius.md)),
                ),
                child: _isSubmitting
                    ? const SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2),
                      )
                    : const Text(
                        'Agree & Continue',
                        style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
                      ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoRow(IconData icon, String title, String body) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Icon(icon, size: 20, color: JuhiColors.lavender500),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(title, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
              const SizedBox(height: 2),
              Text(body, style: const TextStyle(fontSize: 12, color: Colors.grey)),
            ],
          ),
        ),
      ],
    );
  }
}
