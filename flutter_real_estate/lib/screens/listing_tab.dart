import 'package:flutter/material.dart';

// --- Imports ---
import '../widgets/property_card.dart'; 
import '../widgets/search_filter.dart';
import '../utils/language_logic.dart'; // ဘာသာစကားအတွက်
import '../utils/data_manager.dart';   // Data အသစ်ကို နားထောင်ဖို့အတွက်

// 🔴 Filter Data မှတ်ထားရန် StatefulWidget သို့ ပြောင်းလိုက်သည်
class ListingTab extends StatefulWidget {
  final String category; 

  const ListingTab({super.key, required this.category});

  @override
  State<ListingTab> createState() => _ListingTabState();
}

class _ListingTabState extends State<ListingTab> {
  
  // 🔴 Active Filter Data များကို သိမ်းဆည်းရန်
  Map<String, dynamic>? _activeFilters;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // --- SEARCH BAR (Modern UI) ---
        GestureDetector(
          onTap: () async {
            // 🔴 Modal မှ ပြန်ပို့မည့် Data ကို ဖမ်းယူရန် await အသုံးပြုခြင်း
            final filters = await showModalBottomSheet<Map<String, dynamic>>(
              context: context,
              isScrollControlled: true,
              backgroundColor: Colors.transparent,
              builder: (context) => const SearchFilter(), 
            );

            // 🔴 ပြန်လာသော Data ရှိလျှင် State Update လုပ်ပေးခြင်း
            if (filters != null) {
              setState(() {
                _activeFilters = filters;
              });
            }
          },
          child: Container(
            margin: const EdgeInsets.fromLTRB(16, 16, 16, 8),
            padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
            decoration: BoxDecoration(
              color: Colors.white, 
              borderRadius: BorderRadius.circular(16),
              boxShadow: [
                BoxShadow(
                  color: const Color(0xFF3577F6).withOpacity(0.06),
                  blurRadius: 12,
                  offset: const Offset(0, 4),
                ),
              ],
              border: Border.all(color: const Color(0xFFE4ECFB), width: 1.2),
            ),
            child: Row(
              children: [
                const Icon(Icons.search_rounded, color: Color(0xFF3577F6), size: 22),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    // Filter On ထားလျှင် စာသားပြောင်းရန်
                    _activeFilters != null 
                        ? 'စစ်ထုတ်ထားသော အိမ်ခြံမြေများ' 
                        : (t('search_hint') ?? 'မြို့နယ်၊ အိမ်အမျိုးအစား ရှာရန်...'), 
                    style: TextStyle(
                      color: _activeFilters != null ? const Color(0xFF2B3550) : const Color(0xFF9AA5B8), 
                      fontSize: 14.5, 
                      fontWeight: _activeFilters != null ? FontWeight.bold : FontWeight.w500
                    ),
                  ),
                ),
                Container(
                  padding: const EdgeInsets.all(6),
                  decoration: BoxDecoration(
                    color: _activeFilters != null ? const Color(0xFF3577F6).withOpacity(0.1) : const Color(0xFFF4F7FF),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Icon(
                    _activeFilters != null ? Icons.filter_alt_rounded : Icons.tune_rounded, 
                    size: 18, 
                    color: _activeFilters != null ? const Color(0xFF3577F6) : const Color(0xFF5A6B8A)
                  ),
                ),
                // Filter ဖြုတ်ရန် Clear ခလုတ် (Filter On ထားမှသာပေါ်မည်)
                if (_activeFilters != null) ...[
                  const SizedBox(width: 8),
                  GestureDetector(
                    onTap: () {
                      setState(() {
                        _activeFilters = null; // 🔴 Filter များကို ရှင်းလင်းမည်
                      });
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
        ),
        
        // --- REAL-TIME DATA LIST ---
        Expanded(
          child: ValueListenableBuilder<List<Map<String, dynamic>>>( 
            valueListenable: propertyListNotifier, 
            builder: (context, properties, child) {
              
              if (properties.isEmpty) {
                return _buildEmptyState();
              }

              // 🔴 ၁။ မူလ Category Tab Filter (All, Sale, Rent) စစ်ထုတ်ခြင်း
              List<Map<String, dynamic>> filteredList = properties.where((item) {
                if (widget.category != 'all') {
                  bool isSaleTab = widget.category == 'sale';
                  bool isItemSale = item['type'] == 'For Sale' || item['type'] == 'အရောင်း';
                  return isSaleTab == isItemSale;
                }
                return true;
              }).toList();

              // 🔴 ၂။ Advanced Search Filter စစ်ထုတ်ခြင်း
              if (_activeFilters != null) {
                filteredList = filteredList.where((item) {
                  
                  // တိုင်း / ပြည်နယ် စစ်ဆေးခြင်း (တည်နေရာ စာသားထဲတွင် ပါ/မပါ စစ်သည်)
                  if (_activeFilters!['state'] != 'အားလုံး') {
                    String loc = item['location']?.toString() ?? '';
                    if (!loc.contains(_activeFilters!['state'])) return false;
                  }

                  // မြို့နယ် စစ်ဆေးခြင်း
                  if (_activeFilters!['township'] != 'အားလုံး') {
                    String loc = item['location']?.toString() ?? '';
                    if (!loc.contains(_activeFilters!['township'])) return false;
                  }

                  // Transaction Type စစ်ဆေးခြင်း ('အရောင်း', 'အငှား', 'ဝယ်လိုသည်', 'ငှားလိုသည်')
                  if (_activeFilters!['transactionType'] != 'အားလုံး') {
                    String typeMap = _mapTypeToMyanmar(item['type']?.toString() ?? '');
                    if (typeMap != _activeFilters!['transactionType']) return false;
                  }

                  // Property Type (အိမ်၊ ကွန်ဒို၊ တိုက်ခန်း စသည်) စစ်ဆေးခြင်း
                  if (_activeFilters!['propertyType'] != 'အားလုံး') {
                    // UploadScreen တွင် သိမ်းထားသော propertyType data လိုအပ်ပါသည်
                    String propType = item['propertyType']?.toString() ?? ''; 
                    String searchType = _mapPropertyTypeToEnglish(_activeFilters!['propertyType']);
                    if (propType != searchType && propType != _activeFilters!['propertyType']) return false;
                  }

                  // မျက်နှာလှည့် စစ်ဆေးခြင်း
                  if (_activeFilters!['direction'] != 'အားလုံး') {
                    String specs = item['specs']?.toString() ?? '';
                    if (!specs.contains("မျက်နှာလှည့်: ${_activeFilters!['direction']}")) return false;
                  }

                  // ဈေးနှုန်း အနည်းဆုံး စစ်ဆေးခြင်း
                  double itemPrice = double.tryParse(item['price']?.toString() ?? '0') ?? 0;
                  
                  if (_activeFilters!['minPrice'] != null && _activeFilters!['minPrice'].toString().isNotEmpty) {
                    double minP = double.tryParse(_activeFilters!['minPrice']) ?? 0;
                    if (itemPrice < minP) return false;
                  }

                  // ဈေးနှုန်း အများဆုံး စစ်ဆေးခြင်း
                  if (_activeFilters!['maxPrice'] != null && _activeFilters!['maxPrice'].toString().isNotEmpty) {
                    double maxP = double.tryParse(_activeFilters!['maxPrice']) ?? double.infinity;
                    if (itemPrice > maxP) return false;
                  }

                  return true; 
                }).toList();
              }

              // Filter စစ်ပြီးနောက် Data မရှိပါက
              if (filteredList.isEmpty) {
                return _buildNoMatchState();
              }

              return ListView.builder(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                physics: const BouncingScrollPhysics(), 
                itemCount: filteredList.length,
                itemBuilder: (context, index) {
                  // နောက်ဆုံးတင်ထားတာ အပေါ်ဆုံးမှာပေါ်အောင် ပြောင်းပြန်ယူရန် (Optional)
                  final reversedIndex = filteredList.length - 1 - index;
                  final item = filteredList[reversedIndex]; 
                  
                  return PropertyCard(
                    fullPropertyData: item,
                    title: item['title']?.toString() ?? 'အမည်မသိ',
                    price: item['price']?.toString() ?? '0',
                    location: item['location']?.toString() ?? 'နေရာမသိ',
                    imageUrl: item['image']?.toString() ?? 'https://via.placeholder.com/400x300',
                    type: item['type']?.toString() ?? 'For Sale', 
                    specs: item['specs']?.toString() ?? '',
                  );
                },
              );
            },
          ),
        ),
      ],
    );
  }

  // --- Helper Methods For Filtering ---

  // Database က English လို သိမ်းထားရင် မြန်မာလို ပြန်ပြောင်းစစ်ဖို့
  String _mapTypeToMyanmar(String type) {
    switch (type) {
      case 'For Sale': return 'အရောင်း';
      case 'For Rent': return 'အငှား';
      case 'Want to Buy': return 'ဝယ်လိုသည်';
      case 'Want to Rent': return 'ငှားလိုသည်';
      default: return type;
    }
  }

  // Search Filter က မြန်မာလို ရွေးလိုက်တဲ့ အိမ်အမျိုးအစားကို Upload data နဲ့ ကိုက်ညီအောင်ပြောင်းဖို့
  String _mapPropertyTypeToEnglish(String mmType) {
    switch (mmType) {
      case 'အိမ်': return 'house';
      case 'ကွန်ဒို': return 'condo';
      case 'တိုက်ခန်း': return 'apartment';
      case 'မြေ': return 'land';
      case 'ဂိုဒေါင်': return 'warehouse';
      default: return mmType;
    }
  }

  // Data မရှိသေးချိန်တွင် ပြသမည့် ပုံစံ
  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            padding: const EdgeInsets.all(24),
            decoration: const BoxDecoration(color: Color(0xFFF4F7FF), shape: BoxShape.circle),
            child: const Icon(Icons.real_estate_agent_rounded, size: 60, color: Color(0xFF9AA5B8)),
          ),
          const SizedBox(height: 16),
          const Text(
            "အိမ်ခြံမြေ စာရင်းမရှိသေးပါ",
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Color(0xFF2B3550)),
          ),
          const SizedBox(height: 8),
          const Text(
            "အောက်ပါ 'စာရင်းသွင်းမည်' မှတစ်ဆင့်\nစတင်ထည့်သွင်းနိုင်ပါသည်။",
            textAlign: TextAlign.center,
            style: TextStyle(fontSize: 14, color: Color(0xFF76799C), height: 1.5),
          ),
        ],
      ),
    );
  }

  // Filter ဖြင့် ရှာမတွေ့ချိန်တွင် ပြသမည့် ပုံစံ (NEW)
  Widget _buildNoMatchState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            padding: const EdgeInsets.all(24),
            decoration: BoxDecoration(color: Colors.orange.shade50, shape: BoxShape.circle),
            child: Icon(Icons.search_off_rounded, size: 60, color: Colors.orange.shade300),
          ),
          const SizedBox(height: 16),
          const Text(
            "ရှာဖွေမှု ရလဒ်မတွေ့ပါ",
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Color(0xFF2B3550)),
          ),
          const SizedBox(height: 8),
          const Text(
            "အခြား အချက်အလက်များဖြင့်\nပြန်လည် ရှာဖွေကြည့်ပါ။",
            textAlign: TextAlign.center,
            style: TextStyle(fontSize: 14, color: Color(0xFF76799C), height: 1.5),
          ),
        ],
      ),
    );
  }
}