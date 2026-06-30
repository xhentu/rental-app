import 'dart:convert';
import 'dart:typed_data';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';

class ApiService {
  // Replace with your actual local or production server IP
  static const String baseUrl = 'http://127.0.0.1:8000/api';

  /// Sends the multi-step real estate form data along with image bytes to Django
  static Future<bool> uploadProperty({
    required Map<String, dynamic> formData,
    required List<Uint8List> images,
    required String authToken, // Pass token fetched from your auth_service.dart
  }) async {
    try {
      final uri = Uri.parse('$baseUrl/listings/create/');
      final request = http.MultipartRequest('POST', uri);

      // 1. Add Authentication Header
      request.headers['Authorization'] = 'Bearer $authToken';
      request.headers['Accept'] = 'application/json';

      // 2. Map Flat & Text Fields to Django Fields
      request.fields['title'] = formData['title'] ?? '';
      request.fields['offer_type'] = formData['offer_type'] ?? 'sale';
      request.fields['property_type'] = formData['property_type'] ?? 'house';
      request.fields['price'] = formData['price'] ?? '0';
      
      request.fields['region'] = formData['region'] ?? '';
      request.fields['township'] = formData['township'] ?? '';
      request.fields['quarter'] = formData['quarter'] ?? '';
      request.fields['road'] = formData['road'] ?? '';
      request.fields['landmarks'] = jsonEncode(formData['landmarks'] ?? []);

      request.fields['width'] = formData['width'] ?? '0';
      request.fields['length'] = formData['length'] ?? '0';
      request.fields['type_of_land'] = formData['type_of_land'] ?? '';
      request.fields['description'] = formData['description'] ?? '';

      // 3. Map Checkbox Booleans
      request.fields['owner_direct'] = (formData['owner_direct'] ?? false).toString();
      request.fields['price_negotiable'] = (formData['price_negotiable'] ?? true).toString();
      request.fields['installment_available'] = (formData['installment_available'] ?? false).toString();
      request.fields['bank_transfer_accepted'] = (formData['bank_transfer_accepted'] ?? false).toString();

      // 4. Map Contacts & Dedicated Notification Switch JSON Data
      request.fields['contact_phone'] = formData['contact_phone'] ?? '';
      request.fields['contact_phone1'] = formData['contact_phone1'] ?? '';
      request.fields['active_buttons'] = jsonEncode(formData['active_buttons'] ?? {});

      // 5. Map Complex Sub-Structures into Django JSONFields
      request.fields['floor_data'] = jsonEncode(formData['floor_data'] ?? {});
      request.fields['room_structure'] = jsonEncode(formData['room_structure'] ?? {});
      request.fields['features'] = jsonEncode(formData['features'] ?? {});

      // 6. Attach Raw Image Byte Streams to Multipart Request Pipeline
      for (int i = 0; i < images.length; i++) {
        final multipartFile = http.MultipartFile.fromBytes(
          'uploaded_images', // Field name caught by Django's self.request.FILES.getlist()
          images[i],
          filename: 'property_image_$i.jpg',
          contentType: MediaType('image', 'jpeg'),
        );
        request.files.add(multipartFile);
      }

      // 7. Stream data to the server instance
      final streamedResponse = await request.send();
      final response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 201 || response.statusCode == 200) {
        print("🎉 Property Listing Uploaded Successfully!");
        return true;
      } else {
        print("❌ Upload Failed Status: ${response.statusCode}");
        print("❌ Server Response: ${response.body}");
        return false;
      }
    } catch (e) {
      print("🚨 Error encountered while sending API request: $e");
      return false;
    }
  }
}

// ok, first, i wanna see how data is transported to server, maybe from backend side or frontend side, we just need to verify something, so print out in terminal, i need to check or maybe we can check using codes, right? i want to check which data is send, which data is saved, which data is missing from database for that instance of listing, do you understand?