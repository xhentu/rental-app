import 'package:flutter/material.dart';

// ဘာသာစကား အပြောင်းအလဲကို နားထောင်မည့် Notifier
final ValueNotifier<String> currentLanguage = ValueNotifier('mm'); // Default: Myanmar

// ဘာသာစကား ပြောင်းသည့် Function
void toggleLanguage() {
  currentLanguage.value = currentLanguage.value == 'mm' ? 'en' : 'mm';
}

// စာသားများကို ဘာသာပြန်ပေးမည့် Function
String t(String key) {
  return _localizedValues[currentLanguage.value]?[key] ?? key;
}

// Dictionary (စာသားများ)
const Map<String, Map<String, String>> _localizedValues = {
  'mm': {
    // App Bar & General
    'app_title': 'ရွှေအိမ်',
    'login': 'ဝင်ရောက်မည်',
    'search_hint': 'မြို့နယ်၊ ဈေးနှုန်း၊ အထပ် ရွေးရန်...',
    
    // Bottom Navigation
    'nav_home': 'ရောင်း၊ငှား',
    'nav_buy': 'ရောင်းရန်',
    'nav_rent': 'ငှားရန်',
    'nav_profile': 'အကောင့်',

    // Upload & Actions
    'upload_title': 'အိမ်ခြံမြေ စာရင်းသွင်းရန်',
    'btn_search': 'ရှာဖွေပါ',
  },
  'en': {
    // App Bar & General
    'app_title': 'Shwe Eain',
    'login': 'Login',
    'search_hint': 'Search by Township, Price, Floor...',
    
    // Bottom Navigation
    'nav_home': 'home',
    'nav_buy': 'for sale',
    'nav_rent': 'for rent',
    'nav_profile': 'Profile',

    // Upload & Actions
    'upload_title': 'Upload Property',
    'btn_search': 'Search',
  },
};