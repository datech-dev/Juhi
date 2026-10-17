import 'package:flutter/material.dart';
import '../../../core/api/api_client.dart';
import '../../../design_system/tokens/colors.dart';
import '../../../design_system/tokens/spacing.dart';

class MemoryScreen extends StatefulWidget {
  final JuhiApiClient apiClient;

  const MemoryScreen({super.key, required this.apiClient});

  @override
  State<MemoryScreen> createState() => _MemoryScreenState();
}

class _MemoryScreenState extends State<MemoryScreen> {
  List<dynamic> _memories = [];
  bool _isLoading = true;
  String _searchQuery = "";
  String _selectedCategory = "all";
  final TextEditingController _searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _fetchMemories();
  }

  Future<void> _fetchMemories({String? search}) async {
    setState(() => _isLoading = true);
    try {
      final items = await widget.apiClient.getMemories(search: search);
      setState(() {
        _memories = items;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to load memories: $e')),
        );
      }
    }
  }

  Future<void> _deleteMemory(String id) async {
    try {
      await widget.apiClient.deleteMemory(id);
      setState(() {
        _memories.removeWhere((item) => item['id'] == id);
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Memory deleted.')),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Delete failed: $e')),
        );
      }
    }
  }

  Future<void> _clearAllMemories() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Clear All Memories?'),
        content: const Text(
          'Juhi will forget all personal memories saved from previous conversations. This action cannot be undone.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx, false),
            child: const Text('Cancel'),
          ),
          FilledButton(
            style: FilledButton.styleFrom(backgroundColor: Colors.red),
            onPressed: () => Navigator.pop(ctx, true),
            child: const Text('Clear All'),
          ),
        ],
      ),
    );

    if (confirmed == true) {
      try {
        await widget.apiClient.clearAllMemories();
        setState(() {
          _memories.clear();
        });
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('All memories cleared.')),
          );
        }
      } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Error clearing memories: $e')),
          );
        }
      }
    }
  }

  void _showAddMemoryDialog() {
    final contentCtrl = TextEditingController();
    String memoryType = 'preference';
    int importance = 3;

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (ctx) => StatefulBuilder(
        builder: (ctx, setModalState) => Padding(
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
              const Row(
                children: [
                  Icon(Icons.bookmark_add_rounded, color: JuhiColors.lavender500),
                  SizedBox(width: 8),
                  Text(
                    'Add a Personal Memory',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              TextField(
                controller: contentCtrl,
                maxLines: 2,
                decoration: InputDecoration(
                  hintText: 'e.g. I prefer mild spicy South Indian food',
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                ),
              ),
              const SizedBox(height: 12),
              DropdownButtonFormField<String>(
                initialValue: memoryType,
                decoration: InputDecoration(
                  labelText: 'Category',
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                ),
                items: const [
                  DropdownMenuItem(value: 'preference', child: Text('Preference')),
                  DropdownMenuItem(value: 'profile_fact', child: Text('Profile Fact')),
                  DropdownMenuItem(value: 'goal', child: Text('Goal / Hobby')),
                  DropdownMenuItem(value: 'event', child: Text('Life Event')),
                  DropdownMenuItem(value: 'boundary', child: Text('Boundary')),
                ],
                onChanged: (val) {
                  if (val != null) setModalState(() => memoryType = val);
                },
              ),
              const SizedBox(height: 12),
              Row(
                children: [
                  const Text('Importance:'),
                  const SizedBox(width: 8),
                  Slider(
                    value: importance.toDouble(),
                    min: 1,
                    max: 5,
                    divisions: 4,
                    label: '$importance',
                    onChanged: (val) {
                      setModalState(() => importance = val.toInt());
                    },
                  ),
                  Text('$importance/5'),
                ],
              ),
              const SizedBox(height: 12),
              SizedBox(
                width: double.infinity,
                child: FilledButton(
                  onPressed: () async {
                    final text = contentCtrl.text.trim();
                    if (text.isEmpty) return;
                    Navigator.pop(ctx);
                    try {
                      final item = await widget.apiClient.createMemory(
                        contentText: text,
                        memoryType: memoryType,
                        importance: importance,
                      );
                      setState(() {
                        _memories.insert(0, item);
                      });
                      if (mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Memory saved!')),
                        );
                      }
                    } catch (e) {
                      if (mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(content: Text('Failed to save memory: $e')),
                        );
                      }
                    }
                  },
                  child: const Text('Save Memory'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Color _getCategoryColor(String type) {
    switch (type) {
      case 'preference':
        return Colors.teal;
      case 'profile_fact':
        return JuhiColors.lavender500;
      case 'goal':
        return Colors.amber.shade700;
      case 'event':
        return Colors.blueAccent;
      case 'boundary':
        return Colors.purple;
      default:
        return Colors.blueGrey;
    }
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    final filtered = _memories.where((m) {
      final type = m['memory_type'] as String? ?? '';
      if (_selectedCategory != 'all' && type != _selectedCategory) return false;
      if (_searchQuery.isNotEmpty) {
        final content = (m['content_text'] as String? ?? '').toLowerCase();
        if (!content.contains(_searchQuery.toLowerCase())) return false;
      }
      return true;
    }).toList();

    return Scaffold(
      appBar: AppBar(
        title: const Text('What Juhi Remembers'),
        actions: [
          IconButton(
            tooltip: 'Clear All',
            icon: const Icon(Icons.delete_sweep_rounded),
            onPressed: _memories.isEmpty ? null : _clearAllMemories,
          ),
        ],
      ),
      body: Column(
        children: [
          // Search & Filter header
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: TextField(
              controller: _searchController,
              decoration: InputDecoration(
                hintText: 'Search memories...',
                prefixIcon: const Icon(Icons.search_rounded),
                suffixIcon: _searchQuery.isNotEmpty
                    ? IconButton(
                        icon: const Icon(Icons.clear_rounded),
                        onPressed: () {
                          _searchController.clear();
                          setState(() => _searchQuery = "");
                        },
                      )
                    : null,
                contentPadding: const EdgeInsets.symmetric(horizontal: 16),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(JuhiRadius.md),
                ),
              ),
              onChanged: (val) {
                setState(() => _searchQuery = val.trim());
              },
            ),
          ),
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
            child: Row(
              children: [
                _buildFilterChip('all', 'All'),
                _buildFilterChip('preference', 'Preferences'),
                _buildFilterChip('profile_fact', 'Facts'),
                _buildFilterChip('goal', 'Goals'),
                _buildFilterChip('event', 'Events'),
                _buildFilterChip('boundary', 'Boundaries'),
              ],
            ),
          ),
          const Divider(height: 1),
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator())
                : filtered.isEmpty
                    ? Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(
                              Icons.psychology_outlined,
                              size: 64,
                              color: isDark ? Colors.white30 : Colors.black26,
                            ),
                            const SizedBox(height: 16),
                            const Text(
                              'No memories found',
                              style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
                            ),
                            const SizedBox(height: 8),
                            const Padding(
                              padding: EdgeInsets.symmetric(horizontal: 32),
                              child: Text(
                                'Juhi automatically remembers key facts from your chats, or you can add them manually with the button below.',
                                textAlign: TextAlign.center,
                                style: TextStyle(fontSize: 13, color: Colors.grey),
                              ),
                            ),
                          ],
                        ),
                      )
                    : ListView.builder(
                        padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
                        itemCount: filtered.length,
                        itemBuilder: (context, index) {
                          final item = filtered[index];
                          final id = item['id'] as String;
                          final text = (item['content_text'] ?? item['content'] ?? '') as String;
                          final type = item['memory_type'] as String? ?? 'fact';
                          final importance = item['importance'] as int? ?? 3;
                          final badgeColor = _getCategoryColor(type);

                          return Card(
                            margin: const EdgeInsets.symmetric(vertical: 6),
                            elevation: 1,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(JuhiRadius.md),
                            ),
                            child: Padding(
                              padding: const EdgeInsets.all(14),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    children: [
                                      Container(
                                        padding: const EdgeInsets.symmetric(
                                            horizontal: 8, vertical: 2),
                                        decoration: BoxDecoration(
                                          color: badgeColor.withValues(alpha: 0.15),
                                          borderRadius: BorderRadius.circular(4),
                                        ),
                                        child: Text(
                                          type.toUpperCase(),
                                          style: TextStyle(
                                            fontSize: 10,
                                            fontWeight: FontWeight.bold,
                                            color: badgeColor,
                                          ),
                                        ),
                                      ),
                                      const SizedBox(width: 8),
                                      Row(
                                        children: List.generate(
                                          importance,
                                          (i) => const Icon(Icons.star_rounded,
                                              size: 14, color: Colors.amber),
                                        ),
                                      ),
                                      const Spacer(),
                                      IconButton(
                                        icon: const Icon(Icons.delete_outline_rounded,
                                            size: 20, color: Colors.grey),
                                        onPressed: () => _deleteMemory(id),
                                      ),
                                    ],
                                  ),
                                  const SizedBox(height: 6),
                                  Text(
                                    text,
                                    style: const TextStyle(
                                      fontSize: 14.5,
                                      height: 1.3,
                                      fontWeight: FontWeight.w500,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          );
                        },
                      ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        icon: const Icon(Icons.add_rounded),
        label: const Text('Add Memory'),
        onPressed: _showAddMemoryDialog,
      ),
    );
  }

  Widget _buildFilterChip(String key, String label) {
    final isSelected = _selectedCategory == key;
    return Padding(
      padding: const EdgeInsets.only(right: 6),
      child: FilterChip(
        selected: isSelected,
        label: Text(label),
        onSelected: (_) {
          setState(() => _selectedCategory = key);
        },
      ),
    );
  }
}
