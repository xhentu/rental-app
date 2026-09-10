from django.shortcuts import render

# Create your views here.
import jwt
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserPrivateSerializer

User = get_user_model()

def generate_jwt_token(user):
    payload = {
        'user_id': user.id,
        'email': user.email,
        'phone_number': user.phone_number,
        'exp': timezone.now() + timezone.timedelta(days=7),
        'iat': timezone.now()
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

class CustomJWTAuthentication(BaseAuthentication):
    """
    Custom authentication class to decode PyJWT tokens from the Authorization header 
    and attach the user to request.user.
    """
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired.')
        except (jwt.InvalidTokenError, User.DoesNotExist):
            raise AuthenticationFailed('Invalid token.')

        return (user, token)

class RegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        full_name = request.data.get('full_name', '')

        if not email and not phone_number:
            return Response({"error": "Either an email or phone number is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

        if email and User.objects.filter(email=email).exists():
            return Response({"error": "An account with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if phone_number and User.objects.filter(phone_number=phone_number).exists():
            return Response({"error": "An account with this phone number already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            email=email,
            phone_number=phone_number,
            password=password,
            full_name=full_name
        )

        token = generate_jwt_token(user)
        serializer = UserPrivateSerializer(user)
        return Response({"status": "created", "token": token, "user": serializer.data}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        identifier = request.data.get('identifier') # Accepts email or phone number
        password = request.data.get('password')

        if not identifier or not password:
            return Response({"error": "Identifier (email or phone) and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Uses the EmailOrPhoneBackend configured in settings
        user = authenticate(username=identifier, password=password)

        if not user:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        if user.is_banned:
            return Response({"error": "This account has been banned."}, status=status.HTTP_403_FORBIDDEN)

        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        token = generate_jwt_token(user)
        serializer = UserPrivateSerializer(user)
        return Response({"status": "success", "token": token, "user": serializer.data}, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserPrivateSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserPrivateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)