import 'package:flutter/material.dart';
import 'signup_screen.dart';
import '../utils/data_manager.dart'; // isUserLoggedIn သုံးရန်

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController _emailController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  bool _isPasswordVisible = false;
  bool _isLoading = false;

  void _handleLogin() async {
    setState(() => _isLoading = true);
    await Future.delayed(const Duration(seconds: 1)); // Network delay ပုံစံတု
    setState(() => _isLoading = false);

    if (!mounted) return;
    
    // Login ဝင်ကြောင်း State ကို မှတ်သားလိုက်သည်
    isUserLoggedIn = true; 
    
    // MainScreen ဆီသို့ အောင်မြင်ကြောင်း (true) ပြန်ပို့ပေးမည်
    Navigator.pop(context, true); 
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFFAFBFF),
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        foregroundColor: const Color(0xFF2B3550), // နောက်သို့ ပြန်ထွက်ရန် Back ခလုတ် ပေါ်မည်
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24.0),
          physics: const BouncingScrollPhysics(),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Logo
              Container(
                height: 90, width: 90,
                decoration: BoxDecoration(color: const Color(0xFF3577F6).withOpacity(0.1), shape: BoxShape.circle),
                child: const Icon(Icons.real_estate_agent_rounded, size: 50, color: Color(0xFF3577F6)),
              ),
              const SizedBox(height: 24),
              const Text("ပြန်လည်ကြိုဆိုပါသည်!", textAlign: TextAlign.center, style: TextStyle(fontSize: 24, fontWeight: FontWeight.w900, color: Color(0xFF2B3550))),
              const SizedBox(height: 8),
              const Text("ဤလုပ်ဆောင်ချက်အတွက် အကောင့်ဝင်ရန် လိုအပ်ပါသည်", textAlign: TextAlign.center, style: TextStyle(fontSize: 14, color: Color(0xFF76799C))),
              const SizedBox(height: 40),

              _buildTextField(controller: _emailController, label: "အီးမေးလ်", icon: Icons.email_outlined, keyboardType: TextInputType.emailAddress),
              const SizedBox(height: 16),
              _buildTextField(controller: _passwordController, label: "စကားဝှက်", icon: Icons.lock_outline_rounded, isPassword: true),
              
              Align(
                alignment: Alignment.centerRight,
                child: TextButton(onPressed: () {}, child: const Text("စကားဝှက် မေ့နေပါသလား?", style: TextStyle(color: Color(0xFF3577F6), fontWeight: FontWeight.w600))),
              ),
              const SizedBox(height: 16),

              // Login Button
              Container(
                height: 54,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(14),
                  gradient: const LinearGradient(colors: [Color(0xFF4C71F9), Color(0xFF3558D6)]),
                  boxShadow: [BoxShadow(color: const Color(0xFF4C71F9).withOpacity(0.3), blurRadius: 12, offset: const Offset(0, 6))],
                ),
                child: ElevatedButton(
                  onPressed: _isLoading ? null : _handleLogin,
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.transparent, shadowColor: Colors.transparent, shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14))),
                  child: _isLoading 
                      ? const SizedBox(height: 24, width: 24, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2.5))
                      : const Text("အကောင့်ဝင်မည်", style: TextStyle(color: Colors.white, fontSize: 16.5, fontWeight: FontWeight.bold)),
                ),
              ),
              const SizedBox(height: 24),

              Row(
                children: [
                  Expanded(child: Divider(color: Colors.grey.shade300, thickness: 1)),
                  const Padding(padding: EdgeInsets.symmetric(horizontal: 16), child: Text("သို့မဟုတ်", style: TextStyle(color: Color(0xFF9AA5B8), fontWeight: FontWeight.w600))),
                  Expanded(child: Divider(color: Colors.grey.shade300, thickness: 1)),
                ],
              ),
              const SizedBox(height: 24),

              _buildGoogleButton(onTap: _handleLogin),
              
              const SizedBox(height: 30),

              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text("အကောင့် မရှိသေးဘူးလား? ", style: TextStyle(color: Color(0xFF76799C), fontSize: 14.5)),
                  GestureDetector(
                    onTap: () {
                      Navigator.push(context, MaterialPageRoute(builder: (context) => const SignupScreen()));
                    },
                    child: const Text("အကောင့်သစ်ဖွင့်မည်", style: TextStyle(color: Color(0xFF3577F6), fontSize: 14.5, fontWeight: FontWeight.w800)),
                  ),
                ],
              ),
              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }

  // Helper widgets ...
  Widget _buildTextField({required TextEditingController controller, required String label, required IconData icon, bool isPassword = false, TextInputType keyboardType = TextInputType.text}) {
    return TextFormField(
      controller: controller, obscureText: isPassword && !_isPasswordVisible, keyboardType: keyboardType,
      style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600, color: Color(0xFF2B3550)),
      decoration: InputDecoration(
        labelText: label, labelStyle: const TextStyle(color: Color(0xFF76799C)), prefixIcon: Icon(icon, color: const Color(0xFF9AA5B8), size: 22),
        suffixIcon: isPassword ? IconButton(icon: Icon(_isPasswordVisible ? Icons.visibility_rounded : Icons.visibility_off_rounded, color: const Color(0xFF9AA5B8), size: 20), onPressed: () => setState(() => _isPasswordVisible = !_isPasswordVisible)) : null,
        filled: true, fillColor: Colors.white, contentPadding: const EdgeInsets.symmetric(vertical: 16),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(14), borderSide: BorderSide(color: Colors.grey.shade300)),
        enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(14), borderSide: BorderSide(color: Colors.grey.shade300)),
        focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(14), borderSide: const BorderSide(color: Color(0xFF3577F6), width: 1.5)),
      ),
    );
  }

  Widget _buildGoogleButton({required VoidCallback onTap}) {
    return Container(
      height: 54,
      decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(14), border: Border.all(color: Colors.grey.shade300), boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.03), blurRadius: 10, offset: const Offset(0, 4))]),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(14), onTap: onTap,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Image.network("https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg", height: 24),
              const SizedBox(width: 12),
              const Text("Google Account ဖြင့် ဝင်မည်", style: TextStyle(fontSize: 15.5, fontWeight: FontWeight.bold, color: Color(0xFF2B3550))),
            ],
          ),
        ),
      ),
    );
  }
}