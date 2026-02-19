from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    # We only return the IDs of saved listings to keep the JSON small/fast.
    saved_listings_count = serializers.SerializerMethodField()
    # saved_listings = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'firebase_uid', 'first_name', 'last_name', 
            'email', 'phone_number', 'profile_picture', 
            'is_verified_landlord', 'saved_listings', 
            'saved_listings_count', 'settings'
        ]
        read_only_fields = ['id', 'firebase_uid', 'is_verified_landlord']

    def get_saved_listings_count(self, obj):
        return obj.saved_listings.count()