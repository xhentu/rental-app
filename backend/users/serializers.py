from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserPrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'phone_number',
            'full_name',
            'profile_picture',
            'is_verified_landlord',
            'saved_listings',
            'settings',
            'date_joined',
        )
        read_only_fields = ('id', 'is_verified_landlord', 'date_joined')

class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'profile_picture',
            'is_verified_landlord',
        )