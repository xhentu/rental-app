// lib/screens/listing_tab.dart
import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../widgets/property_card.dart'; 
import '../widgets/search_filter.dart';
import '../utils/language_logic.dart';
import 'property_detail_screen.dart';

class ListingTab extends StatefulWidget {
  final String category; 

  const ListingTab({super.key, required this.category});

  @override
  State<ListingTab> createState() => _ListingTabState();
}

class _ListingTabState extends State<ListingTab> {
  final ScrollController _scrollController = ScrollController();
  
  Map<String, dynamic>? _activeFilters;
  List<dynamic> _properties = []; // Dynamic List သုံးပြီး Raw Json ဒေတာများကို တိုက်ရိုက်သိမ်းဆည်းခြင်း
  String? _nextCursorUrl;
  bool _isLoading = false;
  bool _isLoadingMore = false;
  bool _isFirstLoadError = false;

  @override
  void initState() {
    super.initState();
    _loadInitialFeed();
    
    // 🔄 Infinite Scroll အတွက် မျက်နှာပြင်အောက်ခြေ ရောက်ခါနီးလျှင် ဒေတာ ထပ်ဆွဲမည့် စနစ်
    _scrollController.addListener(() {
      if (_scrollController.position.pixels >= _scrollController.position.maxScrollExtent - 200) {
        _loadMoreFeed();
      }
    });
  }

  @override
  void didUpdateWidget(covariant ListingTab oldWidget) {
    super.didUpdateWidget(oldWidget);
    // အရောင်း/အငှား Tab ပြောင်းသွားပါက ဒေတာအသစ် ပြန်ဆွဲရန်
    if (oldWidget.category != widget.category) {
      _loadInitialFeed();
    }
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  /// ပထမဆုံးအကြိမ် ဝင်လာစဉ် (သို့) Pull to Refresh လုပ်စဉ် Feed ဆွဲယူခြင်း
  Future<void> _loadInitialFeed({bool forceRefresh = false}) async {
    if (!mounted) return;
    setState(() {
      _isLoading = !forceRefresh;
      _isFirstLoadError = false;
    });

    final data = await ApiService.fetchPropertyFeed(
      category: widget.category,
      activeFilters: _activeFilters,
      forceRefresh: forceRefresh,
    );

    if (!mounted) return;

    if (data != null) {
      setState(() {
        _properties = data['results'] as List? ?? [];
        _nextCursorUrl = data['next'];
        _isLoading = false;
      });
    } else {
      setState(() {
        _isLoading = false;
        if (_properties.isEmpty) _isFirstLoadError = true;
      });
    }
  }

  /// အောက်သို့ Scroll ဆွဲချပါက နောက်စာမျက်နှာ Pagination ဒေတာ ဆက်ဆွဲယူခြင်း
  Future<void> _loadMoreFeed() async {
    if (_isLoadingMore || _nextCursorUrl == null) return;

    setState(() {
      _isLoadingMore = true;
    });

    final data = await ApiService.fetchPropertyFeed(
      cursorUrl: _nextCursorUrl,
      category: widget.category,
      activeFilters: _activeFilters,
    );

    if (!mounted) return;

    if (data != null) {
      setState(() {
        var newItems = data['results'] as List? ?? [];
        _properties.addAll(newItems);
        _nextCursorUrl = data['next'];
        _isLoadingMore = false;
      });
    } else {
      setState(() {
        _isLoadingMore = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        _buildSearchBarUI(),
        Expanded(
          child: _isLoading 
              ? const Center(child: CircularProgressIndicator(color: Color(0xFF3577F6)))
              : _isFirstLoadError 
                  ? _buildErrorState()
                  : _properties.isEmpty
                      ? (_activeFilters != null ? _buildNoMatchState() : _buildEmptyState())
                      : RefreshIndicator(
                          onRefresh: () => _loadInitialFeed(forceRefresh: true),
                          color: const Color(0xFF3577F6),
                          child: ListView.builder(
                            controller: _scrollController,
                            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                            physics: const AlwaysScrollableScrollPhysics(),
                            itemCount: _properties.length + (_isLoadingMore ? 1 : 0),
                            itemBuilder: (context, index) {
                              if (index == _properties.length) {
                                return const Padding(
                                  padding: EdgeInsets.symmetric(vertical: 16),
                                  child: Center(child: CircularProgressIndicator(color: Color(0xFF3577F6))),
                                );
                              }

                              final item = _properties[index] as Map<String, dynamic>;
                              
                              String displayType = item['offer_type'] == 'sale' ? 'အရောင်း' : 'အငှား';
                              String displayLocation = "${item['township'] ?? ''}၊ ${item['region'] ?? ''}";
                              
                              // Backend ပုံများထဲမှ ပထမဆုံးပုံကို ယူခြင်း၊ ပုံမရှိပါက Placeholder သုံးခြင်း
                              String imgUrl = 'https://via.placeholder.com/400x300';
                              if (item['images'] != null && (item['images'] as List).isNotEmpty) {
                                imgUrl = item['images'][0]['image'] ?? imgUrl;
                              }

                              return GestureDetector(
                                onTap: () {
                                  // Card အား နှိပ်လိုက်ပါက Detail Screen သို့ ဒေတာများ သယ်ဆောင်၍ သွားမည်
                                  Navigator.push(
                                    context,
                                    MaterialPageRoute(
                                      builder: (context) => PropertyDetailScreen(
                                        propertyData: item,
                                        images: const [], // API Feed မှ လာသဖြင့် Local Images အား အလွတ်ပေးမည်
                                      ),
                                    ),
                                  );
                                },
                                child: PropertyCard(
                                  fullPropertyData: item,
                                  title: item['title']?.toString() ?? 'အမည်မသိ',
                                  price: double.tryParse(item['price']?.toString() ?? '0')?.toStringAsFixed(0) ?? '0',
                                  location: displayLocation,
                                  imageUrl: imgUrl,
                                  type: displayType, 
                                  specs: item['area_dimension_text']?.toString() ?? '',
                                ),
                              );
                            },
                          ),
                        ),
        ),
      ],
    );
  }

  /// ရှာဖွေရေးနှင့် Filter Modal ခေါ်ယူသည့် Search Bar Widget
  Widget _buildSearchBarUI() {
    return GestureDetector(
      onTap: () async {
        final filters = await showModalBottomSheet<Map<String, dynamic>>(
          context: context,
          isScrollControlled: true,
          backgroundColor: Colors.transparent,
          builder: (context) => const SearchFilter(), 
        );

        if (filters != null) {
          setState(() {
            _activeFilters = filters;
          });
          _loadInitialFeed();
        }
      },
      child: Container(
        margin: const EdgeInsets.fromLTRB(16, 16, 16, 8),
        padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
        decoration: BoxDecoration(
          color: Colors.white, borderRadius: BorderRadius.circular(16),
          boxShadow: [BoxShadow(color: const Color(0xFF3577F6).withOpacity(0.06), blurRadius: 12, offset: const Offset(0, 4))],
          border: Border.all(color: const Color(0xFFE4ECFB), width: 1.2),
        ),
        child: Row(
          children: [
            const Icon(Icons.search_rounded, color: Color(0xFF3577F6), size: 22),
            const SizedBox(width: 12),
            Expanded(
              child: Text(
                _activeFilters != null ? 'စစ်ထုတ်ထားသော အိမ်ခြံမြေများ' : (t('search_hint') ?? 'မြို့နယ်၊ အိမ်အမျိုးအစား ရှာရန်...'), 
                style: TextStyle(color: _activeFilters != null ? const Color(0xFF2B3550) : const Color(0xFF9AA5B8), fontSize: 14.5, fontWeight: _activeFilters != null ? FontWeight.bold : FontWeight.w500),
              ),
            ),
            Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(color: _activeFilters != null ? const Color(0xFF3577F6).withOpacity(0.1) : const Color(0xFFF4F7FF), borderRadius: BorderRadius.circular(8)),
              child: Icon(_activeFilters != null ? Icons.filter_alt_rounded : Icons.tune_rounded, size: 18, color: _activeFilters != null ? const Color(0xFF3577F6) : const Color(0xFF5A6B8A)),
            ),
            if (_activeFilters != null) ...[
              const SizedBox(width: 8),
              GestureDetector(
                onTap: () {
                  setState(() { _activeFilters = null; });
                  _loadInitialFeed();
                },
                child: Container(
                  padding: const EdgeInsets.all(4),
                  decoration: BoxDecoration(color: Colors.red.shade50, shape: BoxShape.circle),
                  child: const Icon(Icons.close_rounded, size: 16, color: Colors.red),
                ),
              ),
            ]
          ],
        ),
      ),
    );
  }

  /// ဒေတာမရှိပါက ပြသပေးမည့် UI
  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(padding: const EdgeInsets.all(24), decoration: const BoxDecoration(color: Color(0xFFF4F7FF), shape: BoxShape.circle), child: const Icon(Icons.real_estate_agent_rounded, size: 60, color: Color(0xFF9AA5B8))),
          const SizedBox(height: 16),
          const Text("အိမ်ခြံမြေ စာရင်းမရှိသေးပါ", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Color(0xFF2B3550))),
        ],
      ),
    );
  }

  /// Filter စစ်ထုတ်ချက်များနှင့် ကိုက်ညီသော ဒေတာမရှိပါက ပြသပေးမည့် UI
  Widget _buildNoMatchState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(padding: const EdgeInsets.all(24), decoration: BoxDecoration(color: Colors.orange.shade50, shape: BoxShape.circle), child: Icon(Icons.search_off_rounded, size: 60, color: Colors.orange.shade300)),
          const SizedBox(height: 16),
          const Text("ရှာဖွေမှု ရလဒ်မတွေ့ပါ", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Color(0xFF2B3550))),
        ],
      ),
    );
  }

  /// Network သို့မဟုတ် Server Error တက်ပါက ပြသပေးမည့် UI
  Widget _buildErrorState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.wifi_off_rounded, size: 50, color: Colors.redAccent),
          const SizedBox(height: 12),
          const Text("ကွန်ရက်ချိတ်ဆက်မှု မရနိုင်ပါ", style: TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF2B3550))),
          const SizedBox(height: 8),
          ElevatedButton(
            onPressed: () => _loadInitialFeed(),
            style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF3577F6), foregroundColor: Colors.white),
            child: const Text("ပြန်ကြိုးစားမည်"),
          )
        ],
      ),
    );
  }
}