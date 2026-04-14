import 'package:flutter/material.dart';
import '../services/auth_service.dart';
import 'login_screen.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  final AuthService _authService = AuthService();
  Map<String, dynamic>? userData;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadUserProfile();
  }

  Future<void> _loadUserProfile() async {
    try {
      // We assume your AuthService now has a method to get profile data
      // If it fails with 404, it will throw an exception caught below
      final profile = await _authService.getUserProfile(); 
      
      if (mounted) {
        setState(() {
          userData = profile;
          _isLoading = false;
        });
      }
    } catch (e) {
      debugPrint("❌ [PROFILE_LOAD_ERROR] $e");
      if (mounted) {
        setState(() => _isLoading = false);
        // If user not found or token invalid, boot them to Login
        _redirectToLogin();
      }
    }
  }

  void _redirectToLogin() {
  // We don't need to set a boolean anymore. 
  // Calling AuthService.signOut() handles the state globally.
  Navigator.of(context).pushAndRemoveUntil(
    MaterialPageRoute(builder: (context) => const LoginScreen()),
    (route) => false,
    );
  }

  void _handleLogout() async {
    await _authService.signOut();
    if (mounted) {
      _redirectToLogin();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFFAFBFF),
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.transparent,
        centerTitle: true,
        title: const Text(
          "ကျွန်ုပ်၏ ပရိုဖိုင်",
          style: TextStyle(
            fontSize: 19,
            fontWeight: FontWeight.w900,
            color: Color(0xFF2B3550),
            letterSpacing: 0.5,
          ),
        ),
        actions: [
          if (!_isLoading)
            IconButton(
              icon: const Icon(Icons.refresh, color: Color(0xFF3577F6)),
              onPressed: _loadUserProfile,
            )
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : (userData == null)
            ? const Center(child: Text("ဒေတာ ရှာမတွေ့ပါ"))
          : RefreshIndicator(
              onRefresh: _loadUserProfile,
              child: SingleChildScrollView(
                physics: const BouncingScrollPhysics(parent: AlwaysScrollableScrollPhysics()),
                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                child: Column(
                  children: [
                    // 1. Profile Header
                    _buildProfileHeader(
                      name: userData?['full_name'] ?? "အမည်မသိ",
                      phone: userData?['phone_number'] ?? "ဖုန်းနံပါတ်မရှိ",
                      photoUrl: userData?['profile_picture'],
                    ),
                    const SizedBox(height: 28),

                    // 2. Dashboard Cards
                    Row(
                      children: [
                        Expanded(
                          child: _buildStatCard(
                            context,
                            title: "ကိုယ်တင်ထားသော",
                            count: "${userData?['listings_count'] ?? 0} ခု",
                            icon: Icons.maps_home_work_rounded,
                            color: const Color(0xFF3577F6),
                            onTap: () {},
                          ),
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          child: _buildStatCard(
                            context,
                            title: "မှတ်သားထားသော",
                            count: "${userData?['favorites_count'] ?? 0} ခု",
                            icon: Icons.favorite_rounded,
                            color: const Color(0xFFEF5350),
                            onTap: () {},
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 32),

                    // 3. Settings Menu
                    _buildMenuSection(
                      title: "အကောင့်ဆက်တင်များ",
                      items: [
                        _buildMenuItem(Icons.person_outline_rounded, "ကိုယ်ရေးအချက်အလက် ပြင်ရန်"),
                        _buildMenuItem(Icons.lock_outline_rounded, "စကားဝှက် ပြောင်းရန်"),
                        _buildMenuItem(Icons.notifications_none_rounded, "အသိပေးချက်များ"),
                      ],
                    ),
                    const SizedBox(height: 24),

                    // 4. Other Menu
                    _buildMenuSection(
                      title: "အခြား",
                      items: [
                        _buildMenuItem(Icons.language_rounded, "ဘာသာစကား (Language)"),
                        _buildMenuItem(Icons.help_outline_rounded, "အကူအညီ နှင့် အမေးများသောမေးခွန်းများ"),
                        _buildMenuItem(Icons.policy_outlined, "စည်းမျဉ်းစည်းကမ်းများ"),
                      ],
                    ),
                    const SizedBox(height: 32),

                    // 5. Logout Button
                    SizedBox(
                      width: double.infinity,
                      height: 52,
                      child: OutlinedButton.icon(
                        onPressed: _handleLogout,
                        icon: const Icon(Icons.logout_rounded, color: Color(0xFFEF5350), size: 22),
                        label: const Text(
                          "အကောင့်မှ ထွက်မည်",
                          style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Color(0xFFEF5350)),
                        ),
                        style: OutlinedButton.styleFrom(
                          side: const BorderSide(color: Color(0xFFEF5350), width: 1.5),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                        ),
                      ),
                    ),
                    const SizedBox(height: 40),
                  ],
                ),
              ),
            ),
    );
  }

  Widget _buildProfileHeader({required String name, required String phone, String? photoUrl}) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: const Color(0xFF3577F6).withOpacity(0.06),
            blurRadius: 20,
            offset: const Offset(0, 8),
          ),
        ],
        border: Border.all(color: const Color(0xFFF0F5FF), width: 1.5),
      ),
      child: Row(
        children: [
          Container(
            height: 70, width: 70,
            decoration: BoxDecoration(
              color: const Color(0xFFE4ECFB),
              shape: BoxShape.circle,
              border: Border.all(color: Colors.white, width: 3),
              boxShadow: const [BoxShadow(color: Colors.black12, blurRadius: 8)],
              image: photoUrl != null 
                  ? DecorationImage(image: NetworkImage(photoUrl), fit: BoxFit.cover)
                  : null,
            ),
            child: photoUrl == null 
                ? const Icon(Icons.person_rounded, size: 40, color: Color(0xFF9AA5B8))
                : null,
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  name,
                  style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w900, color: Color(0xFF2B3550)),
                ),
                const SizedBox(height: 4),
                Text(
                  phone,
                  style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: Colors.grey.shade600),
                ),
              ],
            ),
          ),
          Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: const Color(0xFFF4F7FF),
              borderRadius: BorderRadius.circular(10),
            ),
            child: const Icon(Icons.edit_rounded, color: Color(0xFF3577F6), size: 20),
          ),
        ],
      ),
    );
  }

  Widget _buildStatCard(BuildContext context, {required String title, required String count, required IconData icon, required Color color, required VoidCallback onTap}) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 20, horizontal: 16),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(20),
          boxShadow: [BoxShadow(color: color.withOpacity(0.08), blurRadius: 16, offset: const Offset(0, 6))],
          border: Border.all(color: color.withOpacity(0.15), width: 1.5),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(color: color.withOpacity(0.1), shape: BoxShape.circle),
              child: Icon(icon, color: color, size: 24),
            ),
            const SizedBox(height: 16),
            Text(count, style: TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: color)),
            const SizedBox(height: 4),
            Text(title, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: Color(0xFF5A6B8A))),
          ],
        ),
      ),
    );
  }

  Widget _buildMenuSection({required String title, required List<Widget> items}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 8, bottom: 12),
          child: Text(title, style: const TextStyle(fontSize: 14.5, fontWeight: FontWeight.w900, color: Color(0xFF9AA5B8), letterSpacing: 0.5)),
        ),
        Container(
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(16),
            boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.03), blurRadius: 10, offset: const Offset(0, 4))],
            border: Border.all(color: const Color(0xFFF0F5FF), width: 1.5),
          ),
          child: Column(children: items),
        ),
      ],
    );
  }

  Widget _buildMenuItem(IconData icon, String title) {
    return ListTile(
      leading: Container(
        padding: const EdgeInsets.all(8),
        decoration: BoxDecoration(color: const Color(0xFFF4F7FF), borderRadius: BorderRadius.circular(8)),
        child: Icon(icon, size: 20, color: const Color(0xFF3577F6)),
      ),
      title: Text(title, style: const TextStyle(fontSize: 14.5, fontWeight: FontWeight.w600, color: Color(0xFF2B3550))),
      trailing: const Icon(Icons.arrow_forward_ios_rounded, size: 16, color: Color(0xFFC0C9DB)),
      onTap: () {},
    );
  }
}