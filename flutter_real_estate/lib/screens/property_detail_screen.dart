import 'dart:typed_data';
import 'package:flutter/material.dart';

class PropertyDetailScreen extends StatelessWidget {
  final Map<String, dynamic> propertyData;
  final List<Uint8List> images;

  const PropertyDetailScreen({
    super.key,
    required this.propertyData,
    required this.images,
  });

  @override
  Widget build(BuildContext context) {
    // 🔴 ၁။ ဓာတ်ပုံများကို စစ်ဆေးခြင်း
    // Map ထဲက localImages ကို အရင်ရှာမည်၊ မရှိမှ parameter က images ကိုယူမည်
    List<Uint8List> displayImages = [];
    if (propertyData.containsKey('localImages') && propertyData['localImages'] != null) {
      displayImages = List<Uint8List>.from(propertyData['localImages']);
    } else if (images.isNotEmpty) {
      displayImages = images;
    }

    String networkImage = propertyData['image']?.toString() ?? '';

    // 🔴 ၂။ အမျိုးအစား နှင့် ဈေးနှုန်း နောက်ဆက်တွဲ Logic ပြင်ဆင်ခြင်း
    String typeStr = propertyData['type']?.toString() ?? 'For Sale';
    String typeLabel = 'အရောင်း';
    String priceSuffix = 'သိန်း';

    if (typeStr == 'For Rent') {
      typeLabel = 'အငှား';
      priceSuffix = 'ကျပ်/တစ်လ';
    } else if (typeStr == 'Want to Buy') {
      typeLabel = 'ဝယ်လိုသည်';
    } else if (typeStr == 'Want to Rent') {
      typeLabel = 'ငှားလိုသည်';
      priceSuffix = 'ကျပ်/တစ်လ';
    }

    return Scaffold(
      backgroundColor: const Color(0xFFFAFBFF),
      bottomNavigationBar: Container(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
        decoration: BoxDecoration(
          color: Colors.white,
          boxShadow: [
            BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 20, offset: const Offset(0, -5))
          ],
          borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
        ),
        child: SafeArea(
          child: Row(
            children: [
              Expanded(
                child: ElevatedButton.icon(
                  onPressed: () {
                    // TODO: Implement Phone Call using url_launcher
                  },
                  icon: const Icon(Icons.call, color: Colors.white, size: 20),
                  label: const Text("ဖုန်းခေါ်မည်", style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold)),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF3577F6),
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    elevation: 0,
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: ElevatedButton.icon(
                  onPressed: () {
                    // TODO: Implement Viber Chat using url_launcher
                  },
                  icon: const Icon(Icons.wechat, color: Colors.white, size: 20),
                  label: const Text("Viber Chat", style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold)),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF8E24AA), // Viber Color
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    elevation: 0,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
      body: CustomScrollView(
        physics: const BouncingScrollPhysics(),
        slivers: [
          // 1. Image Header (ဓာတ်ပုံပြရန်)
          SliverAppBar(
            expandedHeight: 280,
            pinned: true,
            backgroundColor: Colors.white,
            foregroundColor: const Color(0xFF2B3550),
            elevation: 0,
            flexibleSpace: FlexibleSpaceBar(
              // 🔴 ၃။ ဓာတ်ပုံပြသသည့် Logic အသစ်
              background: displayImages.isNotEmpty
                  ? PageView.builder(
                      itemCount: displayImages.length,
                      itemBuilder: (context, index) {
                        return Image.memory(
                          displayImages[index],
                          fit: BoxFit.cover,
                          width: double.infinity,
                        );
                      },
                    )
                  : (networkImage.isNotEmpty)
                      ? Image.network(
                          networkImage,
                          fit: BoxFit.cover,
                          width: double.infinity,
                          errorBuilder: (context, error, stackTrace) => Container(
                            color: const Color(0xFFE4ECFB),
                            child: const Center(
                              child: Icon(Icons.broken_image_rounded, size: 60, color: Color(0xFF9AA5B8)),
                            ),
                          ),
                        )
                      : Container(
                          color: const Color(0xFFE4ECFB),
                          child: const Center(
                            child: Icon(Icons.home_work_rounded, size: 80, color: Color(0xFF9AA5B8)),
                          ),
                        ),
            ),
          ),

          // 2. Property Details (အချက်အလက်များ)
          // 2. Property Details (အချက်အလက်များ)
          SliverToBoxAdapter(
            child: Container(
              padding: const EdgeInsets.all(20),
              decoration: const BoxDecoration(
                color: Color(0xFFFAFBFF),
                borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // 🔴 ၁။ ခေါင်းစဉ် (Title) ကို အပေါ်ဆုံးသို့ ရွှေ့လိုက်ပါပြီ
                  Text(
                    propertyData['title'] ?? 'N/A',
                    style: const TextStyle(fontSize: 21, fontWeight: FontWeight.w900, color: Color(0xFF2B3550), height: 1.3),
                  ),
                  const SizedBox(height: 16),

                  // 🔴 ၂။ Type & Status Tag ကို ဒုတိယနေရာသို့ ရွှေ့လိုက်ပါပြီ
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                        decoration: BoxDecoration(
                          color: const Color(0xFF3577F6).withOpacity(0.1),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(
                          typeLabel, 
                          style: const TextStyle(color: Color(0xFF3577F6), fontWeight: FontWeight.bold, fontSize: 13),
                        ),
                      ),
                      Text(
                        "ID: #${propertyData['id']?.toString().substring(5, 10) ?? '10024'}",
                        style: TextStyle(color: Colors.grey.shade500, fontSize: 13, fontWeight: FontWeight.w600),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),

                  // 🔴 ၃။ Price
                  Text(
                    "${propertyData['price']} $priceSuffix", 
                    style: const TextStyle(fontSize: 26, fontWeight: FontWeight.w900, color: Color(0xFFEF5350)),
                  ),
                  const SizedBox(height: 12),

                  // 🔴 ၄။ Location
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Icon(Icons.location_on_rounded, size: 18, color: Color(0xFF9AA5B8)),
                      const SizedBox(width: 6),
                      Expanded(
                        child: Text(
                          propertyData['location'] ?? 'N/A',
                          style: const TextStyle(fontSize: 14.5, color: Color(0xFF5A6B8A), height: 1.4, fontWeight: FontWeight.w500),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 24),
                  const Divider(color: Color(0xFFEEF0F6), thickness: 1.2),
                  const SizedBox(height: 20),

                  
                  // Specifications
                  const Text("အချက်အလက်များ", style: TextStyle(fontSize: 17, fontWeight: FontWeight.bold, color: Color(0xFF2B3550))),
                  const SizedBox(height: 12),
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: const Color(0xFFE4ECFB), width: 1.2),
                    ),
                    child: Text(
                      propertyData['specs'] ?? 'N/A',
                      style: const TextStyle(fontSize: 14.5, color: Color(0xFF4A5568), height: 1.8),
                    ),
                  ),
                  const SizedBox(height: 20),

                  // Extra Features
                  const Text("အထူးပြုချက်များ", style: TextStyle(fontSize: 17, fontWeight: FontWeight.bold, color: Color(0xFF2B3550))),
                  const SizedBox(height: 12),
                  Wrap(
                    spacing: 10,
                    runSpacing: 10,
                    children: [
                      if (propertyData['isOwnerDirect'] == true) _buildFeatureChip(Icons.person_rounded, "ပိုင်ရှင်တိုက်ရိုက်"),
                      if (propertyData['isNegotiable'] == true) _buildFeatureChip(Icons.handshake_rounded, "စျေးညှိနှိုင်းနိုင်"),
                      if (propertyData['isDecorated'] == true) _buildFeatureChip(Icons.auto_awesome_rounded, "ပြင်ဆင်ပြီး"),
                      if (propertyData['isPreSale'] == true) _buildFeatureChip(Icons.payments_rounded, "အရစ်ကျရ"),
                      if (propertyData['isBankTransfer'] == true) _buildFeatureChip(Icons.account_balance_rounded, "ဘဏ်ငွေလွှဲလက်ခံသည်"),
                    ],
                  ),
                  
                  // Description
                  if (propertyData['description'] != null && propertyData['description'].toString().trim().isNotEmpty) ...[
                    const SizedBox(height: 24),
                    const Text("အခြားမှတ်ချက်များ", style: TextStyle(fontSize: 17, fontWeight: FontWeight.bold, color: Color(0xFF2B3550))),
                    const SizedBox(height: 12),
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: const Color(0xFFF9FBFF),
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(color: const Color(0xFFE4ECFB), width: 1.2),
                      ),
                      child: Text(
                        propertyData['description'],
                        style: const TextStyle(fontSize: 14.5, color: Color(0xFF5A6B8A), height: 1.6),
                      ),
                    ),
                  ],

                  const SizedBox(height: 30),
                  
                  // Phone Numbers
                  const Text("ဆက်သွယ်ရန် နံပါတ်", style: TextStyle(fontSize: 17, fontWeight: FontWeight.bold, color: Color(0xFF2B3550))),
                  const SizedBox(height: 12),
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: const Color(0xFFF4F7FF),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: const Color(0xFFD6E5F8), width: 1.2),
                    ),
                    child: Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.all(10),
                          decoration: const BoxDecoration(color: Colors.white, shape: BoxShape.circle),
                          child: const Icon(Icons.phone_in_talk, color: Color(0xFF3577F6), size: 20),
                        ),
                        const SizedBox(width: 16),
                        Expanded(
                          child: Text(
                            propertyData['phone'] ?? 'N/A',
                            style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: Color(0xFF2B3550)),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 40), 
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildFeatureChip(IconData icon, String label) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: const Color(0xFF10B981).withOpacity(0.1),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: const Color(0xFF10B981).withOpacity(0.3)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 16, color: const Color(0xFF059669)),
          const SizedBox(width: 6),
          Text(label, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.bold, color: Color(0xFF059669))),
        ],
      ),
    );
  }
}