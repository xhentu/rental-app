from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth

User = get_user_model()

class FirebaseSyncView(APIView):
    # This view doesn't require DRF login because it IS the login
    permission_classes = [] 

    def post(self, request):
        token = request.data.get('idToken')
        # Custom data from mobile app form (only used on first signup)
        chosen_first_name = request.data.get('first_name', '')
        chosen_last_name = request.data.get('last_name', '')

        try:
            from firebase_admin import auth
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token.get('uid')
            
            # Firebase gives us these depending on login method
            email = decoded_token.get('email')
            phone = decoded_token.get('phone_number')
            photo = decoded_token.get('picture')

            # Create or get user
            user, created = User.objects.get_or_create(
                firebase_uid=uid,
                defaults={
                    'email': email,
                    'phone_number': phone,
                    'profile_picture': photo,
                    'first_name': chosen_first_name,
                    'last_name': chosen_last_name,
                }
            )

            # If user already existed, update their profile photo/email in case it changed
            if not created:
                user.profile_picture = photo or user.profile_picture
                user.save()

            return Response({
                "status": "success",
                "is_new_user": created,
                "user_id": user.id
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=401)