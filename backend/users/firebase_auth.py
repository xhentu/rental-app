from rest_framework import authentication, exceptions
from firebase_admin import auth as firebase_admin_auth
from django.contrib.auth import get_user_model

User = get_user_model()

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        id_token = auth_header.split(' ').pop()

        try:
            # 1. Verify token with Google/Firebase
            decoded_token = firebase_admin_auth.verify_id_token(id_token)
        except Exception:
            raise exceptions.AuthenticationFailed('Invalid or expired Firebase Token')

        uid = decoded_token.get('uid')
        
        # 2. Look up the user in our local DB
        user = User.objects.filter(firebase_uid=uid).first()

        # 3. Security Check: Banned users get kicked out immediately
        if user and user.is_banned:
            raise exceptions.PermissionDenied(f"Account Banned: {user.ban_reason}")

        # Return user if found, or None if they need to sync/sign-up
        return (user, None)