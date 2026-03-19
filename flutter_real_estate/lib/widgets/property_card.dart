import 'dart:typed_data'; 
import 'package:flutter/material.dart';
import '../screens/property_detail_screen.dart'; 

class PropertyCard extends StatelessWidget {
  final Map<String, dynamic> fullPropertyData;
  final String title;
  final String price;
  final String location;
  final String imageUrl;
  final String type; 
  final String specs;

  const PropertyCard({
    super.key,
    required this.fullPropertyData,
    required this.title,
    required this.price,
    required this.location,
    required this.imageUrl,
    required this.type,
    required this.specs,
  });

  @override
  Widget build(BuildContext context) {
    bool isSaleOrBuy = type == 'For Sale' || type == 'အရောင်း' || type == 'Want to Buy' || type == 'ဝယ်လိုသည်';
    final Color badgeColor = isSaleOrBuy ? const Color(0xFFEF5350) : const Color(0xFF10B981);
    
    String badgeText = "အရောင်း";
    String priceSuffix = "သိန်း";

    if (type == 'For Rent' || type == 'အငှား') {
      badgeText = "အငှား";
      priceSuffix = "ကျပ်/လ";
    } else if (type == 'Want to Buy' || type == 'ဝယ်လိုသည်') {
      badgeText = "ဝယ်လိုသည်";
    } else if (type == 'Want to Rent' || type == 'ငှားလိုသည်') {
      badgeText = "ငှားလိုသည်";
      priceSuffix = "ကျပ်/လ";
    }

    List<Uint8List> localImages = [];
    if (fullPropertyData.containsKey('localImages') && fullPropertyData['localImages'] != null) {
      localImages = List<Uint8List>.from(fullPropertyData['localImages']);
    }

    return Container(
      margin: const EdgeInsets.only(bottom: 20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        boxShadow: [
          BoxShadow(
            color: const Color(0xFF3577F6).withOpacity(0.08),
            blurRadius: 18,
            offset: const Offset(0, 8),
          ),
        ],
        border: Border.all(color: const Color(0xFFF0F5FF), width: 1.5),
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(20),
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => PropertyDetailScreen(
                  propertyData: fullPropertyData, 
                  images: localImages, 
                ),
              ),
            );
          },
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // 1. ပုံ နှင့် Badge အပိုင်း
              Stack(
                children: [
                  ClipRRect(
                    borderRadius: const BorderRadius.vertical(top: Radius.circular(18)),
                    child: localImages.isNotEmpty
                        ? Image.memory(
                            localImages[0], 
                            height: 190,
                            width: double.infinity,
                            fit: BoxFit.cover,
                          )
                        : Image.network(
                            imageUrl,
                            height: 190,
                            width: double.infinity,
                            fit: BoxFit.cover,
                            errorBuilder: (context, error, stackTrace) {
                              return Container(
                                height: 190,
                                color: const Color(0xFFE4ECFB),
                                child: const Center(child: Icon(Icons.broken_image_rounded, size: 50, color: Color(0xFF9AA5B8))),
                              );
                            },
                          ),
                  ),
                  Positioned(
                    top: 12, left: 12,
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                      decoration: BoxDecoration(
                        color: badgeColor,
                        borderRadius: BorderRadius.circular(8),
                        boxShadow: [
                          BoxShadow(color: badgeColor.withOpacity(0.4), blurRadius: 6, offset: const Offset(0, 3)),
                        ],
                      ),
                      child: Text(
                        badgeText, 
                        style: const TextStyle(color: Colors.white, fontSize: 12.5, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ),
                  Positioned(
                    top: 12, right: 12,
                    child: Container(
                      padding: const EdgeInsets.all(6),
                      decoration: const BoxDecoration(
                        color: Colors.white,
                        shape: BoxShape.circle,
                        boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 4)],
                      ),
                      child: const Icon(Icons.favorite_border_rounded, size: 20, color: Color(0xFFEF5350)),
                    ),
                  ),
                ],
              ),

              // 2. စာသား အချက်အလက်များ အပိုင်း (🔴 မင်းလိုချင်သည့် အစီအစဉ်အတိုင်း ပြင်ထားသည်)
              Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // 🔴 ၁။ ခေါင်းစဉ် (Title) ကို အပေါ်ဆုံး တင်လိုက်ပါပြီ
                    Text(
                      title, 
                      style: const TextStyle(fontSize: 17, fontWeight: FontWeight.bold, color: Color(0xFF2B3550), height: 1.3), 
                      maxLines: 2, // စာတန်းရှည်လျှင် ၂ ကြောင်းအထိ ပေါ်ခွင့်ပေးမည်
                      overflow: TextOverflow.ellipsis,
                    ),
                    const SizedBox(height: 12),

                    // 🔴 ၂။ စျေးနှုန်း နှင့် အကျယ်အဝန်း
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        Text(
                          "$price $priceSuffix", 
                          style: const TextStyle(fontSize: 21, fontWeight: FontWeight.w900, color: Color(0xFF3577F6)),
                        ),
                        Row(
                          children: [
                            const Icon(Icons.aspect_ratio_rounded, size: 14, color: Color(0xFF9AA5B8)),
                            const SizedBox(width: 4),
                            Text(
                              specs.split('|')[0].trim(), // Area အပိုင်းကိုသာ ဖြတ်ယူပြမည်
                              style: const TextStyle(color: Color(0xFF76799C), fontSize: 12.5, fontWeight: FontWeight.w600),
                            ),
                          ],
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    
                    // 🔴 ၃။ တည်နေရာ (Location & Nearby)
                    Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Padding(
                          padding: EdgeInsets.only(top: 2),
                          child: Icon(Icons.location_on_rounded, size: 16, color: Color(0xFF9AA5B8)),
                        ),
                        const SizedBox(width: 6),
                        Expanded(
                          child: Text(
                            location, // 👈 ဤနေရာတွင် 'Near ...' ဆိုသည့် အနီးအနား အချက်အလက်ပါ တစ်ခါတည်း ပေါ်မည်
                            style: const TextStyle(color: Color(0xFF5A6B8A), fontSize: 13.5, height: 1.4, fontWeight: FontWeight.w500),
                            maxLines: 2, // Location ရှည်လျှင် ၂ ကြောင်းပြမည်
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}