import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../utils/data_manager.dart';
import '../services/auth_service.dart';
import '../main.dart';

class SignupScreen extends StatefulWidget {
  const SignupScreen({super.key});

  @override
  State<SignupScreen> createState() => _SignupScreenState();
}

class _SignupScreenState extends State<SignupScreen> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _phoneController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  
  final AuthService _authService = AuthService();
  
  bool _isPasswordVisible = false;
  bool _isLoading = false;

  void _handleSignup() async {
    debugPrint("🔘 [TAP] Signup button clicked!");

    try {
      FirebaseAuth.instance.app; 
    } catch (e) {
      debugPrint("💀 [FATAL] Firebase NOT initialized!");
      _showSnackBar("System Error: Firebase not ready.");
      return;
    }

    if (!_formKey.currentState!.validate()) {
      debugPrint("⚠️ [INVALID] Form validation failed.");
      return;
    }

    setState(() => _isLoading = true);

    try {
      debugPrint("📡 [NETWORK] Syncing ${_emailController.text} with Django...");
      await _authService.signUpWithEmail(
        _emailController.text.trim(),
        _passwordController.text.trim(),
        _nameController.text.trim(),
        _phoneController.text.trim(),
      );

      debugPrint("🎯 [SUCCESS] Signup Complete.");
      
      if (!mounted) return;
      _showSnackBar("အကောင့်ဖွင့်ခြင်း အောင်မြင်ပါသည်။");

      // Pop twice to return 'true' to MainScreen
      // ✅ FIX: Kill all previous screens and go to MainScreen
      Navigator.of(context).pushAndRemoveUntil(
        MaterialPageRoute(builder: (context) => MainScreen()),
        (route) => false, // This condition removes ALL previous routes
      );

    } catch (e) {
      debugPrint("❌ [ERROR] Signup Failed: $e");
      _showSnackBar("Signup Error: ${e.toString()}");
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  void _showSnackBar(String message) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));
  }

  @override
  void dispose() {
    _nameController.dispose();
    _phoneController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("🎨 [UI] SignupScreen is building. Loading state: $_isLoading");
    return Scaffold(
      backgroundColor: const Color(0xFFFAFBFF),
      appBar: AppBar(backgroundColor: Colors.transparent, elevation: 0, foregroundColor: const Color(0xFF2B3550)),
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 10),
            physics: const BouncingScrollPhysics(),
            child: Form(
              key: _formKey,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const Text("အကောင့်သစ် ဖွင့်မည်", style: TextStyle(fontSize: 26, fontWeight: FontWeight.w900, color: Color(0xFF2B3550))),
                  const SizedBox(height: 8),
                  const Text("အိမ်ခြံမြေများကို လွယ်ကူစွာ ရှာဖွေရန် အကောင့်ဖွင့်လိုက်ပါ", style: TextStyle(fontSize: 14, color: Color(0xFF76799C))),
                  const SizedBox(height: 30),

                  _buildTextField(
                    controller: _nameController, 
                    label: "အမည်အပြည့်အစုံ", 
                    icon: Icons.person_outline_rounded,
                    validator: (v) => (v == null || v.isEmpty) ? "အမည်ထည့်ပါ" : null,
                  ),
                  const SizedBox(height: 16),
                  
                  _buildTextField(
                    controller: _phoneController, 
                    label: "ဖုန်းနံပါတ်", 
                    icon: Icons.phone_android_rounded, 
                    keyboardType: TextInputType.phone
                  ),
                  const SizedBox(height: 16),

                  _buildTextField(
                    controller: _emailController, 
                    label: "အီးမေးလ်", 
                    icon: Icons.email_outlined, 
                    keyboardType: TextInputType.emailAddress,
                    validator: (v) => (v == null || !v.contains('@')) ? "မှန်ကန်သော အီးမေးလ် ထည့်ပါ" : null,
                  ),
                  const SizedBox(height: 16),

                  _buildTextField(
                    controller: _passwordController, 
                    label: "စကားဝှက်", 
                    icon: Icons.lock_outline_rounded, 
                    isPassword: true,
                    validator: (v) => (v == null || v.length < 6) ? "စကားဝှက် အနည်းဆုံး ၆ လုံးရှိရမည်" : null,
                  ),
                  const SizedBox(height: 30),

                  Container(
                    height: 54,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(14),
                      gradient: const LinearGradient(colors: [Color(0xFF4C71F9), Color(0xFF3558D6)]),
                    ),
                    child: ElevatedButton(
                      onPressed: _isLoading ? null : _handleSignup,
                      style: ElevatedButton.styleFrom(backgroundColor: Colors.transparent, shadowColor: Colors.transparent, shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
                      child: _isLoading 
                          ? const SizedBox(height: 24, width: 24, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2.5))
                          : const Text("အကောင့်ဖွင့်မည်", style: TextStyle(color: Colors.white, fontSize: 16.5, fontWeight: FontWeight.bold)),
                    ),
                  ),
                  const SizedBox(height: 24),

                  Row(
                    children: [
                      Expanded(child: Divider(color: Colors.grey.shade300)),
                      const Padding(padding: EdgeInsets.symmetric(horizontal: 16), child: Text("သို့မဟုတ်", style: TextStyle(color: Color(0xFF9AA5B8)))),
                      Expanded(child: Divider(color: Colors.grey.shade300)),
                    ],
                  ),
                  const SizedBox(height: 24),

                  _buildGoogleButton(onTap: () => debugPrint("Google Sign-In Tapped")),
                  
                  const SizedBox(height: 30),

                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text("အကောင့် ရှိပြီးသားလား? ", style: TextStyle(color: Color(0xFF76799C))),
                      GestureDetector(
                        onTap: () => Navigator.pop(context),
                        child: const Text("အကောင့်ဝင်မည်", style: TextStyle(color: Color(0xFF3577F6), fontWeight: FontWeight.w800)),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildTextField({
    required TextEditingController controller, 
    required String label, 
    required IconData icon, 
    bool isPassword = false, 
    TextInputType keyboardType = TextInputType.text,
    String? Function(String?)? validator,
  }) {
    return TextFormField(
      controller: controller,
      obscureText: isPassword && !_isPasswordVisible,
      keyboardType: keyboardType,
      validator: validator, // ✅ validator is now linked correctly
      style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600, color: Color(0xFF2B3550)),
      decoration: InputDecoration(
        labelText: label,
        prefixIcon: Icon(icon, color: const Color(0xFF9AA5B8), size: 22),
        suffixIcon: isPassword ? IconButton(icon: Icon(_isPasswordVisible ? Icons.visibility_rounded : Icons.visibility_off_rounded), onPressed: () => setState(() => _isPasswordVisible = !_isPasswordVisible)) : null,
        filled: true, fillColor: Colors.white,
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(14), borderSide: BorderSide(color: Colors.grey.shade300)),
      ),
    );
  }

  Widget _buildGoogleButton({required VoidCallback onTap}) {
    return InkWell(
      onTap: onTap,
      child: Container(
        height: 54,
        decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(14), border: Border.all(color: Colors.grey.shade300)),
        child: const Center(child: Text("Gmail Login", style: TextStyle(fontWeight: FontWeight.bold))),
      ),
    );
  }
}