from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'firebase_uid', 
            'first_name', 
            'last_name', 
            'email', 
            'phone_number', 
            'profile_picture', 
            'is_verified_landlord'
        ]
        # These should not be changed by the user directly via API
        read_only_fields = ['id', 'firebase_uid', 'is_verified_landlord']