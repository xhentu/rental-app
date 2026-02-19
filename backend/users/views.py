from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from firebase_admin import auth

User = get_user_model()

class FirebaseSyncView(APIView):
    """
    The main gateway. It handles both Login and Sign-up.
    We MUST check for bans here because this view is public.
    """
    permission_classes = [] # This must be empty so people can log in

    def post(self, request):
        token = request.data.get('idToken')
        if not token:
            return Response({"error": "No token provided"}, status=400)

        try:
            # 1. Verify with Google
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token.get('uid')
            
            # 2. Extract info
            firebase_email = decoded_token.get('email')
            firebase_phone = decoded_token.get('phone_number')
            firebase_photo = decoded_token.get('picture')

            # 3. Get or Create
            user, created = User.objects.get_or_create(
                firebase_uid=uid,
                defaults={
                    'email': firebase_email,
                    'phone_number': firebase_phone,
                    'profile_picture': firebase_photo,
                    'first_name': request.data.get('first_name', ''),
                    'last_name': request.data.get('last_name', ''),
                }
            )

            # 🛑 4. THE SECURITY GATE (ADD THIS NOW)
            if user.is_banned:
                return Response({
                    "error": "Account Banned",
                    "reason": user.ban_reason or "Violation of terms."
                }, status=status.HTTP_403_FORBIDDEN)

            # 5. DATA UPDATE: If user exists, sync their info
            if not created:
                # Update names if the app sends them
                user.first_name = request.data.get('first_name') or user.first_name
                user.last_name = request.data.get('last_name') or user.last_name
                user.profile_picture = firebase_photo or user.profile_picture
                user.save()

            return Response({
                "status": "success",
                "is_new_user": created,
                "user": UserSerializer(user).data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=401)

