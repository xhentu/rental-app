import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../utils/data_manager.dart'; // Import to use PropertyConfig data sets
import 'property_detail_screen.dart';
import 'package:real_estate_mm/services/api_service.dart';
import 'package:firebase_auth/firebase_auth.dart';

class UploadScreen extends StatefulWidget {
  const UploadScreen({super.key});

  @override
  State<UploadScreen> createState() => _UploadScreenState();
}

class _UploadScreenState extends State<UploadScreen> {
  final _formKey = GlobalKey<FormState>();
  final PageController _pageController = PageController();
  int _currentStep = 0; // Tracks Wizard: Step 0, Step 1, or Step 2

  // --- Central Reactive States ---
  String _propertyType = 'house';
  String _transactionType = 'sale';
  String? _selectedState;
  String? _selectedTownship;
  List<String> _currentTownships = [];
  String _floorType = 'ground';
  String? _selectedDirection;
  String? _selectedLandType;

  // --- Flags & Option Checkboxes ---
  bool _isOwnerDirect = false;
  bool _isDecorated = false;
  bool _isNegotiable = false;
  bool _isPreSale = false; 
  bool _isBankTransfer = false; 
  bool _viberPhone1 = false;
  bool _viberPhone2 = false;

  // --- Input Field Controllers ---
  final TextEditingController _titleController = TextEditingController();
  final TextEditingController _otherTypeController = TextEditingController();
  final TextEditingController _lengthController = TextEditingController();
  final TextEditingController _widthController = TextEditingController();
  final TextEditingController _areaController = TextEditingController();
  final TextEditingController _landLengthController = TextEditingController();
  final TextEditingController _landWidthController = TextEditingController();
  final TextEditingController _landAreaController = TextEditingController();
  final TextEditingController _floorNumController = TextEditingController();
  final TextEditingController _priceController = TextEditingController();
  final TextEditingController _storeyTypeController = TextEditingController();

  final TextEditingController _wardController = TextEditingController();
  final TextEditingController _streetController = TextEditingController();
  final TextEditingController _nearbyController = TextEditingController();

  final TextEditingController _masterBedController = TextEditingController();
  final TextEditingController _singleBedController = TextEditingController();
  final TextEditingController _wcController = TextEditingController();

  final TextEditingController _phone1Controller = TextEditingController();
  final TextEditingController _phone2Controller = TextEditingController();
  final TextEditingController _descriptionController = TextEditingController();

  List<Uint8List> _selectedImages = [];

  @override
  void initState() {
    super.initState();
    _lengthController.addListener(() => _calculateDimensions(_lengthController, _widthController, _areaController));
    _widthController.addListener(() => _calculateDimensions(_lengthController, _widthController, _areaController));
    _landLengthController.addListener(() => _calculateDimensions(_landLengthController, _landWidthController, _landAreaController));
    _landWidthController.addListener(() => _calculateDimensions(_landLengthController, _landWidthController, _landAreaController));
  }

  void _calculateDimensions(TextEditingController len, TextEditingController wid, TextEditingController target) {
    double length = double.tryParse(len.text) ?? 0;
    double width = double.tryParse(wid.text) ?? 0;
    if (length > 0 && width > 0) target.text = (length * width).toStringAsFixed(0);
  }

  void _nextStep() {
    if (_currentStep < 2) {
      _pageController.nextPage(duration: const Duration(milliseconds: 300), curve: Curves.easeInOut);
    }
  }

  void _prevStep() {
    if (_currentStep > 0) {
      _pageController.previousPage(duration: const Duration(milliseconds: 300), curve: Curves.easeInOut);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF7F9FC),
      appBar: AppBar(
        title: Text("စာရင်းသွင်းရန် (အဆင့် ${_currentStep + 1} / 3)"),
        elevation: 0, backgroundColor: Colors.white, foregroundColor: const Color(0xFF2B3550),
        centerTitle: true,
        leading: _currentStep > 0 
            ? IconButton(icon: const Icon(Icons.arrow_back_ios_new_rounded, size: 18), onPressed: _prevStep)
            : null,
      ),
      body: Form(
        key: _formKey,
        child: PageView(
          controller: _pageController,
          physics: const NeverScrollableScrollPhysics(), // Prevent slide skips without validation
          onPageChanged: (idx) => setState(() => _currentStep = idx),
          children: [
            _buildStep1CoreAndLocation(),  // Pages: Sections 1 & 2
            _buildStep2SpecsAndPricing(),  // Pages: Sections 3 & 4
            _buildStep3MediaAndContact(),  // Pages: Section 5 & Submission
          ],
        ),
      ),
      bottomNavigationBar: _buildStickyNavigationBar(),
    );
  }

  Widget _buildStickyNavigationBar() {
    return SafeArea(
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        decoration: const BoxDecoration(
          color: Colors.white,
          border: Border(top: BorderSide(color: Color(0xFFEEF2F6), width: 1)),
        ),
        child: Row(
          children: [
            if (_currentStep > 0)
              Expanded(
                flex: 1,
                child: OutlinedButton(
                  onPressed: _prevStep,
                  style: OutlinedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    side: const BorderSide(color: Color(0xFFD6E4FF)),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  child: const Text("နောက်သို့", style: TextStyle(color: Color(0xFF3577F6), fontWeight: FontWeight.bold)),
                ),
              ),
            if (_currentStep > 0) const SizedBox(width: 12),
            Expanded(
              flex: 2,
              child: ElevatedButton(
                onPressed: _currentStep == 2 ? _submitForm : _nextStep,
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF3577F6), foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  elevation: 0, shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                child: Text(_currentStep == 2 ? "စာရင်းသွင်းမည်" : "ဆက်သွားမည်", style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// =========================================================================
// SECTION CHANNELS - EXTENSION COMPONENTS
// =========================================================================

extension _UploadScreenSteps on _UploadScreenState {
  
  // --- STEP 1 PAGE: Core Setup & Address Mapping ---
  Widget _buildStep1CoreAndLocation() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          _buildCardContainer([
            _buildSectionHeader("အမျိုးအစားရွေးပါ", Icons.home_work_outlined),
            const SizedBox(height: 12),
            _buildPropertyTypeWrap(),
          ]),
          const SizedBox(height: 16),
          _buildCardContainer([
            _buildSectionHeader("တည်နေရာ အချက်အလက်", Icons.location_on_outlined),
            const SizedBox(height: 12),
            _buildLocationDropdownFields(),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(child: _buildInputOutline(_wardController, "ရပ်ကွက်/ကျေးရွာ")),
                const SizedBox(width: 8),
                Expanded(child: _buildInputOutline(_streetController, "လမ်း")),
              ],
            ),
            const SizedBox(height: 12),
            _buildInputOutline(_nearbyController, "တည်နေရာအနီးအနား (ဥပမာ- ပါရမီစိန်ဂေဟာ အနီး)"),
          ]),
        ],
      ),
    );
  }

  // --- STEP 2 PAGE: Physical Specifications & Pricing Details ---
  Widget _buildStep2SpecsAndPricing() {
    bool showFloor = (_propertyType == 'condo' || _propertyType == 'apartment');
    bool isLand = (_propertyType == 'land' || _propertyType == 'warehouse' || _propertyType == 'industrial_zone');
    bool showLandSpecs = (_propertyType == 'house' || isLand);

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          _buildCardContainer([
            _buildSectionHeader("အကျယ်အဝန်း နှင့် အသေးစိတ်", Icons.aspect_ratio_rounded),
            const SizedBox(height: 14),
            if (showLandSpecs) ...[
              const Text("ခြံအကျယ်အဝန်း", style: TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: Color(0xFF5A6B8A))),
              const SizedBox(height: 8),
              Row(
                children: [
                  Expanded(child: _buildLabeledInput(_landLengthController, "အလျား (ပေ)")),
                  const SizedBox(width: 8),
                  Expanded(child: _buildLabeledInput(_landWidthController, "အနံ (ပေ)")),
                  const SizedBox(width: 8),
                  Expanded(child: _buildLabeledInput(_landAreaController, "စတုရန်းပေ")),
                ],
              ),
              const SizedBox(height: 14),
            ],
            if (!isLand) ...[
              const Text("အဆောက်အအုံ အကျယ်အဝန်း", style: TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: Color(0xFF5A6B8A))),
              const SizedBox(height: 8),
              Row(
                children: [
                  Expanded(child: _buildLabeledInput(_lengthController, "အလျား (ပေ)")),
                  const SizedBox(width: 8),
                  Expanded(child: _buildLabeledInput(_widthController, "အနံ (ပေ)")),
                  const SizedBox(width: 8),
                  Expanded(child: _buildLabeledInput(_areaController, "စတုရန်းပေ")),
                ],
              ),
              const SizedBox(height: 14),
            ],
            Row(
              children: [
                Expanded(child: _buildDropdownOutline('မျက်နှာလှည့်', _selectedDirection, PropertyConfig.directions, (v) => setState(() => _selectedDirection = v))),
                if (showLandSpecs) ...[
                  const SizedBox(width: 8),
                  Expanded(child: _buildDropdownOutline('မြေအမျိုးအစား', _selectedLandType, PropertyConfig.landTypes, (v) => setState(() => _selectedLandType = v))),
                ]
              ],
            ),
            if (_propertyType == 'house') ...[
              const SizedBox(height: 12),
              TextFormField(controller: _storeyTypeController, decoration: _getInputDecoration("အိမ်အမျိုးအစားပုံစံ (ဥပမာ - ၁ ထပ်ခွဲ RC)", Icons.roofing_rounded)),
            ],
            if (showFloor) ...[
              const SizedBox(height: 14),
              _buildFloorOptionsSelector(),
            ],
          ]),
          const SizedBox(height: 16),
          _buildCardContainer([
            _buildSectionHeader("စျေးနှုန်း နှင့် ကြော်ငြာခေါင်းစဉ်", Icons.monetization_on_outlined),
            const SizedBox(height: 12),
            TextFormField(controller: _titleController, decoration: _getInputDecoration("ကြော်ငြာခေါင်းစဉ် (Title)", Icons.title_rounded)),
            const SizedBox(height: 14),
            _buildTransactionOptionsGrid(),
            const SizedBox(height: 14),
            TextFormField(
              controller: _priceController, keyboardType: TextInputType.number,
              decoration: _getInputDecoration("တန်ဖိုး", Icons.payments_outlined).copyWith(
                suffixText: (_transactionType == 'sale' || _transactionType == 'buy') ? "သိန်း" : "ကျပ်/တစ်လ",
                suffixStyle: const TextStyle(fontWeight: FontWeight.bold, color: Colors.blueGrey),
              ),
            ),
          ]),
        ],
      ),
    );
  }

  // --- STEP 3 PAGE: Verification Checkbox list, Photos & Contact Handles ---
  Widget _buildStep3MediaAndContact() {
    bool isLand = (_propertyType == 'land' || _propertyType == 'warehouse' || _propertyType == 'industrial_zone');

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          if (!isLand) ...[
            _buildCardContainer([
              _buildSectionHeader("ပါ၀င်သော အခန်းဖွဲ့စည်းမှုများ", Icons.living_outlined),
              const SizedBox(height: 12),
              Wrap(
                spacing: 12, runSpacing: 10,
                children: [
                  _buildCountChip("Master Bedroom (MB)", _masterBedController, Icons.bed_rounded),
                  _buildCountChip("Single Bedroom (SB)", _singleBedController, Icons.single_bed_rounded),
                  _buildCountChip("Bathroom (WC)", _wcController, Icons.bathroom_rounded),
                ],
              ),
            ]),
            const SizedBox(height: 16),
          ],
          _buildCardContainer([
            _buildSectionHeader("ဆက်သွယ်ရန် ဖုန်းနံပါတ်များ", Icons.contact_phone_outlined),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(child: _buildPhoneBlock(_phone1Controller, "ဖုန်းနံပါတ် ၁", _viberPhone1, (v) => setState(() => _viberPhone1 = v))),
                const SizedBox(width: 10),
                Expanded(child: _buildPhoneBlock(_phone2Controller, "ဖုန်းနံပါတ် ၂ (Optional)", _viberPhone2, (v) => setState(() => _viberPhone2 = v))),
              ],
            ),
            const SizedBox(height: 14),
            Wrap(
              spacing: 8, runSpacing: 8,
              children: [
                _buildFilterCheck("ပိုင်ရှင်တိုက်ရိုက်", _isOwnerDirect, (v) => setState(() => _isOwnerDirect = v!)),
                _buildFilterCheck("စျေးညှိနှိုင်းနိုင်", _isNegotiable, (v) => setState(() => _isNegotiable = v!)),
                _buildFilterCheck("ပြင်ဆင်ပြီး", _isDecorated, (v) => setState(() => _isDecorated = v!)),
                _buildFilterCheck("အရစ်ကျရ", _isPreSale, (v) => setState(() => _isPreSale = v!)),
                _buildFilterCheck("ဘဏ်ငွေလွှဲရ", _isBankTransfer, (v) => setState(() => _isBankTransfer = v!)),
              ],
            ),
            const SizedBox(height: 14),
            TextFormField(controller: _descriptionController, maxLines: 3, decoration: _getInputDecoration("အသေးစိတ် ရှင်းလင်းချက် ဖြည့်စွက်ရန် (Optional)", Icons.description_outlined)),
          ]),
          const SizedBox(height: 16),
          _buildCardContainer([
            _buildSectionHeader("ဓာတ်ပုံတင်ရန် (အများဆုံး ၄ ပုံ)", Icons.add_photo_alternate_outlined),
            const SizedBox(height: 12),
            GestureDetector(
              onTap: _pickGalleryImages,
              child: Container(
                height: 110,
                decoration: BoxDecoration(color: const Color(0xFFF1F5F9), borderRadius: BorderRadius.circular(12), border: Border.all(color: const Color(0xFFE2E8F0), width: 1.5)),
                child: _buildImageHorizontalStrip(),
              ),
            )
          ]),
        ],
      ),
    );
  }
}

// =========================================================================
// UI LAYOUT SUB-COMPONENTS & UTILITIES
// =========================================================================

extension _UploadScreenComponentsUX on _UploadScreenState {
  Widget _buildCardContainer(List<Widget> children) {
    return Container(
      decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16), border: Border.all(color: const Color(0xFFEBEFF5), width: 1.2)),
      padding: const EdgeInsets.all(16),
      child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: children),
    );
  }

  Widget _buildSectionHeader(String title, IconData icon) {
    return Row(
      children: [
        Icon(icon, size: 18, color: const Color(0xFF3577F6)),
        const SizedBox(width: 8),
        Text(title, style: const TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF1E293B), fontSize: 15)),
      ],
    );
  }

  Widget _buildPropertyTypeWrap() {
    final types = {
      'house': 'အိမ်', 'condo': 'ကွန်ဒို', 'apartment': 'တိုက်ခန်း',
      'shop_office': 'ဆိုင်/ရုံးခန်း', 'hostel': 'အဆောင်', 'industrial_zone': 'စက်မှုဇုန်',
      'warehouse': 'ဂိုဒေါင်', 'land': 'ခြံ/မြေ', 'other': 'အခြား'
    };
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Wrap(
          spacing: 10, runSpacing: 10,
          children: types.entries.map((e) {
            bool isSel = _propertyType == e.key;
            return ChoiceChip(
              label: Text(e.value), selected: isSel,
              selectedColor: const Color(0xFF3577F6), labelStyle: TextStyle(color: isSel ? Colors.white : const Color(0xFF475569), fontWeight: FontWeight.w600),
              backgroundColor: Colors.white, shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10), side: BorderSide(color: isSel ? Colors.transparent : const Color(0xFFCBD5E1))),
              onSelected: (_) => setState(() => _propertyType = e.key),
            );
          }).toList(),
        ),
        if (_propertyType == 'other') ...[
          const SizedBox(height: 10),
          TextFormField(controller: _otherTypeController, decoration: _getInputDecoration("အခြားအဆောက်အအုံ အမျိုးအစား ရေးပါ", Icons.add_circle_outline_rounded)),
        ]
      ],
    );
  }

  Widget _buildLocationDropdownFields() {
    return Row(
      children: [
        Expanded(
          child: _buildDropdownOutline("ပြည်နယ်/တိုင်း", _selectedState, PropertyConfig.regionData.keys.toList(), (val) {
            setState(() {
              _selectedState = val;
              _currentTownships = val != null ? PropertyConfig.regionData[val]! : [];
              _selectedTownship = null;
            });
          }),
        ),
        const SizedBox(width: 8),
        Expanded(child: _buildDropdownOutline("မြို့နယ်", _selectedTownship, _currentTownships, (val) => setState(() => _selectedTownship = val))),
      ],
    );
  }

  Widget _buildFloorOptionsSelector() {
    return Row(
      children: [
        ...['ground', 'low', 'floor'].map((t) {
          bool isSel = _floorType == t;
          String lbl = t == 'ground' ? 'မြေညီ' : t == 'low' ? 'အထပ်နိမ့်' : 'အထပ်မြင့်';
          return Padding(
            padding: const EdgeInsets.only(right: 8.0),
            child: ChoiceChip(
              label: Text(lbl), selected: isSel, selectedColor: const Color(0xFF475569),
              labelStyle: TextStyle(color: isSel ? Colors.white : const Color(0xFF334155)),
              onSelected: (_) => setState(() => _floorType = t),
            ),
          );
        }),
        const Spacer(),
        SizedBox(width: 80, child: _buildLabeledInput(_floorNumController, "အထပ်နံပါတ်")),
      ],
    );
  }

  Widget _buildTransactionOptionsGrid() {
    final trans = {'sale': 'အရောင်း', 'rent': 'အငှား', 'buy': 'ဝယ်လိုသည်', 'tenant': 'ငှားလိုသည်'};
    return GridView.count(
      crossAxisCount: 2, shrinkWrap: true, physics: const NeverScrollableScrollPhysics(),
      childAspectRatio: 3.5, mainAxisSpacing: 8, crossAxisSpacing: 8,
      children: trans.entries.map((e) {
        bool isSel = _transactionType == e.key;
        return InkWell(
          onTap: () => setState(() => _transactionType = e.key),
          child: Container(
            decoration: BoxDecoration(color: isSel ? const Color(0xFF3577F6) : Colors.white, borderRadius: BorderRadius.circular(10), border: Border.all(color: isSel ? Colors.transparent : const Color(0xFFE2E8F0))),
            alignment: Alignment.center,
            child: Text(e.value, style: TextStyle(fontWeight: FontWeight.bold, color: isSel ? Colors.white : const Color(0xFF475569))),
          ),
        );
      }).toList(),
    );
  }

  Widget _buildPhoneBlock(TextEditingController ctrl, String lbl, bool viberOn, Function(bool) toggleViber) {
    return Column(
      children: [
        _buildLabeledInput(ctrl, lbl),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text("Viber ရရှိနိုင်ပါသလား", style: TextStyle(fontSize: 11, color: Colors.blueGrey)),
            Transform.scale(scale: 0.7, child: Switch(value: viberOn, onChanged: toggleViber, activeColor: Colors.purple)),
          ],
        )
      ],
    );
  }

  Widget _buildCountChip(String label, TextEditingController controller, IconData icon) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 6),
      decoration: BoxDecoration(borderRadius: BorderRadius.circular(12), border: Border.all(color: const Color(0xFFE2E8F0)), color: Colors.white),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 16, color: const Color(0xFF4C71F9)),
          const SizedBox(width: 6),
          Text(label, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
          const SizedBox(width: 10),
          SizedBox(
            width: 35, height: 28,
            child: TextFormField(
              controller: controller, keyboardType: TextInputType.number, maxLength: 2, textAlign: TextAlign.center,
              decoration: const InputDecoration(filled: true, fillColor: Color(0xFFF8FAFC), counterText: "", border: InputBorder.none, contentPadding: EdgeInsets.zero),
            ),
          )
        ],
      ),
    );
  }

  Widget _buildFilterCheck(String title, bool val, Function(bool?) onSel) {
    return FilterChip(label: Text(title), selected: val, selectedColor: const Color(0xFF10B981), onSelected: onSel);
  }

  Future<void> _pickGalleryImages() async {
    final picked = await ImagePicker().pickMultiImage();
    if (picked.isNotEmpty) {
      final remSpace = 4 - _selectedImages.length;
      if (remSpace <= 0) return;
      final bytes = await Future.wait(picked.take(remSpace).map((e) => e.readAsBytes()));
      setState(() => _selectedImages.addAll(bytes));
    }
  }

  Widget _buildImageHorizontalStrip() {
    if (_selectedImages.isEmpty) return const Center(child: Text("ဓာတ်ပုံ ရွေးချယ်ရန်နှိပ်ပါ"));
    return ListView.builder(
      scrollDirection: Axis.horizontal, itemCount: _selectedImages.length,
      itemBuilder: (ctx, idx) => Stack(
        children: [
          Container(margin: const EdgeInsets.only(right: 8), width: 90, height: 90, child: ClipRRect(borderRadius: BorderRadius.circular(8), child: Image.memory(_selectedImages[idx], fit: BoxFit.cover))),
          Positioned(right: 12, top: 4, child: GestureDetector(onTap: () => setState(() => _selectedImages.removeAt(idx)), child: const Icon(Icons.cancel, color: Colors.red))),
        ],
      ),
    );
  }

  InputDecoration _getInputDecoration(String hint, IconData icon) {
    return InputDecoration(
      labelText: hint, prefixIcon: Icon(icon, size: 18),
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
      contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 14),
    );
  }

  Widget _buildInputOutline(TextEditingController controller, String hint) {
    return TextFormField(controller: controller, decoration: InputDecoration(hintText: hint, border: OutlineInputBorder(borderRadius: BorderRadius.circular(12))));
  }

  Widget _buildLabeledInput(TextEditingController controller, String label) {
    return TextFormField(controller: controller, keyboardType: TextInputType.number, decoration: InputDecoration(labelText: label, border: OutlineInputBorder(borderRadius: BorderRadius.circular(10))));
  }

  Widget _buildDropdownOutline(String label, String? val, List<String> items, Function(String?) onChg) {
    return DropdownButtonFormField<String>(
      value: val, isExpanded: true, decoration: InputDecoration(labelText: label, border: OutlineInputBorder(borderRadius: BorderRadius.circular(12))),
      items: items.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(), onChanged: onChg,
    );
  }
}

// =========================================================================
// DATA EXECUTION SUBMISSION LINE
// =========================================================================

extension _UploadScreenSubmit on _UploadScreenState {
  Future<void> _submitForm() async {
    if (_formKey.currentState!.validate()) {
      
      // 1. Firebase Auth ထံမှ လက်ရှိ User ရှိမရှိ အရင်စစ်ဆေးပြီး Token ဆွဲထုတ်ပါ
      final user = FirebaseAuth.instance.currentUser;
      if (user == null) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text("⚠️ ကျေးဇူးပြု၍ အိမ်ခြံမြေစာရင်း မတင်မီ အကောင့်အရင်ဝင်ပေးပါဗျာ။"),
            backgroundColor: Colors.orange
          ),
        );
        return; // အကောင့်မရှိရင် ဆက်သွားခွင့်မပြုပါ
      }

      // ပြောင်းလဲမှုများကို စောင့်ဆိုင်းရန် UI တွင် Loading ပြထားပါမည်
      showDialog(
        context: context,
        barrierDismissible: false,
        builder: (ctx) => const Center(child: CircularProgressIndicator()),
      );

      // Token ကို Expired မဖြစ်စေရန် Force Refresh (true) လုပ်ပြီး ဆွဲထုတ်ယူပါတယ်
      String? firebaseToken = await user.getIdToken(true);

      // 2. ဒေတာများကို Django Payload Schema အတိုင်း စုစည်းခြင်း
      final packedPayload = {
        "title": _titleController.text,
        "offer_type": _transactionType, 
        "property_type": _propertyType == 'other' ? _otherTypeController.text : _propertyType,
        "price": _priceController.text,
        
        "region": _selectedState ?? '',
        "township": _selectedTownship ?? '',
        "quarter": _wardController.text,
        "road": _streetController.text,
        "landmarks": _nearbyController.text.isNotEmpty ? [_nearbyController.text] : [],

        "width": _widthController.text.isEmpty ? "0" : _widthController.text,
        "length": _lengthController.text.isEmpty ? "0" : _lengthController.text,
        "type_of_land": _selectedLandType ?? '',
        "description": _descriptionController.text,

        "owner_direct": _isOwnerDirect,
        "price_negotiable": _isNegotiable,
        "installment_available": _isPreSale,
        "bank_transfer_accepted": _isBankTransfer,

        "contact_phone": _phone1Controller.text,
        "contact_phone1": _phone2Controller.text,
        
        "active_buttons": {
          "call": true,
          "viber": _viberPhone1 || _viberPhone2,
          "whatsapp": false
        },

        "floor_data": {
          "type": _floorType,
          "level": int.tryParse(_floorNumController.text) ?? 1
        },

        "room_structure": {
          "master_bed": int.tryParse(_masterBedController.text) ?? 0,
          "single_bed": int.tryParse(_singleBedController.text) ?? 0,
          "bathroom": int.tryParse(_wcController.text) ?? 0
        },

        "features": {
          "facing": _selectedDirection ?? '',
          "fully_repaired": _isDecorated,
        }
      };

      // lib/screens/upload_screen.dart -> Inside _submitForm()
      print("📤 [FLUTTER OUTBOUND] Preparing to send payload...");
      print("📝 METADATA PACK: ${jsonEncode(packedPayload)}");
      print("🖼️ IMAGES COUNT: ${_selectedImages.length} images in byte queue");

      // 3. ApiService သို့ Token အစစ်အမှန်ဖြင့် ပေးပို့ခြင်း
      bool success = await ApiService.uploadProperty(
        formData: packedPayload,
        images: _selectedImages,
        authToken: firebaseToken ?? '', // 👈 Firebase Token စစ်စစ် ရောက်သွားပါပြီ
      );

      if (!mounted) return;
      Navigator.pop(context); // Loading Dialog ကို ပိတ်ပါ

      if (success) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("✅ အိမ်ခြံမြေစာရင်းကို အောင်မြင်စွာ တင်ပြီးပါပြီ။"), backgroundColor: Colors.green),
        );
        Navigator.of(context).pushAndRemoveUntil(
          MaterialPageRoute(builder: (context) => PropertyDetailScreen(propertyData: packedPayload, images: _selectedImages)), // သို့မဟုတ် မူလအတိုင်း Detail ပြချင်ရင်
          (Route<dynamic> route) => route.isFirst, // ပထမဆုံး Main Screen သို့မဟုတ် Home Screen တစ်ခုပဲ Stack မှာ ကျန်ခဲ့စေရန်
        ); // Form Wizard Screen မှ ထွက်ပြီး ရှေ့ Screen သို့ ပြန်သွားပါမည်
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("❌ ဆာဗာသို့ ဒေတာပေးပို့ခြင်း မအောင်မြင်ပါ။ ပြန်ကြိုးစားကြည့်ပါ။"), backgroundColor: Colors.red),
        );
      }
    }
  }
}