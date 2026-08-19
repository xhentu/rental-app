// lib/services/api_service.dart
import 'dart:convert';
import 'dart:io'; // File သုံးရန်အတွက်
import 'dart:typed_data'; // Uint8List သုံးရန်အတွက်
import 'package:http/http.dart' as http;

class ApiService {
  // 🌐 သင်အသုံးပြုမည့် Base URL
  static const String baseUrl = 'http://127.0.0.1:8000/api'; 

  /// Real-time Home Feed အား ဆွဲယူခြင်း
  static Future<Map<String, dynamic>?> fetchPropertyFeed({
    String? cursorUrl,
    String category = 'all',
    Map<String, dynamic>? activeFilters,
    bool forceRefresh = false,
  }) async {
    try {
      Uri url;
      
      if (cursorUrl != null) {
        url = Uri.parse(cursorUrl);
      } else {
        url = Uri.parse('$baseUrl/listings/'); 
        Map<String, String> queryParams = {};

        if (forceRefresh) queryParams['force_refresh'] = 'true';
        if (category == 'sale') queryParams['offer_type'] = 'sale';
        if (category == 'rent') queryParams['offer_type'] = 'rent';

        if (activeFilters != null) {
          if (activeFilters['township'] != null && activeFilters['township'] != 'အားလုံး') {
            queryParams['township'] = activeFilters['township'];
          }
          if (activeFilters['state'] != null && activeFilters['state'] != 'အားလုံး') {
            queryParams['region'] = activeFilters['state'];
          }
          if (activeFilters['propertyType'] != null && activeFilters['propertyType'] != 'အားလုံး') {
            switch (activeFilters['propertyType']) {
              case 'အိမ်': queryParams['property_type'] = 'house'; break;
              case 'ကွန်ဒို': queryParams['property_type'] = 'condo'; break;
              case 'တိုက်ခန်း': queryParams['property_type'] = 'apartment'; break;
              case 'မြေ': queryParams['property_type'] = 'land'; break;
              case 'ဂိုဒေါင်': queryParams['property_type'] = 'warehouse'; break;
              default: queryParams['property_type'] = activeFilters['propertyType'];
            }
          }
          if (activeFilters['minPrice'] != null && activeFilters['minPrice'].toString().isNotEmpty) {
            queryParams['min_price'] = activeFilters['minPrice'].toString();
          }
          if (activeFilters['maxPrice'] != null && activeFilters['maxPrice'].toString().isNotEmpty) {
            queryParams['max_price'] = activeFilters['maxPrice'].toString();
          }
        }

        if (queryParams.isNotEmpty) {
          url = url.replace(queryParameters: queryParams);
        }
      }

      print("🌐 [API FETCH] Requesting URL: $url");
      final response = await http.get(url, headers: {'Accept': 'application/json'});

      if (response.statusCode == 200) {
        final decodedBody = jsonDecode(utf8.decode(response.bodyBytes));
        return decodedBody as Map<String, dynamic>;
      } else {
        print("❌ Feed Fetch Failed Status: ${response.statusCode}");
        return null;
      }
    } catch (e) {
      print("🚨 ApiService Fetch Error: $e");
      return null;
    }
  }

  /// 📤 အိမ်ခြံမြေကြော်ငြာအသစ် တင်ခြင်း
  /// 'authToken' ရော၊ နောက်ထပ် ပါလာနိုင်သမျှ Named Parameters အားလုံးကို လက်ခံနိုင်ရန် ပြုပြင်ထားပါသည်
  static Future<bool> uploadProperty({
    Map<String, dynamic> formData = const {},
    List<dynamic> images = const [],
    String authToken = '', // upload_screen က ပို့သော Firebase Token အား ဖမ်းယူခြင်း
  }) async {
    try {
      var request = http.MultipartRequest('POST', Uri.parse('$baseUrl/listings/create/'));
      
      // 🔑 Bearer Token ရှိပါက Header ထဲသို့ ထည့်သွင်းခြင်း
      if (authToken.isNotEmpty) {
        request.headers['Authorization'] = 'Bearer $authToken';
      }
      request.headers['Accept'] = 'application/json';
      
      // 📝 ၁။ သာမန် Text Data များကို Field ထဲသို့ ထည့်ခြင်း
      formData.forEach((key, value) {
        if (value != null && value is! Map && value is! List) {
          request.fields[key] = value.toString();
        } else if (value is Map || value is List) {
          request.fields[key] = jsonEncode(value);
        }
      });

      // 🖼️ ၂။ ရွေးချယ်ထားသော ပုံများရှိပါက Multipart File အဖြစ် ထည့်သွင်းခြင်း
      for (var img in images) {
        if (img is File) {
          var multipartFile = await http.MultipartFile.fromPath('uploaded_images', img.path);
          request.files.add(multipartFile);
        } else if (img is Uint8List) {
          var multipartFile = http.MultipartFile.fromBytes(
            'uploaded_images',
            img,
            filename: 'property_img_${DateTime.now().millisecondsSinceEpoch}.jpg',
          );
          request.files.add(multipartFile);
        }
      }

      print("📤 [API UPLOAD] Sending data to: ${request.url}");
      var streamedResponse = await request.send();
      var response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 201 || response.statusCode == 200) {
        print("✅ Property Uploaded Successfully!");
        return true;
      } else {
        print("❌ Upload Failed Status: ${response.statusCode}");
        print("❌ Response Body: ${response.body}");
        return false;
      }
    } catch (e) {
      print("🚨 ApiService Upload Error: $e");
      return false;
    }
  }

  /// မြန်မာစာလုံးမှ English Backend Key သို့ Mapping လုပ်ပေးသည့် Helper Function
  static String _mapPropertyTypeToEnglish(String mmType) {
    switch (mmType) {
      case 'အိမ်': return 'house';
      case 'ကွန်ဒို': return 'condo';
      case 'တိုက်ခန်း': return 'apartment';
      case 'ဆိုင်ခန်း': return 'shop';
      case 'ရုံးခန်း': return 'office';
      case 'အဆောင်': return 'hostel';
      case 'စက်မှုဇုန်': return 'industrial';
      case 'ဂိုဒေါင်': return 'warehouse';
      case 'ခြံမြေ': return 'land';
      default: return 'house';
    }
  }
}