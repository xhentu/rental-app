from rest_framework import authentication, exceptions
from firebase_admin import auth as firebase_admin_auth
from django.contrib.auth import get_user_model

User = get_user_model()

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Use .get() for safer access
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None

        parts = auth_header.split()
        if parts[0].lower() != 'bearer' or len(parts) != 2:
            return None # Skip this auth method if header is malformed

        id_token = parts[1]

        try:
            decoded_token = firebase_admin_auth.verify_id_token(id_token)
        except Exception as e:
            # This is likely why you get the 400
            print(f"🔥 Firebase Auth Error: {e}") 
            raise exceptions.AuthenticationFailed('Invalid or expired Firebase Token')

        uid = decoded_token.get('uid')
        user = User.objects.filter(firebase_uid=uid).first()

        if not user:
            # If the user isn't in Django yet, returning None here 
            # allows the View to handle the "Not Found" case manually
            # instead of crashing with a 400.
            return None 

        if user.is_banned:
            raise exceptions.PermissionDenied(f"Account Banned: {user.ban_reason}")

        return (user, None)

        