// lib/screens/property_detail_screen.dart
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
    // 🖼️ ၁။ ဓာတ်ပုံများ စစ်ဆေးခြင်း Logic (Local ဓာတ်ပုံရှိလျှင်ယူမည်၊ မရှိပါက Network/API Images များကို ပတ်မည်)
    List<dynamic> networkImages = propertyData['images'] ?? [];
    
    // 🏷️ ၂။ ဒေတာ ကာကွယ်မှုနှင့် Extraction (Nested Maps များမှ အချက်အလက်များ စနစ်တကျ ထုတ်ယူခြင်း)
    final floorData = propertyData['floor_data'] ?? {};
    final roomStructure = propertyData['room_structure'] ?? {};
    final features = propertyData['features'] ?? {};
    final activeButtons = propertyData['active_buttons'] ?? {};

    // 💰 ၃။ အမျိုးအစား နှင့် ဈေးနှုန်း နောက်ဆက်တွဲ Logic 
    String typeStr = propertyData['offer_type']?.toString() ?? 'sale';
    String typeLabel = _getOfferTypeMyanmar(typeStr);
    String priceSuffix = (typeStr == 'sale' || typeStr == 'buy') ? "သိန်း" : "ကျပ်/တစ်လ";

    // 📝 ၄။ Column ထဲတွင် Variable မကြေညာမိစေရန် ဤနေရာတွင် ကြိုတင် Extract လုပ်ခြင်း
    String remark = propertyData['remark'] ?? propertyData['description'] ?? '';

    // 📍 ၅။ တည်နေရာ စာသား ပေါင်းစပ်ခြင်း (စုံလင်စွာ ပို့ပေးလာပါက စာကြောင်းတစ်ခုတည်း ဖြစ်အောင် တွဲပေးမည်)
    String displayLocation = propertyData['location'] ?? '';
    if (displayLocation.isEmpty) {
      String region = propertyData['region'] ?? '';
      String township = propertyData['township'] ?? '';
      String quarter = propertyData['quarter'] ?? '';
      String road = propertyData['road'] ?? '';
      List<String> locParts = [];
      if (road.isNotEmpty) locParts.add("$road လမ်း");
      if (quarter.isNotEmpty) locParts.add("$quarter ရပ်ကွက်");
      if (township.isNotEmpty) locParts.add(township);
      if (region.isNotEmpty) locParts.add(region);
      displayLocation = locParts.isNotEmpty ? locParts.join("၊ ") : 'N/A';
    }

    // 📞 ဖုန်းနံပါတ်များ စုစည်းခြင်း
    String primaryPhone = propertyData['contact_phone'] ?? propertyData['phone'] ?? 'N/A';
    String? secondaryPhone = propertyData['contact_phone1'];

    return Scaffold(
      backgroundColor: const Color(0xFFFAFBFF),
      bottomNavigationBar: _buildBottomActionBar(activeButtons, primaryPhone),
      body: CustomScrollView(
        physics: const BouncingScrollPhysics(),
        slivers: [
          // ==================== IMAGE SLIDER APP BAR ====================
          SliverAppBar(
            expandedHeight: 300,
            pinned: true,
            backgroundColor: Colors.white,
            foregroundColor: const Color(0xFF2B3550),
            elevation: 0,
            flexibleSpace: FlexibleSpaceBar(
              background: images.isNotEmpty
                  ? PageView.builder(
                      itemCount: images.length,
                      itemBuilder: (context, index) => Image.memory(images[index], fit: BoxFit.cover),
                    )
                  : networkImages.isNotEmpty
                      ? PageView.builder(
                          itemCount: networkImages.length,
                          itemBuilder: (context, index) {
                            String imgUrl = networkImages[index]['image'] ?? '';
                            return Image.network(
                              imgUrl,
                              fit: BoxFit.cover,
                              errorBuilder: (ctx, err, stack) => _buildImagePlaceholder(Icons.broken_image_rounded),
                            );
                          },
                        )
                      : _buildImagePlaceholder(Icons.home_work_rounded),
            ),
          ),

          // ==================== PROPERTY DETAILS BODY ====================
          SliverToBoxAdapter(
            child: Container(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // ကြော်ငြာခေါင်းစဉ်
                  Text(
                    propertyData['title'] ?? 'N/A',
                    style: const TextStyle(fontSize: 21, fontWeight: FontWeight.w900, color: Color(0xFF2B3550), height: 1.3),
                  ),
                  const SizedBox(height: 16),

                  // အမျိုးအစား တဂ် နှင့် ID
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                        decoration: BoxDecoration(
                          color: const Color(0xFF3577F6).withOpacity(0.1),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(typeLabel, style: const TextStyle(color: Color(0xFF3577F6), fontWeight: FontWeight.bold, fontSize: 13)),
                      ),
                      Text(
                        "ID: #${propertyData['id']?.toString() ?? 'NEW'}",
                        style: TextStyle(color: Colors.grey.shade500, fontSize: 13, fontWeight: FontWeight.w600),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),

                  // ဈေးနှုန်း ပြသမှု
                  Text(
                    "${propertyData['price']} $priceSuffix", 
                    style: const TextStyle(fontSize: 26, fontWeight: FontWeight.w900, color: Color(0xFFEF5350)),
                  ),
                  const SizedBox(height: 14),

                  // တည်နေရာ အချက်အလက်
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Icon(Icons.location_on_rounded, size: 18, color: Color(0xFF9AA5B8)),
                      const SizedBox(width: 6),
                      Expanded(
                        child: Text(
                          displayLocation,
                          style: const TextStyle(fontSize: 14.5, color: Color(0xFF5A6B8A), height: 1.4, fontWeight: FontWeight.w500),
                        ),
                      ),
                    ],
                  ),
                  
                  // အနီးနား Landmarks ရှိလျှင် ပြရန်
                  if (propertyData['landmarks'] != null && (propertyData['landmarks'] as List).isNotEmpty) ...[
                    const SizedBox(height: 8),
                    Padding(
                      padding: const EdgeInsets.only(left: 24),
                      child: Text(
                        "📍 အနီးနား: ${(propertyData['landmarks'] as List).join(', ')}",
                        style: const TextStyle(fontSize: 13, color: Colors.blueGrey, fontStyle: FontStyle.italic),
                      ),
                    ),
                  ],

                  const SizedBox(height: 24),
                  const Divider(color: Color(0xFFEEF0F6), thickness: 1.2),
                  const SizedBox(height: 20),

                  // ==================== SPECIFICATIONS BLOCK ====================
                  const Text("အဆောက်အအုံ ဆိုင်ရာများ", style: TextStyle(fontSize: 17, fontWeight: FontWeight.bold, color: Color(0xFF2B3550))),
                  const SizedBox(height: 12),
                  _buildSpecsCard(propertyData, floorData, roomStructure, features),
                  const SizedBox(height: 20),

                  // ==================== EXTRA FEATURES AMENITIES ====================
                  const Text("အထူးပြုချက်များ", style: TextStyle(fontSize: 17, fontWeight: FontWeight.bold, color: Color(0xFF2B3550))),
                  const SizedBox(height: 12),
                  Wrap(
                    spacing: 10, runSpacing: 10,
                    children: [
                      if (propertyData['owner_direct'] == true || propertyData['isOwnerDirect'] == true) _buildFeatureChip(Icons.person_rounded, "ပိုင်ရှင်တိုက်ရိုက်"),
                      if (propertyData['price_negotiable'] == true || propertyData['isNegotiable'] == true) _buildFeatureChip(Icons.handshake_rounded, "စျေးညှိနှိုင်းနိုင်"),
                      if (features['fully_repaired'] == true || propertyData['isDecorated'] == true) _buildFeatureChip(Icons.auto_awesome_rounded, "ပြင်ဆင်ပြီး"),
                      if (propertyData['installment_available'] == true || propertyData['isPreSale'] == true) _buildFeatureChip(Icons.payments_rounded, "အရစ်ကျရ"),
                      if (propertyData['bank_transfer_accepted'] == true || propertyData['isBankTransfer'] == true) _buildFeatureChip(Icons.account_balance_rounded, "ဘဏ်ငွေလွှဲရ"),
                    ],
                  ),
                  
                  // ==================== REMARK / DESCRIPTION ====================
                  if (remark.trim().isNotEmpty) ...[
                    const SizedBox(height: 24),
                    const Text("အသေးစိတ် ရှင်းလင်းချက်", style: TextStyle(fontSize: 17, fontWeight: FontWeight.bold, color: Color(0xFF2B3550))),
                    const SizedBox(height: 12),
                    Container(
                      width: double.infinity, padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16), border: Border.all(color: const Color(0xFFE4ECFB), width: 1.2)),
                      child: Text(remark, style: const TextStyle(fontSize: 14.5, color: Color(0xFF5A6B8A), height: 1.6)),
                    ),
                  ],

                  const SizedBox(height: 24),
                  
                  // ==================== CONTACT DETAILS ====================
                  const Text("ဆက်သွယ်ရန် နံပါတ်များ", style: TextStyle(fontSize: 17, fontWeight: FontWeight.bold, color: Color(0xFF2B3550))),
                  const SizedBox(height: 12),
                  _buildPhoneBlockUI(primaryPhone, secondaryPhone),
                  const SizedBox(height: 40), 
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  // ==================== UI WIDGET HELPERS ====================

  Widget _buildSpecsCard(Map<String, dynamic> data, Map<dynamic, dynamic> floor, Map<dynamic, dynamic> rooms, Map<dynamic, dynamic> feats) {
    // ဧရိယာအကျယ်အဝန်း စာသားတွက်ချက်ခြင်း
    String areaText = data['area_dimension_text'] ?? '';
    if (areaText.isEmpty && data['width'] != null && data['length'] != null) {
      if (data['width'] > 0 && data['length'] > 0) {
        areaText = "${data['length']} ပေ x ${data['width']} ပေ";
      }
    }

    String facing = feats['facing'] ?? data['direction'] ?? '';
    String floorTypeStr = floor['type'] ?? '';
    String floorLevel = floor['level']?.toString() ?? '';

    return Container(
      width: double.infinity, padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16), border: Border.all(color: const Color(0xFFE4ECFB), width: 1.2)),
      child: Column(
        children: [
          if (areaText.isNotEmpty) _buildSpecRow(Icons.aspect_ratio_rounded, "အကျယ်အဝန်း", areaText),
          if (data['property_type'] != null) _buildSpecRow(Icons.business_rounded, "အဆောက်အအုံ", _getPropertyTypeMyanmar(data['property_type'])),
          if (floorTypeStr.isNotEmpty || floorLevel.isNotEmpty) 
            _buildSpecRow(Icons.layers_rounded, "အထပ်အချက်အလက်", "${floorTypeStr == 'ground' ? 'မြေညီထပ်' : 'အထပ်'} (${floorLevel.isEmpty ? '1' : floorLevel}) ထပ်"),
          if (facing.isNotEmpty && facing != 'အားလုံး') _buildSpecRow(Icons.explore_outlined, "မျက်နှာလှည့်", facing),
          
          // အခန်းဖွဲ့စည်းမှုများ ရှိလျှင် ပြရန်
          if (rooms.isNotEmpty && (rooms['master_bed'] != 0 || rooms['single_bed'] != 0 || rooms['bathroom'] != 0)) ...[
            const Padding(padding: EdgeInsets.symmetric(vertical: 8), child: Divider(color: Color(0xFFF0F4FC))),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                _buildRoomGridItem(Icons.bed_rounded, "Master", rooms['master_bed'] ?? 0),
                _buildRoomGridItem(Icons.single_bed_rounded, "Single", rooms['single_bed'] ?? 0),
                _buildRoomGridItem(Icons.bathroom_rounded, "W.C", rooms['bathroom'] ?? 0),
              ],
            )
          ]
        ],
      ),
    );
  }

  Widget _buildSpecRow(IconData icon, String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6),
      child: Row(
        children: [
          Icon(icon, size: 18, color: const Color(0xFF3577F6)),
          const SizedBox(width: 10),
          Text(label, style: const TextStyle(color: Color(0xFF76799C), fontSize: 14)),
          const Spacer(),
          Text(value, style: const TextStyle(color: Color(0xFF2B3550), fontWeight: FontWeight.bold, fontSize: 14.5)),
        ],
      ),
    );
  }

  Widget _buildRoomGridItem(IconData icon, String label, int count) {
    return Column(
      children: [
        Icon(icon, size: 20, color: const Color(0xFF5A6B8A)),
        const SizedBox(height: 4),
        Text("$label: $count", style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Color(0xFF2B3550))),
      ],
    );
  }

  Widget _buildPhoneBlockUI(String p1, String? p2) {
    return Container(
      width: double.infinity, padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(color: const Color(0xFFF4F7FF), borderRadius: BorderRadius.circular(16), border: Border.all(color: const Color(0xFFD6E5F8), width: 1.2)),
      child: Column(
        children: [
          Row(
            children: [
              const Icon(Icons.phone_in_talk, color: Color(0xFF3577F6), size: 18),
              const SizedBox(width: 12),
              Text(p1, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: Color(0xFF2B3550))),
            ],
          ),
          if (p2 != null && p2.isNotEmpty) ...[
            const SizedBox(height: 10),
            Row(
              children: [
                const Icon(Icons.phone_iphone_rounded, color: Color(0xFF3577F6), size: 18),
                const SizedBox(width: 12),
                Text(p2, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: Color(0xFF2B3550))),
              ],
            ),
          ]
        ],
      ),
    );
  }

  Widget _buildBottomActionBar(Map<dynamic, dynamic> buttons, String phone) {
    bool isViberEnabled = buttons['viber'] ?? false;
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
      decoration: BoxDecoration(color: Colors.white, boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 20, offset: const Offset(0, -5))]),
      child: SafeArea(
        child: Row(
          children: [
            Expanded(
              child: ElevatedButton.icon(
                onPressed: () {}, // TODO: url_launcher phone call တွဲရန်
                icon: const Icon(Icons.call, color: Colors.white, size: 20),
                label: const Text("ဖုန်းခေါ်မည်", style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold)),
                style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF3577F6), foregroundColor: Colors.white, padding: const EdgeInsets.symmetric(vertical: 14), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
              ),
            ),
            if (isViberEnabled) ...[
              const SizedBox(width: 12),
              Expanded(
                child: ElevatedButton.icon(
                  onPressed: () {}, // TODO: url_launcher viber direct link တွဲရန်
                  icon: const Icon(Icons.chat_bubble_rounded, color: Colors.white, size: 18),
                  label: const Text("Viber Chat", style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold)),
                  style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF8E24AA), foregroundColor: Colors.white, padding: const EdgeInsets.symmetric(vertical: 14), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildFeatureChip(IconData icon, String label) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(color: const Color(0xFF10B981).withOpacity(0.1), borderRadius: BorderRadius.circular(20), border: Border.all(color: const Color(0xFF10B981).withOpacity(0.3))),
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

  Widget _buildImagePlaceholder(IconData icon) {
    return Container(color: const Color(0xFFE4ECFB), child: Center(child: Icon(icon, size: 70, color: const Color(0xFF9AA5B8))));
  }

  String _getOfferTypeMyanmar(String type) {
    switch (type) {
      case 'sale': return 'အရောင်း';
      case 'rent': return 'အငှား';
      case 'buy': return 'ဝယ်လိုသည်';
      case 'tenant': return 'ငှားလိုသည်';
      default: return 'အရောင်း';
    }
  }

  String _getPropertyTypeMyanmar(String type) {
    final types = {'house': 'အိမ်', 'condo': 'ကွန်ဒို', 'apartment': 'တိုက်ခန်း', 'shop': 'ဆိုင်', 'office': 'ရုံးခန်း', 'hostel': 'အဆောင်', 'industrial': 'စက်မှုဇုန်', 'warehouse': 'ဂိုဒေါင်', 'land': 'ခြံ/မြေ'};
    return types[type] ?? type;
  }
}