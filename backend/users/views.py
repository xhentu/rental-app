from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from firebase_admin import auth
# Import both serializers we created earlier
from .serializers import UserPrivateSerializer, UserPublicSerializer

User = get_user_model()

class FirebaseBaseView(APIView):
    """
    Base class to handle Firebase token verification.
    """
    permission_classes = []

    def verify_firebase_token(self, request):
        token = request.data.get('idToken')
        if not token:
            return None, Response({"error": "No token provided"}, status=400)
        try:
            decoded_token = auth.verify_id_token(token)
            return decoded_token, None
        except Exception as e:
            return None, Response({"error": str(e)}, status=401)
            
class RegisterView(FirebaseBaseView):
    def post(self, request):
        decoded_token, error_response = self.verify_firebase_token(request)
        if error_response: return error_response

        uid = decoded_token.get('uid')
        if User.objects.filter(firebase_uid=uid).exists():
            return Response({"error": "Account exists"}, status=400)

        # Create user
        user = User.objects.create(
            firebase_uid=uid,
            email=decoded_token.get('email'), 
            phone_number=decoded_token.get('phone_number'),
            profile_picture=decoded_token.get('picture'),
            first_name=request.data.get('first_name', ''),
            last_name=request.data.get('last_name', ''),
        )
        # Use UserPrivateSerializer because this is the user's own account creation
        serializer = UserPrivateSerializer(user)
        return Response({"status": "created", "user": serializer.data}, status=201)

class LoginView(FirebaseBaseView):
    def post(self, request):
        decoded_token, error_response = self.verify_firebase_token(request)
        if error_response: return error_response

        uid = decoded_token.get('uid')
        user = User.objects.filter(firebase_uid=uid).first()

        if not user:
            return Response({"error": "Please register"}, status=404)

        # Update login info
        user.email = decoded_token.get('email') or user.email
        user.phone_number = decoded_token.get('phone_number') or user.phone_number
        user.profile_picture = decoded_token.get('picture') or user.profile_picture
        
        user.last_login = timezone.now()
        user.save()

        # Use UserPrivateSerializer for the response
        serializer = UserPrivateSerializer(user)
        return Response({"status": "success", "user": serializer.data})