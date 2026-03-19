import 'dart:convert';
import 'dart:io'; // To detect socket/network errors
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

class AuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance;

  // 💡 PRO TIP: 'localhost' only works if you ran 'adb reverse tcp:8000 tcp:8000'
  // If you are on the same Wi-Fi, use your laptop's Local IP (e.g., 192.168.1.x)
  // final String _baseUrl = "http://localhost:8000/api"; // 10.0.2.2 is the alias for host machine in Android
  final String _baseUrl = "http://10.0.2.2:8000/api";
  // 1. SIGN UP LOGIC
  Future<void> signUpWithEmail(String email, String password, String name) async {
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

        // Step B: Get the ID Token (The "Passport" for Django)
        debugPrint("📡 [STEP B] Fetching ID Token from Firebase...");
        String? idToken = await user.getIdToken();
        
        if (idToken != null) {
          debugPrint("✅ [STEP B] Token received (length: ${idToken.length})");

          // Step C: Send the token to your Django Backend
          debugPrint("📡 [STEP C] Syncing with Django at $_baseUrl...");
          await _syncWithDjango(idToken, "register", {"name": name});
          debugPrint("✅ [STEP C] Django Sync Complete!");
        }
      }
    } on FirebaseAuthException catch (e) {
      debugPrint("❌ [FIREBASE_ERROR] Code: ${e.code} | Message: ${e.message}");
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
  Future<void> _syncWithDjango(String token, String endpoint, [Map<String, String>? extraData]) async {
    final url = "$_baseUrl/users/$endpoint/";
    
    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
        body: jsonEncode({
          'idToken': token,
          if (extraData != null) ...extraData,
        }),
      ).timeout(const Duration(seconds: 10)); // Don't hang forever

      debugPrint("📥 [DJANGO_RESPONSE] Status: ${response.statusCode}");

      if (response.statusCode != 200 && response.statusCode != 201) {
        debugPrint("🚫 [DJANGO_REJECTED] Body: ${response.body}");
        throw Exception("Django sync failed (${response.statusCode}): ${response.body}");
      }
    } on SocketException catch (e) {
      debugPrint("🌐 [NETWORK_ERROR] Could not reach Django at $url. Is your server running? Did you run 'adb reverse'?");
      throw Exception("Connection to backend failed. Check your network.");
    } catch (e) {
      debugPrint("❌ [SYNC_EXCEPTION] $e");
      rethrow;
    }
  }

  Future<void> signOut() async {
    debugPrint("🚪 [AUTH] Signing out...");
    await _auth.signOut();
  }
}