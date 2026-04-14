// import 'package:flutter/material.dart';
// import 'package:flutter/services.dart';
// import 'package:flutter/foundation.dart';
// import 'package:firebase_core/firebase_core.dart'; // ✅ Added this

// import 'screens/listing_tab.dart'; 
// import 'screens/upload_screen.dart'; 
// import 'screens/profile_screen.dart';
// import 'screens/login_screen.dart';
// import 'utils/data_manager.dart'; // isUserLoggedIn ကို သုံးရန်

// // Change to Future<void> and add async
// Future<void> main() async {
//   // ✅ FIX 1: Essential for Firebase & Platform channels
//   WidgetsFlutterBinding.ensureInitialized();
  
//   debugPrint("🚀 [BOOT] Step 1: WidgetsBinding Initialized");

//   try {
//     // ✅ FIX 2: Start Firebase before the UI loads
//     debugPrint("📡 [BOOT] Step 2: Attempting Firebase Initialization...");
//     await Firebase.initializeApp();
//     debugPrint("✅ [BOOT] Step 3: Firebase Ready!");
//   } catch (e) {
//     debugPrint("💀 [BOOT] FATAL ERROR: Firebase failed to start: $e");
//   }

//   SystemChrome.setSystemUIOverlayStyle(
//     const SystemUiOverlayStyle(
//       statusBarColor: Colors.transparent,
//       statusBarIconBrightness: Brightness.dark,
//     ),
//   );

//   runApp(const RealEstateApp());
// }

// class RealEstateApp extends StatelessWidget {
//   const RealEstateApp({super.key});

//   @override
//   Widget build(BuildContext context) {
//     return MaterialApp(
//       title: 'Myanmar Real Estate',
//       debugShowCheckedModeBanner: false,
//       theme: ThemeData(
//         primaryColor: const Color(0xFF3577F6),
//         scaffoldBackgroundColor: const Color(0xFFFAFBFF),
//         colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF3577F6)),
//         useMaterial3: true, 
//       ),
//       home: const MainScreen(), // <--- ပင်မစာမျက်နှာကို ပြန်ထားလိုက်ပါပြီ
//     );
//   }
// }

// class MainScreen extends StatefulWidget {
//   const MainScreen({super.key});

//   @override
//   State<MainScreen> createState() => _MainScreenState();
// }

// class _MainScreenState extends State<MainScreen> {
//   int _currentIndex = 0; 

//   final List<Widget> _pages = [
//     const ListingTab(category: 'all'),     
//     const UploadScreen(),   
//     const ProfileScreen(), 
//   ];

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       body: IndexedStack(
//         index: _currentIndex,
//         children: _pages,
//       ),
//       bottomNavigationBar: Container(
//         decoration: BoxDecoration(
//           boxShadow: [
//             BoxShadow(color: const Color(0xFF3577F6).withOpacity(0.08), blurRadius: 20, offset: const Offset(0, -4))
//           ],
//         ),
//         child: ClipRRect(
//           borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
//           child: BottomNavigationBar(
//             currentIndex: _currentIndex,
//             onTap: (index) async {
//               // 'စာရင်းသွင်းမည်' (1) သို့မဟုတ် 'ပရိုဖိုင်' (2) ကို နှိပ်ပြီး Login မဝင်ရသေးလျှင်
//               if ((index == 1 || index == 2) && !isUserLoggedIn) {
//                 // Login Screen သို့ သွားခိုင်းမည်
//                 final bool? loginSuccess = await Navigator.push(
//                   context,
//                   MaterialPageRoute(builder: (context) => const LoginScreen()),
//                 );
//                 // Login အောင်မြင်ပါက နှိပ်လိုက်သော Tab သို့ ကူးပြောင်းပေးမည်
//                 if (loginSuccess == true) {
//                   setState(() => _currentIndex = index);
//                 }
//               } else {
//                 // Home (0) ကိုနှိပ်လျှင် သို့မဟုတ် Login ဝင်ပြီးသားဖြစ်လျှင် ပုံမှန်အတိုင်း သွားမည်
//                 setState(() => _currentIndex = index);
//               }
//             },
//             backgroundColor: Colors.white,
//             selectedItemColor: const Color(0xFF3577F6),
//             unselectedItemColor: const Color(0xFF9AA5B8),
//             selectedFontSize: 12.5,
//             unselectedFontSize: 12,
//             type: BottomNavigationBarType.fixed,
//             elevation: 0,
//             items: const [
//               BottomNavigationBarItem(
//                 icon: Padding(padding: EdgeInsets.only(bottom: 6.0), child: Icon(Icons.home_outlined, size: 26)),
//                 activeIcon: Padding(padding: EdgeInsets.only(bottom: 6.0), child: Icon(Icons.home_rounded, size: 26)),
//                 label: 'ပင်မ',
//               ),
//               BottomNavigationBarItem(
//                 icon: Padding(padding: EdgeInsets.only(bottom: 6.0), child: Icon(Icons.add_box_outlined, size: 26)),
//                 activeIcon: Padding(padding: EdgeInsets.only(bottom: 6.0), child: Icon(Icons.add_box_rounded, size: 26)),
//                 label: 'စာရင်းသွင်းမည်',
//               ),
//               BottomNavigationBarItem(
//                 icon: Padding(padding: EdgeInsets.only(bottom: 6.0), child: Icon(Icons.person_outline_rounded, size: 26)),
//                 activeIcon: Padding(padding: EdgeInsets.only(bottom: 6.0), child: Icon(Icons.person_rounded, size: 26)),
//                 label: 'ပရိုဖိုင်',
//               ),
//             ],
//           ),
//         ),
//       ),
//     );
//   }
// }

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter/foundation.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_auth/firebase_auth.dart'; // ✅ Added for the session check

import 'screens/listing_tab.dart'; 
import 'screens/upload_screen.dart'; 
import 'screens/profile_screen.dart';
import 'screens/login_screen.dart';
// 🗑️ Removed: utils/data_manager.dart import

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  debugPrint("🚀 [BOOT] Step 1: WidgetsBinding Initialized");

  try {
    debugPrint("📡 [BOOT] Step 2: Attempting Firebase Initialization...");
    await Firebase.initializeApp();
    debugPrint("✅ [BOOT] Step 3: Firebase Ready!");
  } catch (e) {
    debugPrint("💀 [BOOT] FATAL ERROR: Firebase failed to start: $e");
  }

  SystemChrome.setSystemUIOverlayStyle(
    const SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.dark,
    ),
  );

  runApp(const RealEstateApp());
}

class RealEstateApp extends StatelessWidget {
  const RealEstateApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Myanmar Real Estate',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primaryColor: const Color(0xFF3577F6),
        scaffoldBackgroundColor: const Color(0xFFFAFBFF),
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF3577F6)),
        useMaterial3: true, 
      ),
      home: const MainScreen(),
    );
  }
}

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int _currentIndex = 0; 

  final List<Widget> _pages = [
    const ListingTab(category: 'all'),     
    const UploadScreen(),   
    const ProfileScreen(), 
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _currentIndex,
        children: _pages,
      ),
      bottomNavigationBar: Container(
        decoration: BoxDecoration(
          boxShadow: [
            BoxShadow(
              color: const Color(0xFF3577F6).withOpacity(0.08), 
              blurRadius: 20, 
              offset: const Offset(0, -4)
            )
          ],
        ),
        child: ClipRRect(
          borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
          child: BottomNavigationBar(
            currentIndex: _currentIndex,
            onTap: (index) async {
              // ✅ FIX: Replace 'isUserLoggedIn' with Firebase session check
              final bool isAuth = FirebaseAuth.instance.currentUser != null;

              if ((index == 1 || index == 2) && !isAuth) {
                final bool? loginSuccess = await Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const LoginScreen()),
                );
                if (loginSuccess == true) {
                  setState(() => _currentIndex = index);
                }
              } else {
                setState(() => _currentIndex = index);
              }
            },
            backgroundColor: Colors.white,
            selectedItemColor: const Color(0xFF3577F6),
            unselectedItemColor: const Color(0xFF9AA5B8),
            selectedFontSize: 12.5,
            unselectedFontSize: 12,
            type: BottomNavigationBarType.fixed,
            elevation: 0,
            items: const [
              BottomNavigationBarItem(
                icon: Padding(padding: EdgeInsets.only(bottom: 6.0), child: Icon(Icons.home_outlined, size: 26)),
                activeIcon: Padding(padding: EdgeInsets.only(bottom: 6.0), child: Icon(Icons.home_rounded, size: 26)),
                label: 'ပင်မ',
              ),
              BottomNavigationBarItem(
                icon: Padding(padding: EdgeInsets.only(bottom: 6.0), child: Icon(Icons.add_box_outlined, size: 26)),
                activeIcon: Padding(padding: EdgeInsets.only(bottom: 6.0), child: Icon(Icons.add_box_rounded, size: 26)),
                label: 'စာရင်းသွင်းမည်',
              ),
              BottomNavigationBarItem(
                icon: Padding(padding: EdgeInsets.only(bottom: 6.0), child: Icon(Icons.person_outline_rounded, size: 26)),
                activeIcon: Padding(padding: EdgeInsets.only(bottom: 6.0), child: Icon(Icons.person_rounded, size: 26)),
                label: 'ပရိုဖိုင်',
              ),
            ],
          ),
        ),
      ),
    );
  }
}