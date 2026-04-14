# from rest_framework import serializers
# from .models import User

# class UserPublicSerializer(serializers.ModelSerializer):
#     """
#     Public-facing info. Used when someone views a house.
#     """
#     # Uses the @property from your model for a clean 'John Doe' or 'UID_123'
#     display_name = serializers.ReadOnlyField()

#     class Meta:
#         model = User
#         fields = [
#             'firebase_uid', 
#             'display_name', 
#             'profile_picture', 
#             'is_verified_landlord'
#         ]

# class UserPrivateSerializer(serializers.ModelSerializer):
#     """
#     The 'My Account' serializer. Only for the logged-in user.
#     """
#     display_name = serializers.ReadOnlyField()
#     # We provide a count instead of a list of IDs to prevent JSON bloat
#     saved_listings_count = serializers.IntegerField(source='saved_listings.count', read_only=True)

#     class Meta:
#         model = User
#         fields = [
#             'id', 
#             'firebase_uid', 
#             'first_name', 
#             'last_name', 
#             'display_name',
#             'email', 
#             'phone_number', 
#             'profile_picture', 
#             'is_verified_landlord', 
#             'settings',
#             'saved_listings_count',
#             'date_joined'
#         ]
#         read_only_fields = ['id', 'firebase_uid', 'email', 'is_verified_landlord', 'date_joined']

#     def validate_settings(self, value):
#         """Ensure settings remains a dictionary and doesn't get corrupted"""
#         if not isinstance(value, dict):
#             raise serializers.ValidationError("Settings must be a JSON object.")
#         return value

from rest_framework import serializers
from .models import User

class UserPublicSerializer(serializers.ModelSerializer):
    """
    Public-facing info. Used when someone views a house.
    """
    # Uses the @property from your model for a clean 'John Doe' or 'UID_123'
    display_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'firebase_uid', 
            'display_name', 
            'profile_picture', 
            'is_verified_landlord'
        ]

class UserPrivateSerializer(serializers.ModelSerializer):
    """
    The 'My Account' serializer. Only for the logged-in user.
    """
    display_name = serializers.ReadOnlyField()
    saved_listings_count = serializers.IntegerField(source='saved_listings.count', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 
            'firebase_uid', 
            'full_name',        # ✅ Swapped from first_name/last_name
            'display_name',
            'email', 
            'phone_number', 
            'profile_picture', 
            'is_verified_landlord', 
            'settings',
            'saved_listings_count',
            'date_joined'
        ]
        read_only_fields = ['id', 'firebase_uid', 'email', 'is_verified_landlord', 'date_joined']

    def validate_settings(self, value):
        """Ensure settings remains a dictionary and doesn't get corrupted"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Settings must be a JSON object.")
        return value