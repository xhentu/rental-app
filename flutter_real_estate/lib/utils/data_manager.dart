import 'package:flutter/foundation.dart';

// App စဖွင့်လျှင် မြင်ရမည့် နမူနာ ဒေတာများ (Dummy Data)
final List<Map<String, dynamic>> _initialData = [
  {
    "title": "လှိုင်, ရန်ကုန်တိုင်း (ကွန်ဒို)",
    "price": "1500",
    "location": "သီရိလမ်း, အနီးအနား: MICT Park",
    "image": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
    "type": "For Sale",
    "specs": "1200 sqft | မျက်နှာလှည့်: တောင် | MB:1 SB:2 AC:3",
    "phone": "09-123456789 (Viber)",
    "isBankTransfer": true,
  },
  {
    "title": "စမ်းချောင်း, ရန်ကုန်တိုင်း (တိုက်ခန်း)",
    "price": "4",
    "location": "ဗဟိုလမ်း, အနီးအနား: ဂမုန်းပွင့်",
    "image": "https://images.unsplash.com/photo-1502672260266-1c1e082fd345?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=60",
    "type": "For Rent",
    "specs": "900 sqft | အလွှာ (၃) | AC:1",
    "phone": "09-987654321",
    "isBankTransfer": false,
  }
];

// Data များကို ထိန်းချုပ်မည့် Notifier
ValueNotifier<List<Map<String, dynamic>>> propertyListNotifier = ValueNotifier(_initialData);

// စာရင်းအသစ်ထည့်ရန် Function
void addProperty(Map<String, dynamic> property) {
  // အသစ်တင်တဲ့ အိမ်ကို အပေါ်ဆုံးမှာ ပေါ်အောင် ရှေ့ဆုံးကနေ ထည့်ပါမည်
  propertyListNotifier.value = [property, ...propertyListNotifier.value];

}
// User Login ဝင်ထားခြင်း ရှိ/မရှိ မှတ်သားထားမည့် နေရာ
bool isUserLoggedIn = false;