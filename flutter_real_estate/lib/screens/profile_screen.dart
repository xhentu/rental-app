import 'package:flutter/material.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

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
      ),
      body: SingleChildScrollView(
        physics: const BouncingScrollPhysics(),
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
        child: Column(
          children: [
            // 1. Profile Header (ကိုယ်ရေးအချက်အလက်)
            _buildProfileHeader(),
            const SizedBox(height: 28),

            // 2. Dashboard Cards (ကိုယ်တင်ထားသော နှင့် မှတ်သားထားသော စာရင်းများ)
            Row(
              children: [
                Expanded(
                  child: _buildStatCard(
                    context,
                    title: "ကိုယ်တင်ထားသော",
                    count: "၅ ခု", // Data အစစ်ချိတ်လျှင် ဤနေရာတွင် ပြင်ပါ
                    icon: Icons.maps_home_work_rounded,
                    color: const Color(0xFF3577F6),
                    onTap: () {
                      // TODO: Navigate to My Listings Screen
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('ကိုယ်တင်ထားသော စာရင်းများသို့ သွားမည်')),
                      );
                    },
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: _buildStatCard(
                    context,
                    title: "မှတ်သားထားသော",
                    count: "၁၂ ခု", // Data အစစ်ချိတ်လျှင် ဤနေရာတွင် ပြင်ပါ
                    icon: Icons.favorite_rounded,
                    color: const Color(0xFFEF5350),
                    onTap: () {
                      // TODO: Navigate to Saved Properties Screen
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('မှတ်သားထားသော စာရင်းများသို့ သွားမည်')),
                      );
                    },
                  ),
                ),
              ],
            ),
            const SizedBox(height: 32),

            // 3. Settings Menu (အကောင့် ဆက်တင်များ)
            _buildMenuSection(
              title: "အကောင့်ဆက်တင်များ",
              items: [
                _buildMenuItem(Icons.person_outline_rounded, "ကိုယ်ရေးအချက်အလက် ပြင်ရန်"),
                _buildMenuItem(Icons.lock_outline_rounded, "စကားဝှက် ပြောင်းရန်"),
                _buildMenuItem(Icons.notifications_none_rounded, "အသိပေးချက်များ"),
              ],
            ),
            const SizedBox(height: 24),

            // 4. Other Menu (အခြား)
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
                onPressed: () {
                  // TODO: Implement Logout Logic
                },
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
    );
  }

  // --- Custom Helper Widgets ---

  // Profile ပုံ နှင့် နာမည်ပြမည့် အပိုင်း
  Widget _buildProfileHeader() {
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
            height: 70,
            width: 70,
            decoration: BoxDecoration(
              color: const Color(0xFFE4ECFB),
              shape: BoxShape.circle,
              border: Border.all(color: Colors.white, width: 3),
              boxShadow: const [BoxShadow(color: Colors.black12, blurRadius: 8)],
            ),
            child: const Icon(Icons.person_rounded, size: 40, color: Color(0xFF9AA5B8)),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  "Aung Aung", // User Name
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.w900, color: Color(0xFF2B3550)),
                ),
                const SizedBox(height: 4),
                Text(
                  "09-123456789", // User Phone
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

  // ကိုယ်တင်ထားသော / မှတ်သားထားသော ကတ်များ
  Widget _buildStatCard(BuildContext context, {required String title, required String count, required IconData icon, required Color color, required VoidCallback onTap}) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 20, horizontal: 16),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(20),
          boxShadow: [
            BoxShadow(
              color: color.withOpacity(0.08),
              blurRadius: 16,
              offset: const Offset(0, 6),
            ),
          ],
          border: Border.all(color: color.withOpacity(0.15), width: 1.5),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: color.withOpacity(0.1),
                shape: BoxShape.circle,
              ),
              child: Icon(icon, color: color, size: 24),
            ),
            const SizedBox(height: 16),
            Text(
              count,
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: color),
            ),
            const SizedBox(height: 4),
            Text(
              title,
              style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: Color(0xFF5A6B8A)),
            ),
          ],
        ),
      ),
    );
  }

  // Menu Group ခေါင်းစဉ်
  Widget _buildMenuSection({required String title, required List<Widget> items}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 8, bottom: 12),
          child: Text(
            title,
            style: const TextStyle(fontSize: 14.5, fontWeight: FontWeight.w900, color: Color(0xFF9AA5B8), letterSpacing: 0.5),
          ),
        ),
        Container(
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(16),
            boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.03), blurRadius: 10, offset: const Offset(0, 4))],
            border: Border.all(color: const Color(0xFFF0F5FF), width: 1.5),
          ),
          child: Column(
            children: items,
          ),
        ),
      ],
    );
  }

  // Menu Item တစ်ခုချင်းစီ
  Widget _buildMenuItem(IconData icon, String title) {
    return ListTile(
      leading: Container(
        padding: const EdgeInsets.all(8),
        decoration: BoxDecoration(color: const Color(0xFFF4F7FF), borderRadius: BorderRadius.circular(8)),
        child: Icon(icon, size: 20, color: const Color(0xFF3577F6)),
      ),
      title: Text(
        title,
        style: const TextStyle(fontSize: 14.5, fontWeight: FontWeight.w600, color: Color(0xFF2B3550)),
      ),
      trailing: const Icon(Icons.arrow_forward_ios_rounded, size: 16, color: Color(0xFFC0C9DB)),
      onTap: () {
        // Handle Menu Tap
      },
    );
  }
}