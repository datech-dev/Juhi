import 'dart:convert';
import 'package:flutter/material.dart';
import '../../../core/api/api_client.dart';
import '../../../design_system/tokens/colors.dart';
import '../../../design_system/tokens/radii.dart';

class AccountScreen extends StatefulWidget {
  final JuhiApiClient apiClient;

  const AccountScreen({
    super.key,
    required this.apiClient,
  });

  @override
  State<AccountScreen> createState() => _AccountScreenState();
}

class _AccountScreenState extends State<AccountScreen> {
  bool _isLoading = true;
  int _availableCredits = 0;
  int _reservedCredits = 0;
  List<dynamic> _ledger = [];
  String _displayName = 'Friend';

  @override
  void initState() {
    super.initState();
    _loadAccountData();
  }

  Future<void> _loadAccountData() async {
    try {
      final balance = await widget.apiClient.getCreditBalance();
      final ledger = await widget.apiClient.getCreditLedger(limit: 10);
      final profile = await widget.apiClient.syncUser();

      setState(() {
        _availableCredits = balance['available_balance'] as int? ?? 0;
        _reservedCredits = balance['reserved_balance'] as int? ?? 0;
        _ledger = ledger;
        if (profile.containsKey('display_name') && profile['display_name'] != null) {
          _displayName = profile['display_name'] as String;
        }
        _isLoading = false;
      });
    } catch (_) {
      setState(() => _isLoading = false);
    }
  }

  Future<void> _exportData() async {
    try {
      final export = await widget.apiClient.exportUserData();
      if (!mounted) return;

      final memoriesCount = (export['memories'] as List?)?.length ?? 0;
      final conversationsCount = (export['conversations'] as List?)?.length ?? 0;

      showDialog(
        context: context,
        builder: (ctx) => AlertDialog(
          title: const Text('Data Export Ready'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Your complete personal data package has been assembled according to GDPR and DPDP rights.',
                style: TextStyle(fontSize: 13),
              ),
              const SizedBox(height: 12),
              Text('• Memories: $memoriesCount items'),
              Text('• Conversations: $conversationsCount sessions'),
              Text('• Credits Available: $_availableCredits'),
              const SizedBox(height: 12),
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: Colors.black12,
                  borderRadius: BorderRadius.circular(JuhiRadius.sm),
                ),
                child: Text(
                  const JsonEncoder.withIndent('  ').convert({
                    'user': export['user'],
                    'preferences': export['preferences'],
                    'memories_count': memoriesCount,
                  }),
                  maxLines: 8,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(fontFamily: 'monospace', fontSize: 11),
                ),
              ),
            ],
          ),
          actions: [
            FilledButton(
              onPressed: () => Navigator.pop(ctx),
              child: const Text('Done'),
            ),
          ],
        ),
      );
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Export failed: $e')),
        );
      }
    }
  }

  Future<void> _confirmDeleteAccount() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Delete Account Permanently?'),
        content: const Text(
          'This will permanently delete your account, all companion profiles, saved memories, message histories, and media assets. This action is irreversible.',
          style: TextStyle(fontSize: 13),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx, false),
            child: const Text('Cancel'),
          ),
          FilledButton(
            style: FilledButton.styleFrom(backgroundColor: Colors.red),
            onPressed: () => Navigator.pop(ctx, true),
            child: const Text('Delete Forever'),
          ),
        ],
      ),
    );

    if (confirmed == true) {
      try {
        await widget.apiClient.deleteAccount();
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Account permanently deleted.')),
          );
          Navigator.pop(context, true);
        }
      } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Deletion failed: $e')),
          );
        }
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
        title: const Text('Account & Privacy'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Hi, $_displayName',
              style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            // Credits Card
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [JuhiColors.lavender500, JuhiColors.rose500],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                borderRadius: BorderRadius.circular(JuhiRadius.lg),
                boxShadow: const [
                  BoxShadow(
                    color: Colors.black12,
                    blurRadius: 10,
                    offset: Offset(0, 4),
                  ),
                ],
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        'Juhi Credits Wallet',
                        style: TextStyle(color: Colors.white70, fontSize: 13, fontWeight: FontWeight.w500),
                      ),
                      Icon(Icons.stars_rounded, color: Colors.white),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Text(
                    '$_availableCredits',
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 36,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    _reservedCredits > 0
                        ? '$_reservedCredits reserved for pending image generation'
                        : 'Free Starter Balance',
                    style: const TextStyle(color: Colors.white70, fontSize: 12),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),
            Card(
              elevation: 0,
              color: JuhiColors.lavender500.withValues(alpha: 0.08),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(JuhiRadius.md)),
              child: const Padding(
                padding: EdgeInsets.all(12),
                child: Row(
                  children: [
                    Icon(Icons.info_outline_rounded, color: JuhiColors.lavender500, size: 20),
                    SizedBox(width: 10),
                    Expanded(
                      child: Text(
                        '1 photo request = 10 credits. You receive free promotional credits on sign-up.',
                        style: TextStyle(fontSize: 12),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Recent activity ledger
            const Text(
              'Credit Activity History',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            if (_ledger.isEmpty)
              const Text('No transactions recorded yet.', style: TextStyle(color: Colors.grey, fontSize: 13))
            else
              ..._ledger.map((entry) {
                final delta = entry['available_delta'] as int? ?? 0;
                final reason = entry['reason'] as String? ?? 'transaction';
                final isPositive = delta >= 0;
                return Card(
                  margin: const EdgeInsets.symmetric(vertical: 4),
                  elevation: 0,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(JuhiRadius.md),
                    side: const BorderSide(color: Colors.black12),
                  ),
                  child: ListTile(
                    dense: true,
                    leading: Icon(
                      isPositive ? Icons.add_circle_outline_rounded : Icons.remove_circle_outline_rounded,
                      color: isPositive ? Colors.green : Colors.deepOrange,
                    ),
                    title: Text(
                      reason.replaceAll('_', ' ').toUpperCase(),
                      style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 12),
                    ),
                    trailing: Text(
                      '${isPositive ? "+" : ""}$delta credits',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: isPositive ? Colors.green : Colors.deepOrange,
                      ),
                    ),
                  ),
                );
              }),

            const SizedBox(height: 32),
            const Text(
              'Privacy & Data Controls',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Card(
              elevation: 0,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(JuhiRadius.md),
                side: const BorderSide(color: Colors.black12),
              ),
              child: Column(
                children: [
                  ListTile(
                    leading: const Icon(Icons.file_download_outlined, color: JuhiColors.lavender500),
                    title: const Text('Export My Data', style: TextStyle(fontWeight: FontWeight.w600)),
                    subtitle: const Text('Download a JSON copy of all memories, chats, and settings', style: TextStyle(fontSize: 12)),
                    onTap: _exportData,
                  ),
                  const Divider(height: 1),
                  ListTile(
                    leading: const Icon(Icons.delete_forever_rounded, color: Colors.red),
                    title: const Text('Delete Account Forever', style: TextStyle(color: Colors.red, fontWeight: FontWeight.w600)),
                    subtitle: const Text('Permanently erase all personal memories and conversation history', style: TextStyle(fontSize: 12)),
                    onTap: _confirmDeleteAccount,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
