from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils import timezone
from firebase_admin import auth
from .serializers import UserPrivateSerializer, UserPublicSerializer
from rest_framework.permissions import AllowAny

User = get_user_model()

class FirebaseBaseView(APIView):
    permission_classes = []

    def verify_firebase_token(self, request):
        # 1. Try to get token from Authorization Header (standard)
        auth_header = request.headers.get('Authorization')
        token = None

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        # 2. Fallback to Request Body (for your POST login/register calls)
        if not token:
            token = request.data.get('idToken')

        if not token:
            print("❌ DEBUG: No token found in Header or Body")
            return None, Response({"error": "No token provided"}, status=400)

        try:
            decoded_token = auth.verify_id_token(token)
            print(f"✅ DEBUG: Token verified for UID: {decoded_token.get('uid')}")
            return decoded_token, None
        except Exception as e:
            print(f"❌ DEBUG: Firebase Error: {str(e)}")
            return None, Response({"error": str(e)}, status=401)
            
class RegisterView(FirebaseBaseView):
    authentication_classes = []
    def post(self, request):
        decoded_token, error_response = self.verify_firebase_token(request)
        if error_response: return error_response

        uid = decoded_token.get('uid')
        if User.objects.filter(firebase_uid=uid).exists():
            return Response({"error": "Account exists"}, status=400)

        # Create user
        # We prioritize 'name' from the request body (Flutter) 
        # then fallback to Firebase display name if it exists.
        full_name = request.data.get('name') or decoded_token.get('name', '')

        user = User.objects.create(
            firebase_uid=uid,
            full_name=full_name, # ✅ New field
            email=decoded_token.get('email'), 
            phone_number=request.data.get('phone_number') or decoded_token.get('phone_number'),
            profile_picture=decoded_token.get('picture'),
        )
        
        serializer = UserPrivateSerializer(user)
        return Response({"status": "created", "user": serializer.data}, status=201)

class LoginView(FirebaseBaseView):
    # authentication_classes = [] # Ensure no global auth interferes
    permission_classes = [AllowAny]
    def post(self, request):
        print("🚀 DEBUG: I AM FINALLY RUNNING!")
        decoded_token, error_response = self.verify_firebase_token(request)
        if error_response: return error_response

        uid = decoded_token.get('uid')
        user = User.objects.filter(firebase_uid=uid).first()

        if not user:
            return Response({"error": "Please register"}, status=404)

        # Update login info from Firebase token
        user.email = decoded_token.get('email') or user.email
        user.profile_picture = decoded_token.get('picture') or user.profile_picture
        
        # Only update phone if Firebase actually has a verified one
        user.phone_number = request.data.get('phone_number') or decoded_token.get('phone_number') or user.phone_number
        user.full_name = request.data.get('name') or user.full_name

        user.last_login = timezone.now()
        user.save()

        serializer = UserPrivateSerializer(user)
        return Response({"status": "success", "user": serializer.data})

class UserProfileView(FirebaseBaseView):
    def get(self, request):
        decoded_token, error_response = self.verify_firebase_token(request)
        if error_response: 
            return error_response

        uid = decoded_token.get('uid')
        user = User.objects.filter(firebase_uid=uid).first()
        
        if not user:
            print(f"⚠️ DEBUG: User {uid} not found in Django DB")
            return Response({"error": "User not found"}, status=404)

        serializer = UserPrivateSerializer(user)
        print(f"👤 DEBUG: Fetching profile for {user.full_name}")
        return Response(serializer.data)