from rest_framework import authentication, exceptions
from firebase_admin import auth

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None  # No token, treat as Guest (AllowAny)

        id_token = auth_header.split(' ').pop()
        try:
            # The actual "Handshake" with Firebase
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise exceptions.AuthenticationFailed('Invalid Firebase Token')

        uid = decoded_token.get('uid')
        # Here, you would normally get or create a user in your local DB
        # For now, we'll return None to keep it simple, but token is verified!
        return (None, None)