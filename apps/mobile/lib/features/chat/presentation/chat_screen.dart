import 'dart:math';
import 'package:flutter/material.dart';
import '../../../core/api/api_client.dart';
import '../../../design_system/components/chat_bubble.dart';
import '../../../design_system/components/chat_composer.dart';
import '../../../design_system/components/companion_avatar.dart';
import '../../../design_system/tokens/colors.dart';
import '../../account/presentation/account_screen.dart';
import '../../companion/presentation/companion_settings_screen.dart';
import '../../memory/presentation/memory_screen.dart';
import '../../onboarding/presentation/onboarding_dialog.dart';
import '../../story/presentation/story_picker_sheet.dart';


class MessageItem {
  final String text;
  final bool isUser;
  final String time;
  final String? imageBase64;

  MessageItem({
    required this.text,
    required this.isUser,
    required this.time,
    this.imageBase64,
  });
}

class ChatScreen extends StatefulWidget {
  final JuhiApiClient apiClient;
  final String? initialConversationId;
  final String companionName;

  const ChatScreen({
    super.key,
    required this.apiClient,
    this.initialConversationId,
    this.companionName = "Juhi",
  });

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final List<MessageItem> _messages = [];
  bool _isLoading = true;
  bool _isSending = false;
  String? _conversationId;
  late String _companionName;

  @override
  void initState() {
    super.initState();
    _companionName = widget.companionName;
    _conversationId = widget.initialConversationId;
    _initializeChat();
  }

  Future<void> _initializeChat() async {
    try {
      if (_conversationId == null) {
        final conv = await widget.apiClient.createConversation(
          title: "Chat with ${widget.companionName}",
        );
        _conversationId = conv['id'] as String;
      }

      final messagesData = await widget.apiClient.getMessages(_conversationId!);
      final loadedMessages = <MessageItem>[];

      for (final m in messagesData) {
        final role = m['role'] as String;
        final isUser = role == 'user';
        final content = m['content_json'] as Map<String, dynamic>;
        String text = "";
        if (content.containsKey('parts')) {
          final parts = content['parts'] as List;
          for (final p in parts) {
            if (p['type'] == 'text') {
              text += p['text'] as String;
            }
          }
        }
        loadedMessages.add(MessageItem(
          text: text,
          isUser: isUser,
          time: "",
        ));
      }

      setState(() {
        _messages.addAll(loadedMessages);
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _handleSendMessage(String text) async {
    if (_conversationId == null) return;

    final idempotencyKey =
        'client_${DateTime.now().millisecondsSinceEpoch}_${Random().nextInt(10000)}';

    setState(() {
      _messages.add(MessageItem(
        text: text,
        isUser: true,
        time: "Just now",
      ));
      _isSending = true;
    });

    try {
      final turn = await widget.apiClient.sendMessage(
        conversationId: _conversationId!,
        text: text,
        idempotencyKey: idempotencyKey,
      );

      final assistContent =
          turn['assistant_message']['content_json'] as Map<String, dynamic>;
      String replyText = "";
      if (assistContent.containsKey('parts')) {
        for (final p in assistContent['parts'] as List) {
          if (p['type'] == 'text') replyText += p['text'] as String;
        }
      }

      setState(() {
        _messages.add(MessageItem(
          text: replyText,
          isUser: false,
          time: "Just now",
        ));
        _isSending = false;
      });
    } catch (e) {
      setState(() {
        _isSending = false;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to send: $e')),
        );
      }
    }
  }

  Future<void> _requestCompanionPhoto(String prompt) async {
    if (_conversationId == null) return;

    final idempotencyKey =
        'client_img_${DateTime.now().millisecondsSinceEpoch}_${Random().nextInt(10000)}';

    setState(() {
      _messages.add(MessageItem(
        text: "Could you share a photo of: $prompt?",
        isUser: true,
        time: "Just now",
      ));
      _messages.add(MessageItem(
        text: "✨ Generating a photo for you...",
        isUser: false,
        time: "Just now",
      ));
    });

    try {
      final job = await widget.apiClient.generateImage(
        prompt: prompt,
        conversationId: _conversationId,
        idempotencyKey: idempotencyKey,
      );

      final jobId = job['id'] as String;

      int attempts = 0;
      while (attempts < 20) {
        await Future.delayed(const Duration(milliseconds: 1500));
        attempts++;
        final status = await widget.apiClient.getJobStatus(jobId);
        final jobStatus = status['status'] as String;

        if (jobStatus == 'succeeded') {
          final resJson = status['result_json'] as Map<String, dynamic>;
          final assetId = resJson['asset_id'] as String;
          final asset = await widget.apiClient.getMediaAsset(assetId);
          final meta = asset['metadata_json'] as Map<String, dynamic>;
          final b64 = meta['b64_preview'] as String?;

          setState(() {
            _messages.removeLast();
            _messages.add(MessageItem(
              text: "Here is the photo you asked for!",
              isUser: false,
              time: "Just now",
              imageBase64: b64,
            ));
          });
          return;
        } else if (jobStatus == 'failed') {
          final errMsg = status['error_message'] ?? 'Image generation failed';
          setState(() {
            _messages.removeLast();
            _messages.add(MessageItem(
              text: "Sorry, I couldn't generate that photo: $errMsg",
              isUser: false,
              time: "Just now",
            ));
          });
          return;
        }
      }

      setState(() {
        _messages.removeLast();
        _messages.add(MessageItem(
          text: "Photo generation is taking a little longer than usual. Please check back shortly!",
          isUser: false,
          time: "Just now",
        ));
      });
    } catch (e) {
      setState(() {
        _messages.removeLast();
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Photo request error: $e')),
        );
      }
    }
  }

  void _showPhotoRequestDialog() {
    final promptController = TextEditingController();
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) {
        return Padding(
          padding: EdgeInsets.only(
            left: 20,
            right: 20,
            top: 20,
            bottom: MediaQuery.of(ctx).viewInsets.bottom + 20,
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  const Icon(Icons.auto_awesome_rounded, color: JuhiColors.lavender500),
                  const SizedBox(width: 8),
                  Text(
                    "Request Photo from ${widget.companionName}",
                    style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              const Text(
                "Each image generation uses 10 credits from your account.",
                style: TextStyle(fontSize: 13, color: Colors.grey),
              ),
              const SizedBox(height: 16),
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: [
                  ActionChip(
                    label: const Text("Filter coffee in Bangalore"),
                    onPressed: () {
                      Navigator.pop(ctx);
                      _requestCompanionPhoto("Juhi having hot filter coffee at a traditional cafe in Bangalore");
                    },
                  ),
                  ActionChip(
                    label: const Text("Diwali festive portrait"),
                    onPressed: () {
                      Navigator.pop(ctx);
                      _requestCompanionPhoto("Juhi wearing a festive Indian attire with diyas and warm lights");
                    },
                  ),
                  ActionChip(
                    label: const Text("Monsoon walk in Mumbai"),
                    onPressed: () {
                      Navigator.pop(ctx);
                      _requestCompanionPhoto("Juhi holding an umbrella enjoying gentle rain at Marine Drive Mumbai");
                    },
                  ),
                ],
              ),
              const SizedBox(height: 16),
              TextField(
                controller: promptController,
                decoration: InputDecoration(
                  hintText: "Or describe a custom scene...",
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                  suffixIcon: IconButton(
                    icon: const Icon(Icons.send_rounded),
                    onPressed: () {
                      final val = promptController.text.trim();
                      if (val.isNotEmpty) {
                        Navigator.pop(ctx);
                        _requestCompanionPhoto(val);
                      }
                    },
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        titleSpacing: 0,
        title: Row(
          children: [
            CompanionAvatar(name: _companionName, size: 36),
            const SizedBox(width: 12),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  _companionName,
                  style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 1),
                  decoration: BoxDecoration(
                    color: JuhiColors.lavender500.withValues(alpha: 0.15),
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: const Text(
                    "AI Companion",
                    style: TextStyle(
                      fontSize: 10,
                      fontWeight: FontWeight.w500,
                      color: JuhiColors.lavender500,
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
        actions: [
          IconButton(
            tooltip: "Request Photo",
            icon: const Icon(Icons.photo_camera_rounded),
            onPressed: _showPhotoRequestDialog,
          ),
          PopupMenuButton<String>(
            icon: const Icon(Icons.more_vert_rounded),
            onSelected: (value) async {
              if (value == 'story') {
                showModalBottomSheet(
                  context: context,
                  isScrollControlled: true,
                  shape: const RoundedRectangleBorder(
                    borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
                  ),
                  builder: (ctx) => StoryPickerSheet(
                    apiClient: widget.apiClient,
                    onStoryStarted: (conv) {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => ChatScreen(
                            apiClient: widget.apiClient,
                            initialConversationId: conv['id'] as String,
                            companionName: _companionName,
                          ),
                        ),
                      );
                    },
                  ),
                );
              } else if (value == 'memory') {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => MemoryScreen(apiClient: widget.apiClient),
                  ),
                );
              } else if (value == 'customize') {
                final result = await Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => CompanionSettingsScreen(apiClient: widget.apiClient),
                  ),
                );
                if (result == true && mounted) {
                  try {
                    final profile = await widget.apiClient.getDefaultCompanion();
                    if (profile.containsKey('display_name') && mounted) {
                      setState(() {
                        _companionName = profile['display_name'] as String;
                      });
                    }
                  } catch (_) {}
                }
              } else if (value == 'account') {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => AccountScreen(apiClient: widget.apiClient),
                  ),
                );
              } else if (value == 'disclosure') {
                OnboardingDialog.showIfNeeded(context, widget.apiClient);
              }
            },
            itemBuilder: (context) => [
              const PopupMenuItem(
                value: 'story',
                child: Row(
                  children: [
                    Icon(Icons.auto_stories_rounded, size: 20, color: JuhiColors.lavender500),
                    SizedBox(width: 12),
                    Text("Story Mode & Roleplay"),
                  ],
                ),
              ),
              const PopupMenuItem(
                value: 'memory',
                child: Row(
                  children: [
                    Icon(Icons.psychology_outlined, size: 20, color: JuhiColors.lavender500),
                    SizedBox(width: 12),
                    Text("What Juhi Remembers"),
                  ],
                ),
              ),
              const PopupMenuItem(
                value: 'customize',
                child: Row(
                  children: [
                    Icon(Icons.tune_rounded, size: 20, color: JuhiColors.lavender500),
                    SizedBox(width: 12),
                    Text("Customize Companion"),
                  ],
                ),
              ),
              const PopupMenuItem(
                value: 'account',
                child: Row(
                  children: [
                    Icon(Icons.account_balance_wallet_outlined, size: 20, color: JuhiColors.lavender500),
                    SizedBox(width: 12),
                    Text("Wallet & Privacy"),
                  ],
                ),
              ),
              const PopupMenuItem(
                value: 'disclosure',
                child: Row(
                  children: [
                    Icon(Icons.shield_outlined, size: 20, color: JuhiColors.lavender500),
                    SizedBox(width: 12),
                    Text("AI & Safety Disclosure"),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : _messages.isEmpty
                    ? Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            CompanionAvatar(name: _companionName, size: 64),
                            const SizedBox(height: 16),
                            Text(
                              "Say hi to $_companionName!",
                              style: TextStyle(
                                fontSize: 18,
                                fontWeight: FontWeight.w600,
                                color: isDark
                                    ? JuhiColors.textDarkPrimary
                                    : JuhiColors.textLightPrimary,
                              ),
                            ),
                            const SizedBox(height: 8),
                            const Text(
                              "Type in English, Hindi, Tamil, Hinglish or Tanglish",
                              style: TextStyle(
                                fontSize: 13,
                                color: JuhiColors.textDarkMuted,
                              ),
                            ),
                          ],
                        ),
                      )
                    : ListView.builder(
                        padding: const EdgeInsets.symmetric(vertical: 8),
                        itemCount: _messages.length,
                        itemBuilder: (context, index) {
                          final msg = _messages[index];
                          return ChatBubble(
                            text: msg.text,
                            isUser: msg.isUser,
                            time: msg.time,
                            imageBase64: msg.imageBase64,
                          );
                        },
                      ),
          ),
          ChatComposer(
            onSend: _handleSendMessage,
            isSending: _isSending,
          ),
        ],
      ),
    );
  }
}
