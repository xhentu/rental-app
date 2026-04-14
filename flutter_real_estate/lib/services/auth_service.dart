import 'dart:convert';
import 'dart:io'; // To detect socket/network errors
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

class AuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance;

  // 💡 PRO TIP: 'localhost' only works if you ran 'adb reverse tcp:8000 tcp:8000'
  // If you are on the same Wi-Fi, use your laptop's Local IP (e.g., 192.168.1.x)
  final String _baseUrl = "http://localhost:8000/api"; // 10.0.2.2 is the alias for host machine in Android
  // final String _baseUrl = "http://10.0.2.2:8000/api";
  
  // 1. SIGN UP LOGIC
  // 1. SIGN UP LOGIC (Modified to accept and relay phone)
  Future<void> signUpWithEmail(String email, String password, String name, String phone) async {
    debugPrint("📡 [AUTH_SERVICE] Starting signUpWithEmail for: $email");
    
    try {
      // Step A: Create User in Firebase
      debugPrint("📡 [STEP A] Requesting Firebase User Creation...");
      UserCredential result = await _auth.createUserWithEmailAndPassword(
        email: email, 
        password: password
      );
      
      User? user = result.user;
      if (user != null) {
        debugPrint("✅ [STEP A] Firebase User Created: ${user.uid}");

        // Step B: Get the ID Token
        debugPrint("📡 [STEP B] Fetching ID Token...");
        String? idToken = await user.getIdToken();
        
        if (idToken != null) {
          // Step C: Send name AND phone to Django
          debugPrint("📡 [STEP C] Syncing with Django (Registering User Data)...");
          await _syncWithDjango(idToken, "register", {
            "name": name,
            "phone_number": phone, // 👈 The "lie" becomes data here!
          });
          debugPrint("✅ [STEP C] Django Sync Complete!");
        }
      }
    } on FirebaseAuthException catch (e) {
      debugPrint("❌ [FIREBASE_ERROR] ${e.message}");
      rethrow; 
    } catch (e) {
      debugPrint("❌ [UNKNOWN_ERROR] $e");
      rethrow; 
    }
  }

  // 2. LOGIN LOGIC
  Future<void> loginWithEmail(String email, String password) async {
    debugPrint("📡 [AUTH_SERVICE] Attempting login for: $email");
    try {
      UserCredential result = await _auth.signInWithEmailAndPassword(
        email: email, 
        password: password
      );
      
      debugPrint("✅ [LOGIN] Firebase Auth Success");
      
      String? idToken = await result.user?.getIdToken();
      if (idToken != null) {
        debugPrint("📡 [SYNC] Syncing Login with Django...");
        await _syncWithDjango(idToken, "login");
        debugPrint("✅ [SYNC] Django Login Sync Success");
      }
    } catch (e) {
      debugPrint("❌ [LOGIN_ERROR] $e");
      rethrow;
    }
  }

  // 3. THE PRIVATE BRIDGE (Talks to your Void Linux machine)
  // 3. THE PRIVATE BRIDGE (Optimized to use Header only for Auth)
  Future<void> _syncWithDjango(String token, String endpoint, [Map<String, String>? extraData]) async {
    final url = "$_baseUrl/users/$endpoint/";
    
    debugPrint("------------------------------------------");
    debugPrint("📡 [SYNC_START] Endpoint: /api/users/$endpoint/");

    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token', // Standard way to authenticate
        },
        body: jsonEncode({
          // ✅ We ONLY send actual data (name/phone) in the body now
          if (extraData != null) ...extraData,
        }),
      ).timeout(const Duration(seconds: 10));

      debugPrint("📥 [DJANGO_RESPONSE] Status: ${response.statusCode}");
      debugPrint("📄 [BODY] ${response.body}");

      if (response.statusCode != 200 && response.statusCode != 201) {
        throw Exception("Django rejected sync (${response.statusCode}): ${response.body}");
      }
    } on SocketException {
      debugPrint("🌐 [NETWORK_ERROR] Could not reach Django. Check 'adb reverse' or Server.");
      throw Exception("Connection to backend failed.");
    } catch (e) {
      debugPrint("❌ [SYNC_EXCEPTION] $e");
      rethrow;
    }
    debugPrint("------------------------------------------");
  }

  // 4. GET PROFILE LOGIC (The "Who Am I" check)
  Future<Map<String, dynamic>> getUserProfile() async {
    final user = _auth.currentUser;
    if (user == null) throw Exception("No firebase user found");

    final idToken = await user.getIdToken();
    print("📡 Sending Token: $idToken"); // 👀 Check your Flutter console!
    final url = "$_baseUrl/users/profile/";

    try {
      final response = await http.get(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $idToken',
        },
      ).timeout(const Duration(seconds: 10));

      debugPrint("📥 [PROFILE_FETCH] Status: ${response.statusCode}");

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else if (response.statusCode == 404) {
        // This is the trigger for the frontend to redirect to login/register
        throw Exception("USER_NOT_FOUND");
      } else {
        throw Exception("Server error: ${response.statusCode}");
      }
    } catch (e) {
      debugPrint("❌ [GET_PROFILE_ERROR] $e");
      rethrow;
    }
  }

  Future<void> signOut() async {
    debugPrint("🚪 [AUTH] Signing out...");
    await _auth.signOut();
  }
}