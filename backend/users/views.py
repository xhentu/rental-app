from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth

User = get_user_model()

class FirebaseSyncView(APIView):
    def post(self, request):
        token = request.data.get('idToken')
        
        try:
            # 1. Verify the token with Firebase Admin SDK
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token.get('uid')
            email = decoded_token.get('email')
            
            # 2. Extract Names (Handles Google Sign-in naming)
            full_name = decoded_token.get('name', '')
            name_parts = full_name.split(' ', 1)
            first_name = name_parts[0] if len(name_parts) > 0 else ""
            last_name = name_parts[1] if len(name_parts) > 1 else ""

            # 3. Get or Create the user record
            user, created = User.objects.get_or_create(
                firebase_uid=uid,
                defaults={
                    'email': email,
                    'username': email if email else uid,
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )

            # 4. Optional: Update names if they changed since last login
            if not created:
                user.first_name = first_name
                user.last_name = last_name
                user.save()

            return Response({
                "message": "User Created" if created else "User Logged In",
                "user_id": user.id,
                "email": user.email,
                "first_name": user.first_name
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"❌ Handshake error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)