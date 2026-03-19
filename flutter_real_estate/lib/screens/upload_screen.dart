import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../utils/data_manager.dart';
import 'property_detail_screen.dart';

class UploadScreen extends StatefulWidget {
  const UploadScreen({super.key});
  @override
  State<UploadScreen> createState() => _UploadScreenState();
}

class _UploadScreenState extends State<UploadScreen> {
  final _formKey = GlobalKey<FormState>();

  // --- Variables ---
  String _propertyType = 'house';
  String _transactionType = 'sale';
  String? _selectedState;
  String? _selectedTownship;
  List<String> _currentTownships = [];

  // Floor Logic
  String _floorType = 'ground';

  // Storey / House type
  String? _selectedStoreyType;
  final List<String> _storeyTypes = [
    'တစ်ထပ် အိမ်', 'တစ်ထပ်ခွဲ အိမ်', 'နှစ်ထပ် အိမ်', 'နှစ်ထပ်ခွဲ အိမ်',
    'သုံးထပ် အိမ်', 'သုံးထပ်ခွဲ အိမ်', 'လေးထပ် အိမ်',
  ];

  // (1) Direction (မျက်နှာလှည့်)
  String? _selectedDirection;
  final List<String> _directions = [
    'အရှေ့', 'အနောက်', 'တောင်', 'မြောက်',
    'အရှေ့တောင်', 'အနောက်တောင်', 'အရှေ့မြောက်', 'အနောက်မြောက်'
  ];

  // (2) Land Type (မြေအမျိုးအစား)
  String? _selectedLandType;
  final List<String> _landTypes = [
    'ဂရန်မြေ', 'ဘိုးဘွားပိုင်မြေ', 'ပါမစ်မြေ', 
    'လိုင်စင်မြေ', 'စလစ်မြေ', 'ဂရန်လျှောက်ထားဆဲ','ရွာမြေ','အခြား'
  ];

  // Checkboxes & Toggles
  bool _isOwnerDirect = false;
  bool _isDecorated = false;
  bool _isNegotiable = false;
  bool _isPreSale = false; 
  bool _isBankTransfer = false; 
  bool _viberPhone1 = false;
  bool _viberPhone2 = false;

  // Controllers
  final TextEditingController _titleController = TextEditingController(); // NEW: Title Controller
  final TextEditingController _otherTypeController = TextEditingController();
  final TextEditingController _lengthController = TextEditingController();
  final TextEditingController _widthController = TextEditingController();
  final TextEditingController _areaController = TextEditingController();
  
  // NEW: Land Area Controllers (ခြံအကျယ်အတွက် သီးသန့်)
  final TextEditingController _landLengthController = TextEditingController();
  final TextEditingController _landWidthController = TextEditingController();
  final TextEditingController _landAreaController = TextEditingController();

  final TextEditingController _floorNumController = TextEditingController();
  final TextEditingController _priceController = TextEditingController();

  // Location Controllers
  final TextEditingController _wardController = TextEditingController();
  final TextEditingController _streetController = TextEditingController();
  final TextEditingController _nearbyController = TextEditingController();

  // Amenities Controllers
  final TextEditingController _acController = TextEditingController();
  final TextEditingController _tvController = TextEditingController();
  final TextEditingController _fridgeController = TextEditingController();
  final TextEditingController _masterBedController = TextEditingController();
  final TextEditingController _singleBedController = TextEditingController();
  final TextEditingController _wcController = TextEditingController();

  // Phone Controllers 
  final TextEditingController _phone1Controller = TextEditingController();
  final TextEditingController _phone2Controller = TextEditingController();
  final TextEditingController _descriptionController = TextEditingController();

  // Image picker
  List<Uint8List> _selectedImages = [];

  Future<void> _pickImages() async {
    final picker = ImagePicker();
    final picked = await picker.pickMultiImage();
    if (picked.isNotEmpty) {
      final imagesToPick = picked.length + _selectedImages.length > 4
          ? 4 - _selectedImages.length
          : picked.length;
      final newImages = await Future.wait(
        picked.take(imagesToPick).map((x) => x.readAsBytes()),
      );
      if (mounted) {
        setState(() {
          _selectedImages.addAll(newImages);
          if (_selectedImages.length > 4) {
            _selectedImages = _selectedImages.sublist(0, 4);
          }
        });
      }
    }
  }

  // --- Region Data ---
  final Map<String, List<String>> _regionData ={
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



  @override
  void initState() {
    super.initState();
    _lengthController.addListener(_calculateArea);
    _widthController.addListener(_calculateArea);
    _landLengthController.addListener(_calculateLandArea);
    _landWidthController.addListener(_calculateLandArea);
  }

  void _calculateArea() {
    double length = double.tryParse(_lengthController.text) ?? 0;
    double width = double.tryParse(_widthController.text) ?? 0;
    if (length > 0 && width > 0) {
      _areaController.text = (length * width).toStringAsFixed(0);
    }
  }

  void _calculateLandArea() {
    double length = double.tryParse(_landLengthController.text) ?? 0;
    double width = double.tryParse(_landWidthController.text) ?? 0;
    if (length > 0 && width > 0) {
      _landAreaController.text = (length * width).toStringAsFixed(0);
    }
  }

  @override
  void dispose() {
    _titleController.dispose();
    _lengthController.dispose(); _widthController.dispose(); _areaController.dispose();
    _landLengthController.dispose(); _landWidthController.dispose(); _landAreaController.dispose();
    _otherTypeController.dispose(); _floorNumController.dispose(); _priceController.dispose();
    _wardController.dispose(); _streetController.dispose(); _nearbyController.dispose();
    _acController.dispose(); _tvController.dispose(); _fridgeController.dispose();
    _masterBedController.dispose(); _singleBedController.dispose(); _wcController.dispose();
    _phone1Controller.dispose(); _phone2Controller.dispose(); _descriptionController.dispose();
    super.dispose();
  }

  // --- Reset Form Method ---
  void _resetForm() {
    _formKey.currentState?.reset();

    _titleController.clear();
    _otherTypeController.clear();
    _lengthController.clear(); _widthController.clear(); _areaController.clear();
    _landLengthController.clear(); _landWidthController.clear(); _landAreaController.clear();
    _floorNumController.clear();
    _priceController.clear();
    _wardController.clear(); _streetController.clear(); _nearbyController.clear();
    _acController.clear(); _tvController.clear(); _fridgeController.clear();
    _masterBedController.clear(); _singleBedController.clear(); _wcController.clear();
    _phone1Controller.clear(); _phone2Controller.clear(); _descriptionController.clear();

    setState(() {
      _propertyType = 'house';
      _transactionType = 'sale';
      _selectedState = null;
      _selectedTownship = null;
      _currentTownships = [];
      _floorType = 'ground';
      _selectedStoreyType = null;
      _selectedDirection = null;
      _selectedLandType = null;
      _isOwnerDirect = false;
      _isDecorated = false;
      _isNegotiable = false;
      _isPreSale = false;
      _isBankTransfer = false;
      _viberPhone1 = false;
      _viberPhone2 = false;
      _selectedImages.clear();
    });
  }

  // --- Submit Method ---
  void _submitForm() {
    if (_formKey.currentState!.validate()) {
      // Custom Validation for Title
      if (_titleController.text.trim().isEmpty) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('ကျေးဇူးပြု၍ ခေါင်းစဉ် (Title) ထည့်ပါ'), backgroundColor: Colors.redAccent),
        );
        return;
      }

      String propType = _propertyType == 'other' ? _otherTypeController.text : _propertyType;
      bool isLandType = (_propertyType == 'land' || _propertyType == 'warehouse' || _propertyType == 'industrial_zone');

      String amenityInfo = "";
      if (!isLandType) {
        if (_masterBedController.text.isNotEmpty) amenityInfo += "MB:${_masterBedController.text} ";
        if (_singleBedController.text.isNotEmpty) amenityInfo += "SB:${_singleBedController.text} ";
      }

      String floorInfo = (_propertyType == 'condo' || _propertyType == 'apartment')
          ? "| $_floorType (${_floorNumController.text})" : "";

      String extraSpecs = "";
      if (_selectedDirection != null) extraSpecs += "မျက်နှာလှည့်: $_selectedDirection | ";
      if (_selectedLandType != null) extraSpecs += "မြေ : $_selectedLandType | ";

      // ဖုန်းနံပါတ် အချက်အလက်
      String contactInfo = "${_phone1Controller.text} ${_viberPhone1 ? '(Viber)' : ''}";
      if (_phone2Controller.text.isNotEmpty) {
        contactInfo += ", ${_phone2Controller.text} ${_viberPhone2 ? '(Viber)' : ''}";
      }

      // အကျယ်အဝန်း အချက်အလက်
      String finalAreaInfo = isLandType ? "${_landAreaController.text} sqft" : "${_areaController.text} sqft";

      // တည်နေရာကို ပြည်နယ်/တိုင်း၊ မြို့နယ်၊ ရပ်ကွက်၊ လမ်း အစဉ်လိုက် စီစဉ်ခြင်း
      List<String> locationParts = [];
      if (_selectedState != null && _selectedState!.isNotEmpty) locationParts.add(_selectedState!);
      if (_selectedTownship != null && _selectedTownship!.isNotEmpty) locationParts.add(_selectedTownship!);
      if (_wardController.text.trim().isNotEmpty) locationParts.add("${_wardController.text.trim()} ရပ်ကွက်");
      if (_streetController.text.trim().isNotEmpty) locationParts.add("${_streetController.text.trim()} လမ်း");
      
      String finalLocation = locationParts.join('၊ '); 
      
      if (_nearbyController.text.trim().isNotEmpty) {
        finalLocation += " (${_nearbyController.text.trim()} အနီး)";
      }

      // Data များကို Map သို့ ပြောင်းခြင်း
      final newProp = {
        "id": DateTime.now().millisecondsSinceEpoch.toString(), 
        "title": _titleController.text, 
        "price": _priceController.text,
        "location": finalLocation, 
        "image": "https://via.placeholder.com/400x300", 
        "localImages": List<Uint8List>.from(_selectedImages), 
        "type": _getTransactionLabel(),
        "propertyType": propType, 
        "specs": "$finalAreaInfo $floorInfo | $extraSpecs $amenityInfo",
        "phone": contactInfo,
        "isBankTransfer": _isBankTransfer,
        "isOwnerDirect": _isOwnerDirect,
        "isNegotiable": _isNegotiable,
        "isDecorated": _isDecorated,
        "isPreSale": _isPreSale,
        "description": _descriptionController.text,
      };

      addProperty(newProp);

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('စာရင်းသွင်းခြင်း အောင်မြင်ပါသည်'), backgroundColor: Color(0xFF4C71F9)),
      );
      
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => PropertyDetailScreen(
            propertyData: newProp,
            images: List<Uint8List>.from(_selectedImages),
          ),
        ),
      ).then((_) {
        _resetForm(); 
      });
    }
  }

  String _getTransactionLabel() {
    switch (_transactionType) {
      case 'sale': return 'For Sale';
      case 'rent': return 'For Rent';
      case 'buy': return 'Want to Buy';
      case 'tenant': return 'Want to Rent';
      default: return 'For Sale';
    }
  }

  @override
  Widget build(BuildContext context) {
    bool showFloorOptions = (_propertyType == 'condo' || _propertyType == 'apartment');
    // မြေကွက်သက်သက်ဖြစ်သောကြောင့် အဆောက်အအုံ Area နှင့် Amenities များ မပြပါ
    bool isLandType = (_propertyType == 'land' || _propertyType == 'warehouse' || _propertyType == 'industrial_zone');
    bool showAmenities = !isLandType;
    bool showLandTypeOptions = (_propertyType == 'house' || isLandType);

    return Scaffold(
      backgroundColor: Colors.transparent,
      appBar: AppBar(
        title: const Text("စာရင်းသွင်းရန်"),
        elevation: 0, 
        backgroundColor: Colors.white.withOpacity(0.95),
        foregroundColor: const Color(0xFF2B3550),
        toolbarHeight: 60,
        centerTitle: true,
        titleTextStyle: const TextStyle(
          fontSize: 18.5, fontWeight: FontWeight.bold, color: Color(0xFF2B3550), letterSpacing: 0.5,
        ),
        shape: const RoundedRectangleBorder(
          borderRadius: BorderRadius.vertical(bottom: Radius.circular(20)),
        ),
      ),
      extendBodyBehindAppBar: true, 
      body: Container(
        width: double.infinity,
        height: double.infinity,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFFF4F7FF), Color(0xFFE8F0FE), Color(0xFFFAFBFF)],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: SafeArea(
          bottom: false, 
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 20),
            child: Form(
              key: _formKey,
              child: AnimatedContainer(
                duration: const Duration(milliseconds: 400),
                curve: Curves.fastOutSlowIn,
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(24),
                  boxShadow: [
                    BoxShadow(color: const Color(0xFF3577F6).withOpacity(0.06), blurRadius: 20, spreadRadius: 4, offset: const Offset(0, 8)),
                  ],
                ),
                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 25),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    // 1. အမျိုးအစား နှင့် ခေါင်းစဉ် (Title)
                    _SectionTitle(title: "အမျိုးအစားရွေးပါ", icon: Icons.home_work_outlined),
                    const SizedBox(height: 5),
                    SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      physics: const BouncingScrollPhysics(),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          _buildTypeChip(Icons.home_work_rounded, 'အိမ်', 'house'),
                          _buildTypeChip(Icons.domain_rounded, 'ကွန်ဒို', 'condo'),
                          _buildTypeChip(Icons.apartment_rounded, 'တိုက်ခန်း', 'apartment'),
                          _buildTypeChip(Icons.night_shelter, 'အဆောင်', 'hostel'),
                          _buildTypeChip(Icons.precision_manufacturing_rounded, 'စက်မှုဇုန်', 'industrial_zone'),
                          _buildTypeChip(Icons.factory_rounded, 'ဂိုဒေါင်', 'warehouse'),
                          _buildTypeChip(Icons.landscape_rounded, 'ခြံ/မြေ', 'land'),
                          _buildTypeChip(Icons.more_horiz_rounded, 'အခြား', 'other'),
                          
                          if (_propertyType == 'other')
                            Container(
                              width: 180,
                              margin: const EdgeInsets.only(left: 2),
                              child: _buildSmallInput(_otherTypeController, "ဟိုတယ်/ကျောင်း...", maxLength: 20),
                            ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 16),
                    
                    // NEW: Title Input Box
                    TextFormField(
                      controller: _titleController,
                      style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: Color(0xFF2B4B84)),
                      decoration: InputDecoration(
                        labelText: "ခေါင်းစဉ် (Title)",
                        hintText: "ဥပမာ - လှိုင်မြို့နယ်ရှိ ပြင်ဆင်ပြီး တိုက်ခန်းအရောင်း",
                        hintStyle: const TextStyle(fontSize: 13, color: Color(0xFF9AA5B8), fontWeight: FontWeight.normal),
                        labelStyle: const TextStyle(fontSize: 13, color: Color(0xFF76799C)),
                        prefixIcon: const Icon(Icons.title_rounded, color: Color(0xFF9AA5B8), size: 20),
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                        enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Color(0xFFD6E5F8))),
                        focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Color(0xFF3577F6), width: 1.5)),
                        filled: true,
                        fillColor: const Color(0xFFFAFBFF),
                      ),
                    ),
                    const SizedBox(height: 24),

                    // 2. တည်နေရာ နှင့် စျေးနှုန်း (Transaction 2x2 Grid)
                    _SectionTitle(title: "တည်နေရာ & စျေးနှုန်း", icon: Icons.location_on_outlined),
                    const SizedBox(height: 10),
                    Container(
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(18),
                        gradient: const LinearGradient(
                          colors: [Color(0xFFF9FBFF), Color(0xFFF0F5FF)],
                          begin: Alignment.topLeft, end: Alignment.bottomRight,
                        ),
                        border: Border.all(color: const Color(0xFFE4ECFB), width: 1.2),
                      ),
                      padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 14),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          _buildRegionTownshipRow(),
                          const SizedBox(height: 14),
                          Column(
                                crossAxisAlignment: CrossAxisAlignment.stretch,
                                children: [
                                  Row(
                                    children: [
                                      Expanded(child: _buildSmallInput(_wardController, "ရပ်ကွက်/ကျေးရွာ")),
                                      const SizedBox(width: 8), 
                                      Expanded(child: _buildSmallInput(_streetController, "လမ်း")),
                                    ],
                                  ),
                                  const SizedBox(height: 14), 
                                  _buildSmallInput(_nearbyController, "တည်နေရာ - ဥပမာ (ပါရမီစိန်‌ဂေဟာ အနီး)"), 
                                ],
                              ),
                                              
                          const SizedBox(height: 14),
                          SizedBox(
                            height: 48,
                            child: ElevatedButton.icon(
                              onPressed: () {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  const SnackBar(content: Text('Google Map စနစ် မကြာမီလာမည်။')),
                                );
                              },
                              icon: const Icon(Icons.map_rounded, size: 20, color: Colors.white),
                              label: const Text(
                                "Google Map တွင် နေရာရွေးရန်",
                                style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold, letterSpacing: 0.3),
                              ),
                              style: ElevatedButton.styleFrom(
                                backgroundColor: const Color(0xFF9AA5B8), 
                                foregroundColor: Colors.white,
                                elevation: 0,
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                              ),
                            ),
                          ),
                          const SizedBox(height: 20),
                          
                          // NEW: Transaction Grid (2x2) and Price
                          _buildTransactionAndPriceSection(),
                        ],
                      ),
                    ),
                    const SizedBox(height: 20),

                    // 3. အကျယ်အဝန်း နှင့် အသေးစိတ် (Logic Applied for Land vs Building)
                    _SectionTitle(title: "အကျယ်အဝန်း နှင့် အသေးစိတ်", icon: Icons.aspect_ratio_rounded),
                    const SizedBox(height: 10),
                    
                    // ခြံမြေ Area 
                    if (showLandTypeOptions) ...[
                      const Text("ခြံအကျယ်အဝန်း", style: TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: Color(0xFF5A6B8A))),
                      const SizedBox(height: 8),
                      Row(
                        children: [
                          Expanded(child: _buildLabeledInput(_landLengthController, "အလျား (ပေ)", maxLength: 5)),
                          const SizedBox(width: 8),
                          Expanded(child: _buildLabeledInput(_landWidthController, "အနံ (ပေ)", maxLength: 5)),
                          const SizedBox(width: 8),
                          Expanded(child: _buildLabeledInput(_landAreaController, "ဧရိယာ (စတုရန်းပေ)", maxLength: 6)),
                        ],
                      ),
                      const SizedBox(height: 14),
                    ],

                    // အဆောက်အအုံ Area (ခြံသက်သက် မဟုတ်မှသာ ပေါ်မည်)
                    if (!isLandType) ...[
                      const Text("အဆောက်အအုံ အကျယ်အဝန်း", style: TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: Color(0xFF5A6B8A))),
                      const SizedBox(height: 8),
                      Row(
                        children: [
                          Expanded(child: _buildLabeledInput(_lengthController, "အလျား (ပေ)", maxLength: 5)),
                          const SizedBox(width: 8),
                          Expanded(child: _buildLabeledInput(_widthController, "အနံ (ပေ)", maxLength: 5)),
                          const SizedBox(width: 8),
                          Expanded(child: _buildLabeledInput(_areaController, "ဧရိယာ (စတုရန်းပေ)", maxLength: 6)),
                        ],
                      ),
                      const SizedBox(height: 14),
                    ],

                    Row(
                      children: [
                        Expanded(
                          child: _buildDropdownField(
                            label: 'မျက်နှာလှည့်',
                            value: _selectedDirection,
                            items: _directions,
                            onChanged: (v) => setState(() => _selectedDirection = v),
                          ),
                        ),
                        if (showLandTypeOptions) ...[
                          const SizedBox(width: 10),
                          Expanded(
                            child: _buildDropdownField(
                              label: 'မြေအမျိုးအစား',
                              value: _selectedLandType,
                              items: _landTypes,
                              onChanged: (v) => setState(() => _selectedLandType = v),
                            ),
                          ),
                        ]
                      ],
                    ),

                    if (_propertyType == 'house') ...[
                      const SizedBox(height: 14),
                      _buildDropdownField(
                        label: 'အိမ်အမျိုးအစား',
                        value: _selectedStoreyType,
                        items: _storeyTypes,
                        onChanged: (v) => setState(() => _selectedStoreyType = v),
                      ),
                    ],
                    
                    if (showFloorOptions) ...[
                      const SizedBox(height: 16),
                      SingleChildScrollView(
                        scrollDirection: Axis.horizontal,
                        child: Row(
                          children: [
                            _buildFloorChip('မြေညီထပ်', 'ground', Icons.align_vertical_bottom_rounded),
                            _buildFloorChip('အထပ်နိမ့်', 'low', Icons.filter_1_rounded),
                            _buildFloorChip('အထပ်မြင့်', 'floor', Icons.filter_9_plus_rounded),
                            const SizedBox(width: 8),
                            SizedBox(width: 90, child: _buildSmallInput(_floorNumController, "ဘယ်နှစ်ထပ်?", maxLength: 2)),
                          ],
                        ),
                      ),
                    ],

                    if (showAmenities) ...[
                      const SizedBox(height: 18),
                      _SectionTitle(title: "ပါ၀င်သော ပစ္စည်းများ", icon: Icons.living_outlined),
                      const SizedBox(height: 8),
                      Wrap(
                        spacing: 12, runSpacing: 10,
                        children: [
                          _buildAmenityChip("MB", _masterBedController, Icons.bed_rounded),
                          _buildAmenityChip("SB", _singleBedController, Icons.king_bed_rounded),
                          _buildAmenityChip("WC", _wcController, Icons.bathroom_rounded),
                          //_buildAmenityChip("AC", _acController, Icons.ac_unit_rounded),
                          //_buildAmenityChip("TV", _tvController, Icons.tv_rounded),
                          //_buildAmenityChip("FR", _fridgeController, Icons.kitchen_rounded),
                        ],
                      ),
                    ],

                    const SizedBox(height: 20),
                    const Divider(height: 1, thickness: 1.2, color: Color(0xFFEEF0F6)),
                    const SizedBox(height: 20),
                    
                    _SectionTitle(title: "ဆက်သွယ်ရန်", icon: Icons.contact_phone_outlined),
                    const SizedBox(height: 12),
                    Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Expanded(
                          child: _buildPhoneContactField(
                            controller: _phone1Controller, label: "ဖုန်းနံပါတ် ၁",
                            hasViber: _viberPhone1, onViberToggle: (v) => setState(() => _viberPhone1 = v),
                          ),
                        ),
                        const SizedBox(width: 14),
                        Expanded(
                          child: _buildPhoneContactField(
                            controller: _phone2Controller, label: "ဖုန်းနံပါတ် ၂ (Optional)",
                            hasViber: _viberPhone2, onViberToggle: (v) => setState(() => _viberPhone2 = v),
                          ),
                        ),
                      ],
                    ),

                    const SizedBox(height: 16),
                    Wrap(
                      spacing: 8, runSpacing: 8,
                      children: [
                        _buildCheckboxChip("ပိုင်ရှင်တိုက်ရိုက်", _isOwnerDirect, (v) => setState(() => _isOwnerDirect = v ?? false)),
                        _buildCheckboxChip("စျေးညှိနှိုင်းနိုင်", _isNegotiable, (v) => setState(() => _isNegotiable = v ?? false)),
                        _buildCheckboxChip("ပြင်ဆင်ပြီး", _isDecorated, (v) => setState(() => _isDecorated = v ?? false)),
                        _buildCheckboxChip("အရစ်ကျရ", _isPreSale, (v) => setState(() => _isPreSale = v ?? false)),
                        _buildCheckboxChip("ဘဏ်ငွေလွှဲလက်ခံသည်", _isBankTransfer, (v) => setState(() => _isBankTransfer = v ?? false)),
                      ],
                    ),
                    const SizedBox(height: 16),
                    
                    TextFormField(
                      controller: _descriptionController,
                      maxLines: 3,
                      style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w500, color: Color(0xFF2B4B84)),
                      decoration: InputDecoration(
                        labelText: "အသေးစိတ် အချက်အလက်များ (Optional)",
                        labelStyle: const TextStyle(fontSize: 12.5, color: Color(0xFF76799C)),
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(14)),
                        enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(14), borderSide: const BorderSide(color: Color(0xFFD6E5F8))),
                        focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(14), borderSide: const BorderSide(color: Color(0xFF3577F6), width: 1.5)),
                        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
                        filled: true,
                        fillColor: const Color(0xFFF9FBFF),
                      ),
                    ),
                    
                    const SizedBox(height: 20),
                    _SectionTitle(title: "ဓာတ်ပုံထည့်ရန် (အများဆုံး ၄ ပုံ)", icon: Icons.add_photo_alternate_outlined),
                    const SizedBox(height: 10),
                    Container(
                      decoration: BoxDecoration(
                        color: const Color(0xFFF5F8FF),
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(color: const Color(0xFFD6E5F8), style: BorderStyle.solid, width: 1.5),
                      ),
                      width: double.infinity, 
                      height: 130,
                      padding: const EdgeInsets.all(8),
                      child: InkWell(
                        borderRadius: BorderRadius.circular(14),
                        onTap: _pickImages,
                        child: _buildImageGallery(),
                      ),
                    ),
                    const SizedBox(height: 28),

                    // Submit Button
                    Container(
                      height: 54,
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(14),
                        gradient: const LinearGradient(
                          colors: [Color(0xFF4C71F9), Color(0xFF3558D6)],
                          begin: Alignment.centerLeft, end: Alignment.centerRight,
                        ),
                        boxShadow: [
                          BoxShadow(color: const Color(0xFF4C71F9).withOpacity(0.3), blurRadius: 12, offset: const Offset(0, 6)),
                        ],
                      ),
                      child: ElevatedButton.icon(
                        icon: const Icon(Icons.cloud_upload_rounded, size: 22, color: Colors.white),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.transparent,
                          shadowColor: Colors.transparent,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                        ),
                        label: const Text(
                          "အချက်အလက်များ စာရင်းသွင်းမည်",
                          style: TextStyle(color: Colors.white, fontSize: 16.5, fontWeight: FontWeight.bold, letterSpacing: 0.5),
                        ),
                        onPressed: _submitForm,
                      ),
                    ),
                    const SizedBox(height: 10),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }

  // --- Custom Helper Widgets ---

  Widget _buildImageGallery() {
    if (_selectedImages.isEmpty) {
      return Center(
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const [
            Icon(Icons.add_a_photo, size: 29, color: Colors.indigo),
            SizedBox(width: 7),
            Text(
              "ဓာတ်ပုံ သို့ ရွေးရန်",
              style: TextStyle(fontSize: 14, color: Color(0xFF616AAC)),
            ),
          ],
        ),
      );
    }
    return ListView.builder(
      scrollDirection: Axis.horizontal,
      itemCount: _selectedImages.length,
      itemBuilder: (context, idx) {
        return Stack(
          children: [
            Container(
              margin: const EdgeInsets.only(right: 9),
              width: 92,
              height: 92,
              child: ClipRRect(
                borderRadius: BorderRadius.circular(11),
                child: Image.memory(
                  _selectedImages[idx],
                  fit: BoxFit.cover,
                  width: 92,
                  height: 92,
                ),
              ),
            ),
            Positioned(
              right: 3,
              top: 3,
              child: InkWell(
                onTap: () {
                  setState(() {
                    _selectedImages.removeAt(idx);
                  });
                },
                child: Container(
                  decoration: const BoxDecoration(
                    color: Colors.black38,
                    shape: BoxShape.circle,
                  ),
                  child: const Icon(Icons.close, color: Colors.white, size: 18),
                ),
              ),
            ),
          ],
        );
      },
    );
  }

  Widget _buildRegionTownshipRow() {
    return Row(
      children: [
        Expanded(
          flex: 1,
          child: _buildDropdownField(
            label: "ပြည်နယ်/တိုင်း",
            value: _selectedState,      
            items: _regionData.keys.toList(),
            onChanged: (val) {
              setState(() {
                _selectedState = val;
                if (val != null && _regionData.containsKey(val)) {
                  _currentTownships = _regionData[val]!;
                } else {
                  _currentTownships = [];
                }
                _selectedTownship = null;
              });
            },
          ),
        ),
        const SizedBox(width: 8),
        Expanded(
          flex: 1,
          child: _buildDropdownField(
            label: "မြို့နယ်",
            value: _selectedTownship,
            items: _currentTownships,
            onChanged: (val) => setState(() => _selectedTownship = val),
          ),
        ),
      ],
    );
  }

  // NEW: Transaction Grid & Price (Full Width)
  Widget _buildTransactionAndPriceSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        // Grid 2x2
        Row(
          children: [
            Expanded(child: _buildTransactionChip('အရောင်း', 'sale', Icons.sell_rounded)),
            const SizedBox(width: 8),
            Expanded(child: _buildTransactionChip('အငှား', 'rent', Icons.apartment_rounded)),
          ],
        ),
        const SizedBox(height: 8),
        Row(
          children: [
            Expanded(child: _buildTransactionChip('ဝယ်လိုသည်', 'buy', Icons.shopping_bag_rounded)),
            const SizedBox(width: 8),
            Expanded(child: _buildTransactionChip('ငှားလိုသည်', 'tenant', Icons.key_rounded)),
          ],
        ),
        const SizedBox(height: 16),
        // Full Width Price
        TextFormField(
          controller: _priceController,
          keyboardType: TextInputType.number,
          style: const TextStyle(fontSize: 16, color: Color(0xFF2B4B84), fontWeight: FontWeight.bold),
          decoration: InputDecoration(
            labelText: "တန်ဖိုး",
            labelStyle: const TextStyle(fontSize: 13, color: Color(0xFF28577B)),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: Color(0xFFD6E5F8), width: 1.1),
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: Color(0xFFD6E5F8), width: 1.1),
            ),
            focusedBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: Color(0xFF3577F6), width: 1.5),
            ),
            contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16), 
            filled: true,
            fillColor: Colors.white,
            suffixText: (_transactionType == 'sale' || _transactionType == 'buy') ? "သိန်း" : "ကျပ်/တစ်လ",
            suffixStyle: const TextStyle(fontSize: 12, color: Colors.blueGrey, fontWeight: FontWeight.w600),
            prefixIcon: const Icon(Icons.monetization_on_rounded, color: Color(0xFF3577F6), size: 20),
          ),
          maxLength: 11,
          buildCounter: (context, {required currentLength, maxLength, required isFocused}) => null,
          validator: (val) {
            if (val == null || val.trim().isEmpty) return "တန်ဖိုးထည့်ပါ";
            return null;
          },
        ),
      ],
    );
  }

  Widget _buildDropdownField({
    required String label, required String? value, required List<String> items, required Function(String?) onChanged,
  }) {
    return DropdownButtonFormField<String>(
      isExpanded: true,
      decoration: InputDecoration(
        labelText: label,
        labelStyle: const TextStyle(fontSize: 12.5, color: Color(0xFF28577B)),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Color(0xFFD6E5F8), width: 1.1)),
        enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Color(0xFFD6E5F8), width: 1.1)),
        focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Color(0xFF3577F6), width: 1.5)),
        contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 14), 
        filled: true, fillColor: Colors.white,
      ),
      style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: Color(0xFF304865)),
      initialValue: value,
      items: items.map((e) => DropdownMenuItem<String>(
            value: e, child: Text(e, style: const TextStyle(fontSize: 13.5, color: Color(0xFF44476D))),
          )).toList(),
      onChanged: onChanged,
    );
  }

  Widget _buildTypeChip(IconData icon, String label, String val) {
    final isSelected = _propertyType == val;
    return GestureDetector(
      onTap: () => setState(() => _propertyType = val),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 250),
        curve: Curves.easeOut,
        margin: const EdgeInsets.only(right: 4), // Set spacing smaller
        width: 60,  // Adjust size to fix screen perfectly
        height: 60, 
        decoration: BoxDecoration(
          color: isSelected ? const Color(0xFF4C71F9) : Colors.white,
          borderRadius: BorderRadius.circular(14),
          border: Border.all(
            color: isSelected ? const Color(0xFF4C71F9) : const Color(0xFFD6E5F8),
            width: isSelected ? 0 : 1.0,
          ),
          boxShadow: isSelected
              ? [BoxShadow(color: const Color(0xFF4C71F9).withOpacity(0.35), blurRadius: 10, offset: const Offset(0, 4))]
              : [const BoxShadow(color: Color(0x0A000000), blurRadius: 6, offset: Offset(0, 2))],
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 20, color: isSelected ? Colors.white : const Color(0xFF5A6B8A)),
            const SizedBox(height: 4),
            Text(
              label,
              style: TextStyle(
                color: isSelected ? Colors.white : const Color(0xFF5A6B8A),
                fontSize: 10.5,
                fontWeight: isSelected ? FontWeight.bold : FontWeight.w600,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTransactionChip(String title, String val, IconData icon) {
    final isSelected = _transactionType == val;
    return GestureDetector(
      onTap: () => setState(() => _transactionType = val),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        height: 48,
        decoration: BoxDecoration(
          color: isSelected ? const Color(0xFF3577F6) : Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: isSelected ? Colors.transparent : const Color(0xFFD6E5F8), width: 1.2),
          boxShadow: isSelected ? [BoxShadow(color: const Color(0xFF3577F6).withOpacity(0.25), blurRadius: 6, offset: const Offset(0, 3))] : [],
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 18, color: isSelected ? Colors.white : const Color(0xFF5A6B8A)),
            const SizedBox(width: 6),
            Text(title, style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: isSelected ? Colors.white : const Color(0xFF5A6B8A))),
          ],
        ),
      ),
    );
  }

  Widget _buildFloorChip(String title, String val, IconData icon) {
    final isSelected = _floorType == val;
    return Padding(
      padding: const EdgeInsets.only(right: 8.0),
      child: FilterChip(
        showCheckmark: false,
        label: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 14, color: isSelected ? Colors.white : const Color(0xFF40599D)),
            const SizedBox(width: 4),
            Text(title, style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: isSelected ? Colors.white : const Color(0xFF40599D))),
          ],
        ),
        selected: isSelected,
        selectedColor: const Color(0xFF3577F6),
        backgroundColor: Colors.white,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(10), 
          side: BorderSide(color: isSelected ? Colors.transparent : const Color(0xFFD6E5F8))
        ),
        onSelected: (_) => setState(() => _floorType = val),
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
      ),
    );
  }

  Widget _buildCheckboxChip(String title, bool value, Function(bool?) onChanged) {
    return FilterChip(
      showCheckmark: value, 
      checkmarkColor: Colors.white,
      label: Text(title, style: TextStyle(fontSize: 13, fontWeight: FontWeight.w500, color: value ? Colors.white : const Color(0xFF4A5568))),
      selected: value,
      selectedColor: const Color(0xFF10B981), 
      backgroundColor: Colors.white,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(10),
        side: BorderSide(color: value ? Colors.transparent : const Color(0xFFD6E5F8)),
      ),
      onSelected: (val) => onChanged(val),
      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 8),
    );
  }

  Widget _buildPhoneContactField({required TextEditingController controller, required String label, required bool hasViber, required Function(bool) onViberToggle}) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: const Color(0xFFD6E5F8), width: 1.1),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildLabeledInput(controller, label, maxLength: 14),
          const SizedBox(height: 8),
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(4),
                decoration: BoxDecoration(color: hasViber ? Colors.purple.withOpacity(0.1) : Colors.grey.shade100, shape: BoxShape.circle),
                child: Icon(Icons.wechat, size: 16, color: hasViber ? Colors.purple : Colors.grey.shade500),
              ),
              const SizedBox(width: 6),
              Text("Viber", style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: hasViber ? Colors.purple.shade700 : Colors.grey.shade600)),
              const Spacer(),
              SizedBox(
                height: 24, width: 36,
                child: Switch(value: hasViber, onChanged: onViberToggle, activeThumbColor: Colors.purple),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildLabeledInput(TextEditingController controller, String label, {int? maxLength}) {
    return TextFormField(
      controller: controller,
      keyboardType: TextInputType.number,
      maxLength: maxLength,
      style: const TextStyle(fontSize: 14, color: Color(0xFF233B6F), fontWeight: FontWeight.bold),
      decoration: InputDecoration(
        labelText: label,
        labelStyle: const TextStyle(fontSize: 12.5, color: Color(0xFF76799C)),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: Color(0xFFD6E5F8))),
        enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: Color(0xFFD6E5F8))),
        focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: Color(0xFF3577F6), width: 1.5)),
        contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 14),
        filled: true, fillColor: const Color(0xFFFAFBFF), counterText: "", isDense: true,
      ),
    );
  }

  Widget _buildSmallInput(TextEditingController controller, String hint, {int? maxLength, TextInputType? inputType}) {
    return TextFormField(
      controller: controller,
      style: const TextStyle(fontSize: 13.5, color: Color(0xFF2B4B84), fontWeight: FontWeight.w600),
      maxLength: maxLength, keyboardType: inputType,
      decoration: InputDecoration(
        hintText: hint,
        hintStyle: const TextStyle(fontSize: 12, color: Color(0xFF9AA5B8)),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: Color(0xFFD6E5F8))),
        enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: Color(0xFFD6E5F8))),
        focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: Color(0xFF3577F6), width: 1.5)),
        contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 14), 
        filled: true, fillColor: Colors.white, counterText: "", isDense: true,
      ),
    );
  }

  Widget _buildAmenityChip(String label, TextEditingController controller, IconData icon) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 4),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border.all(color: const Color(0xFFD6E5F8), width: 1.2),
        borderRadius: BorderRadius.circular(12),
        boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.02), blurRadius: 4, offset: const Offset(0, 2))],
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 16, color: const Color(0xFF4C71F9)),
          const SizedBox(width: 4),
          Text(label, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Color(0xFF4A5568))),
          const SizedBox(width: 8),
          SizedBox(
            width: 36, height: 32,
            child: TextFormField(
              controller: controller, keyboardType: TextInputType.number, maxLength: 2, textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: Color(0xFF2B4B84)),
              decoration: InputDecoration(
                filled: true, fillColor: const Color(0xFFF4F7FF), counterText: "",
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(8), borderSide: BorderSide.none),
                contentPadding: const EdgeInsets.symmetric(horizontal: 0, vertical: 0),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _SectionTitle({required String title, required IconData icon}) {
    return Padding(
      padding: const EdgeInsets.only(left: 4.0, bottom: 4.0),
      child: Row(
        children: [
          Icon(icon, size: 20, color: const Color(0xFF4C71F9)),
          const SizedBox(width: 8),
          Text(
            title,
            style: const TextStyle(fontWeight: FontWeight.w800, color: Color(0xff2B3550), fontSize: 16, letterSpacing: 0.3),
          ),
        ],
      ),
    );
  }
}