import 'package:flutter/material.dart';

class SearchFilter extends StatefulWidget {
  const SearchFilter({super.key});

  @override
  State<SearchFilter> createState() => _SearchFilterState();
}

class _SearchFilterState extends State<SearchFilter> {
  // 🔴 ၁။ Upload Screen မှ ဒေတာအတိုင်း Map ဖြင့် ပြောင်းလဲကြေညာခြင်း
  final Map<String, List<String>> _regionData = {
    'ရန်ကုန်တိုင်း': [
      'ကမာရွတ်', 'စမ်းချောင်း', 'လှိုင်', 'ဗဟန်း', 'လမ်းမတော်', 'လသာ', 'ပန်းဘဲတန်း', 'ကျောက်တံတား',
      'အလုံ', 'ကြည့်မြင်တိုင်', 'တောင်ဥက္ကလာ', 'မြောက်ဥက္ကလာ', 'သင်္ဃန်းကျွန်း', 'တာမွေ', 'ရန်ကင်း', 'မရမ်းကုန်း',
      'ဒဂုံ', 'ဒဂုံမြို့သစ်(မြောက်ပိုင်း)', 'ဒဂုံမြို့သစ်(တောင်ပိုင်း)', 'ဒဂုံမြို့သစ်(အရှေ့ပိုင်း)', 'ဒဂုံမြို့သစ်(ဆိပ်ကမ်း)',
      'မင်္ဂလာဒုံ', 'အင်းစိန်', 'ရွှေပြည်သာ', 'လှိုင်သာယာ', 'သကေတ', 'ဒေါပုံ', 'မင်္ဂလာတောင်ညွန့်',
      'လှည်းကူး', 'မှော်ဘီ', 'တိုက်ကြီး', 'ထန်းတပင်', 'ကော့မှူး', 'ကွမ်းခြံကုန်း', 'တွံတေး', 'သန်လျင်', 'ကျောက်တန်း', 'သုံးခွ', 'ခရမ်း', 'ကိုကိုးကျွန်း', 'ဆိပ်ကြီးခနောင်တို'
    ],
    'မန္တလေးတိုင်း': [
      'ချမ်းအေးသာစံ', 'အောင်မြေသာစံ', 'မဟာအောင်မြေ', 'ချမ်းမြသာစည်', 'ပြည်ကြီးတံခွန်', 'အမရပူရ', 'ပုသိမ်ကြီး',
      'ပြင်ဦးလွင်', 'ကျောက်ဆည်', 'မိတ္ထီလာ', 'မြင်းခြံ', 'ညောင်ဦး', 'မိုးကုတ်',
      'သပိတ်ကျင်း', 'စဉ့်ကူး', 'မတ္တရာ', 'တံတားဦး', 'စဉ့်ကိုင်', 'မြစ်သား', 'နွားထိုးကြီး', 'မလှိုင်', 'ဝမ်းတွင်း', 'သာစည်', 'ရမည်းသင်း', 'ပျော်ဘွယ်'
    ],
    'နေပြည်တော်': [
      'ဇမ္ဗူသီရိ', 'ဒက္ခိဏသီရိ', 'ဥတ္တရသီရိ', 'ပုဗ္ဗသီရိ', 'ဇေယျာသီရိ', 'ပျဉ်းမနား', 'လယ်ဝေး', 'တပ်ကုန်း'
    ],
    'ပဲခူးတိုင်း': [
      'ပဲခူး', 'တောင်ငူ', 'ပြည်', 'ရွှေကျင်', 'ညောင်လေးပင်', 'ကျောက်တံခါး', 'ဒိုက်ဦး', 'ဖြူး', 'သနပ်ပင်',
      'ကဝ', 'ဝေါ', 'ကြို့ပင်ကောက်', 'ဇီးကုန်း', 'နတ်တလင်း', 'မုန်းညို', 'လက်ပံတန်း', 'သာယာဝတီ', 'အုတ်ဖို', 'ပန်းတောင်း', 'ပေါက်ခေါင်း', 'သဲကုန်း', 'ရွှေတောင်', 'ရေတာရှည်', 'ကျောက်ကြီး', 'အုတ်တွင်း', 'ထန်းတပင်'
    ],
    'ဧရာဝတီတိုင်း': [
      'ပုသိမ်', 'ဟင်္သာတ', 'မအူပင်', 'မြောင်းမြ', 'ဖျာပုံ', 'လပွတ္တာ', 'ကျုံပျော်', 'ဘိုကလေး', 'ဇလွန်',
      'ဓနုဖြူ', 'ကျိုက်လတ်', 'ဒေးဒရဲ', 'မော်လမြိုင်ကျွန်း', 'ဝါးခယ်မ', 'အိမ်မဲ', 'ပန်းတနော်', 'ညောင်တုန်း', 'မြန်အောင်', 'ကြံခင်း', 'အင်္ဂပူ', 'လေးမျက်နှာ', 'သာပေါင်း', 'ငပုတော', 'ကန်ကြီးထောင့်'
    ],
    'စစ်ကိုင်းတိုင်း': [
      'စစ်ကိုင်း', 'မုံရွာ', 'ရွှေဘို', 'ကလေး', 'ကသာ', 'မော်လိုက်', 'ခန္တီး', 'ယင်းမာပင်', 'ရေဦး',
      'မြင်းမူ', 'မြောင်', 'အရာတော်', 'ဘုတလင်', 'ချောင်းဦး', 'ပုလဲ', 'ဆားလင်းကြီး', 'ကနီ', 'ခင်ဦး', 'ဝက်လက်', 'ကန့်ဘလူ', 'ကျွန်းလှ', 'ထီးချိုင့်', 'ဗန်းမောက်', 'အင်းတော်', 'ဝန်းသို', 'ကောလင်း', 'ပင်လည်ဘူး', 'ကလေးဝ', 'မင်းကင်း', 'တမူး', 'ဟုမ္မလင်း', 'လဟယ်', 'လေရှီး', 'နန်းယွန်း'
    ],
    'မကွေးတိုင်း': [
      'မကွေး', 'မင်းဘူး', 'ပခုက္ကူ', 'သရက်', 'ဂန့်ဂေါ', 'အောင်လံ', 'တောင်တွင်းကြီး',
      'ရေနံချောင်း', 'ချောက်', 'နတ်မောက်', 'မြို့သစ်', 'ပွင့်ဖြူ', 'ငဖဲ', 'စလင်း', 'စေတုတ္တရာ', 'ဆိပ်ဖြူ', 'ရေစကြို', 'ပေါက်', 'မြိုင်', 'ဆော', 'ထီးလင်း', 'ကျောက်ထု', 'မင်းတုန်း', 'ကံမ', 'ဆင်ပေါင်ဝဲ'
    ],
    'တနင်္သာရီတိုင်း': [
      'ထားဝယ်', 'မြိတ်', 'ကော့သောင်း', 'လောင်းလုံး', 'သရက်ချောင်း',
      'ရေဖြူ', 'ကျွန်းစု', 'ပုလော', 'တနင်္သာရီ', 'ဘုတ်ပြင်း'
    ],
    'ကချင်ပြည်နယ်': [
      'မြစ်ကြီးနား', 'ဗန်းမော်', 'ပူတာအို', 'မိုးညှင်း', 'ဖားကန့်', 'ရွှေကူ',
      'ဝိုင်းမော်', 'အင်ဂျန်းယန်', 'တနိုင်း', 'ချီဖွေ', 'ဆော့လော်', 'မိုးမောက်', 'မန်စီ', 'မိုးကောင်း', 'မချမ်းဘော', 'ခေါင်လန်ဖူး', 'ဆွမ်ပရာဘွမ်', 'နောင်မွန်း'
    ],
    'ကယားပြည်နယ်': [
      'လွိုင်ကော်', 'ဒီးမော့ဆို', 'ဖရူဆို', 'ဘောလခဲ',
      'ဖားဆောင်း', 'မယ်စဲ့', 'ရှားတော'
    ],
    'ကရင်ပြည်နယ်': [
      'ဘားအံ', 'မြဝတီ', 'ကော့ကရိတ်', 'ဖာပွန်', 'ကြာအင်းဆိပ်ကြီး',
      'လှိုင်းဘွဲ့', 'သံတောင်ကြီး'
    ],
    'ချင်းပြည်နယ်': [
      'ဟားခါး', 'ဖလမ်း', 'မင်းတပ်', 'မတူပီ', 'တီးတိန်', 'ပလက်ဝ',
      'ထန်တလန်', 'တွန်းဇံ', 'ကန်ပက်လက်'
    ],
    'မွန်ပြည်နယ်': [
      'မော်လမြိုင်', 'သထုံ', 'ကျိုက်ထို', 'ရေး', 'ပေါင်', 'ချောင်းဆုံ', 'မုဒုံ', 'ကျိုက်မရော', 'သံဖြူဇရပ်', 'ဘီးလင်း'
    ],
    'ရခိုင်ပြည်နယ်': [
      'စစ်တွေ', 'မောင်တော', 'ကျောက်ဖြူ', 'သံတွဲ', 'မြောက်ဦး', 'အမ်း', 'ဂွ',
      'ပုဏ္ဏားကျွန်း', 'ပေါက်တော', 'ရသေ့တောင်', 'ဘူးသီးတောင်', 'ကျောက်တော်', 'မင်းပြား', 'မြေပုံ', 'ရမ်းဗြဲ', 'မန်အောင်', 'တောင်ကုတ်'
    ],
    'ရှမ်းပြည်နယ်': [
      'တောင်ကြီး', 'လားရှိုး', 'ကျိုင်းတုံ', 'တာချီလိတ်', 'မူဆယ်', 'ကလော', 'အောင်ပန်း', 'ဟိုပုံး', 'ညောင်ရွှေ', 'ပင်းတယ', 'ရွာငံ',
      'အေးသာယာ', 'သီပေါ', 'ကျောက်မဲ', 'နောင်ချို', 'နမ္မတူ', 'နမ့်ဆန်', 'မန်တုံ', 'မိုးမိတ်', 'မဘိမ်း', 'မိုင်းရယ်', 'တန့်ယန်း', 'ကွမ်းလုံ', 'လောက်ကိုင်', 'ကုန်းကြမ်း', 'မိုင်းတုံ', 'မိုင်းဆတ်', 'မိုင်းပျဉ်း', 'မက်မန်း'
    ],
  };



  // 🔴 ၂။ ပြည်နယ်နှင့် မြို့နယ်အတွက် Dynamic Lists များ
  List<String> get _states => ['အားလုံး', ..._regionData.keys];
  List<String> _currentTownships = ['အားလုံး'];

  final List<String> _propertyTypes = ['အားလုံး', 'အိမ်', 'ကွန်ဒို', 'တိုက်ခန်း', 'မြေ', 'ဂိုဒေါင်'];
  final List<String> _transactionTypes = ['အားလုံး', 'အရောင်း', 'အငှား', 'ဝယ်လိုသည်', 'ငှားလိုသည်'];
  final List<String> _directions = [
    'အားလုံး', 'အရှေ့', 'အနောက်', 'တောင်', 'မြောက်',
    'အရှေ့တောင်', 'အနောက်တောင်', 'အရှေ့မြောက်', 'အနောက်မြောက်'
  ];

  // Selected Values
  String _selectedState = 'အားလုံး';
  String _selectedTownship = 'အားလုံး';
  String _selectedType = 'အားလုံး';
  String _selectedTransactionType = 'အားလုံး'; 
  String _selectedDirection = 'အားလုံး'; 

  final TextEditingController _minPriceController = TextEditingController();
  final TextEditingController _maxPriceController = TextEditingController();

  @override
  void dispose() {
    _minPriceController.dispose();
    _maxPriceController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final screenHeight = MediaQuery.of(context).size.height;

    return Container(
      height: screenHeight * 0.90,
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(28)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Drag Handle
          Center(
            child: Container(
              margin: const EdgeInsets.only(top: 12, bottom: 8),
              height: 5,
              width: 50,
              decoration: BoxDecoration(
                color: Colors.grey.shade300,
                borderRadius: BorderRadius.circular(10),
              ),
            ),
          ),

          // Title & Close Button
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  "အသေးစိတ် ရှာဖွေရန်",
                  style: TextStyle(fontSize: 19, fontWeight: FontWeight.w900, color: Color(0xFF2B3550)),
                ),
                GestureDetector(
                  onTap: () => Navigator.pop(context),
                  child: Container(
                    padding: const EdgeInsets.all(6),
                    decoration: BoxDecoration(color: Colors.grey.shade100, shape: BoxShape.circle),
                    child: const Icon(Icons.close_rounded, size: 20, color: Color(0xFF5A6B8A)),
                  ),
                ),
              ],
            ),
          ),
          const Divider(height: 1, thickness: 1.2, color: Color(0xFFEEF0F6)),

          // Scrollable Content
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(20),
              physics: const BouncingScrollPhysics(),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // --- ၁။ တည်နေရာ (State & Township Logic) ---
                  _buildSectionTitle(Icons.location_on_outlined, "တည်နေရာ"),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      Expanded(
                        child: _buildDropdownField(
                          label: "တိုင်း / ပြည်နယ်",
                          value: _selectedState,
                          items: _states,
                          onChanged: (val) {
                            setState(() {
                              _selectedState = val!;
                              // 🔴 ၃။ ပြည်နယ်ပြောင်းတိုင်း မြို့နယ် List ကို Update လုပ်ခြင်း
                              if (_selectedState == 'အားလုံး') {
                                _currentTownships = ['အားလုံး'];
                              } else {
                                _currentTownships = ['အားလုံး', ..._regionData[_selectedState]!];
                              }
                              // ပြည်နယ်ပြောင်းလျှင် ရွေးထားသော မြို့နယ်ကို 'အားလုံး' သို့ ပြန်ပြောင်းပေးမည်
                              _selectedTownship = 'အားလုံး'; 
                            });
                          },
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: _buildDropdownField(
                          label: "မြို့နယ်",
                          value: _selectedTownship,
                          items: _currentTownships, // 🔴 ၄။ Dynamic List ကို အသုံးပြုထားသည်
                          onChanged: (val) => setState(() => _selectedTownship = val!),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 24),

                  // --- ၃။ အရောင်း / အငှား ---
                  _buildSectionTitle(Icons.swap_horiz_rounded, "အရောင်း / အငှား"),
                  const SizedBox(height: 12),
                  Wrap(
                    spacing: 10,
                    runSpacing: 10,
                    children: _transactionTypes.map((type) {
                      final isSelected = _selectedTransactionType == type;
                      return _buildSelectableChip(
                        label: type,
                        isSelected: isSelected,
                        onTap: () => setState(() => _selectedTransactionType = type),
                      );
                    }).toList(),
                  ),
                  const SizedBox(height: 24),

                  // --- ၂။ အိမ်ခြံမြေ အမျိုးအစား ---
                  _buildSectionTitle(Icons.category_outlined, "အမျိုးအစား"),
                  const SizedBox(height: 12),
                  Wrap(
                    spacing: 10,
                    runSpacing: 10,
                    children: _propertyTypes.map((type) {
                      final isSelected = _selectedType == type;
                      return _buildSelectableChip(
                        label: type,
                        isSelected: isSelected,
                        onTap: () => setState(() => _selectedType = type),
                      );
                    }).toList(),
                  ),
                  const SizedBox(height: 24),

                  // --- ၄။ ဈေးနှုန်း ---
                  _buildSectionTitle(Icons.monetization_on_outlined, "တန်ဖိုး (သိန်း/ကျပ်)"),
                  const SizedBox(height: 12),
                  Row(
                    children: [
                      Expanded(child: _buildPriceInput(_minPriceController, "အနည်းဆုံး")),
                      const Padding(
                        padding: EdgeInsets.symmetric(horizontal: 12),
                        child: Text("မှ", style: TextStyle(color: Color(0xFF9AA5B8), fontWeight: FontWeight.bold)),
                      ),
                      Expanded(child: _buildPriceInput(_maxPriceController, "အများဆုံး")),
                    ],
                  ),
                  const SizedBox(height: 24),

                  // --- ၅။ မျက်နှာလှည့် ---
                  _buildSectionTitle(Icons.explore_outlined, "မျက်နှာလှည့်"),
                  const SizedBox(height: 12),
                  _buildDropdownField(
                    label: "မျက်နှာလှည့် ရွေးချယ်ရန်",
                    value: _selectedDirection,
                    items: _directions,
                    onChanged: (val) => setState(() => _selectedDirection = val!),
                  ),
                  
                  const SizedBox(height: 40),
                ],
              ),
            ),
          ),

          // --- Bottom Action Buttons ---
          Container(
            padding: const EdgeInsets.fromLTRB(20, 16, 20, 24),
            decoration: BoxDecoration(
              color: Colors.white,
              boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 15, offset: const Offset(0, -5))],
            ),
            child: Row(
              children: [
                // Reset Button
                TextButton(
                  onPressed: () {
                    setState(() {
                      _selectedState = 'အားလုံး';
                      _currentTownships = ['အားလုံး']; // 🔴 Reset နှိပ်လျှင် မြို့နယ် List ကိုပါ Reset ချမည်
                      _selectedTownship = 'အားလုံး';
                      _selectedType = 'အားလုံး';
                      _selectedTransactionType = 'အားလုံး'; 
                      _selectedDirection = 'အားလုံး'; 
                      _minPriceController.clear();
                      _maxPriceController.clear();
                    });
                  },
                  style: TextButton.styleFrom(
                    foregroundColor: const Color(0xFF5A6B8A),
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                  ),
                  child: const Text("ရှင်းလင်းမည်", style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold)),
                ),
                const SizedBox(width: 16),
                
                // Search Button
                Expanded(
                  child: Container(
                    height: 52,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(14),
                      gradient: const LinearGradient(
                        colors: [Color(0xFF4C71F9), Color(0xFF3558D6)],
                        begin: Alignment.centerLeft,
                        end: Alignment.centerRight,
                      ),
                      boxShadow: [
                        BoxShadow(color: const Color(0xFF4C71F9).withOpacity(0.3), blurRadius: 12, offset: const Offset(0, 5)),
                      ],
                    ),
                    child: ElevatedButton.icon(
                      onPressed: () {
                        final searchFilters = {
                          'state': _selectedState,
                          'township': _selectedTownship,
                          'transactionType': _selectedTransactionType,
                          'propertyType': _selectedType,
                          'minPrice': _minPriceController.text,
                          'maxPrice': _maxPriceController.text,
                          'direction': _selectedDirection,
                        };
                        Navigator.pop(context, searchFilters); 
                      },
                      icon: const Icon(Icons.search_rounded, color: Colors.white, size: 22),
                      label: const Text(
                        "ရှာဖွေမည်",
                        style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.white, letterSpacing: 0.5),
                      ),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.transparent,
                        shadowColor: Colors.transparent,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  // --- Helper Widgets ---

  Widget _buildSectionTitle(IconData icon, String title) {
    return Row(
      children: [
        Icon(icon, size: 20, color: const Color(0xFF4C71F9)),
        const SizedBox(width: 8),
        Text(
          title,
          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Color(0xFF2B3550)),
        ),
      ],
    );
  }

  Widget _buildSelectableChip({required String label, required bool isSelected, required VoidCallback onTap}) {
    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
        decoration: BoxDecoration(
          color: isSelected ? const Color(0xFF3577F6) : Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: isSelected ? Colors.transparent : const Color(0xFFD6E5F8),
            width: 1.2,
          ),
          boxShadow: isSelected
              ? [BoxShadow(color: const Color(0xFF3577F6).withOpacity(0.3), blurRadius: 8, offset: const Offset(0, 3))]
              : [],
        ),
        child: Text(
          label,
          style: TextStyle(
            color: isSelected ? Colors.white : const Color(0xFF5A6B8A),
            fontWeight: isSelected ? FontWeight.bold : FontWeight.w600,
            fontSize: 13.5,
          ),
        ),
      ),
    );
  }

  Widget _buildDropdownField({required String label, required String value, required List<String> items, required Function(String?) onChanged}) {
    return DropdownButtonFormField<String>(
      isExpanded: true,
      value: value,
      items: items.map((e) => DropdownMenuItem(value: e, child: Text(e, style: const TextStyle(fontSize: 14, color: Color(0xFF44476D)), overflow: TextOverflow.ellipsis))).toList(),
      onChanged: onChanged,
      decoration: InputDecoration(
        labelText: label,
        labelStyle: const TextStyle(fontSize: 13, color: Color(0xFF76799C)),
        contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 14),
        filled: true,
        fillColor: const Color(0xFFFAFBFF),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Color(0xFFD6E5F8))),
        enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Color(0xFFD6E5F8))),
        focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Color(0xFF3577F6), width: 1.5)),
      ),
      icon: const Icon(Icons.keyboard_arrow_down_rounded, color: Color(0xFF9AA5B8)),
    );
  }

  Widget _buildPriceInput(TextEditingController controller, String label) {
    return TextFormField(
      controller: controller,
      keyboardType: TextInputType.number,
      style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: Color(0xFF2B3550)),
      decoration: InputDecoration(
        labelText: label,
        labelStyle: const TextStyle(fontSize: 13, color: Color(0xFF76799C)),
        contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 14),
        filled: true,
        fillColor: const Color(0xFFFAFBFF),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Color(0xFFD6E5F8))),
        enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Color(0xFFD6E5F8))),
        focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Color(0xFF3577F6), width: 1.5)),
      ),
    );
  }
}