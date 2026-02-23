from rest_framework import serializers
from django.utils import timezone
from .models import Listing, ListingImage
from users.serializers import UserPublicSerializer

class ListingImageSerializer(serializers.ModelSerializer):
    """
    Used for full-quality image delivery in Detail screens.
    """
    class Meta:
        model = ListingImage
        fields = ['id', 'image_url', 'thumbnail_url', 'is_primary']

class ListingFeedSerializer(serializers.ModelSerializer):
    """
    Facebook-style Feed Serializer.
    Optimized for speed: Small JSON, Small Images.
    """
    landlord = UserPublicSerializer(read_only=True)
    # Only providing the primary thumbnail to save bandwidth
    cover_thumbnail = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'price', 'offer_type', 'property_type', 
            'township', 'area_dimension_text', 'cover_thumbnail', 
            'landlord', 'is_boosted', 'owner_direct', 'created_at'
        ]

    def get_cover_thumbnail(self, obj):
        # We fetch only the thumbnail created by Celery/Redis
        image = obj.images.filter(is_primary=True).first()
        if image:
            return image.thumbnail_url or image.image_url # Fallback if celery hasn't finished
        return None

class ListingDetailSerializer(serializers.ModelSerializer):
    """
    Full Detail Serializer.
    Includes all features, landmarks, and contact masking logic.
    """
    landlord = UserPublicSerializer(read_only=True)
    images = ListingImageSerializer(many=True, read_only=True)
    days_left = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ['landlord', 'area_dimension_text', 'expiry_date']

    def get_days_left(self, obj):
        if obj.expiry_date:
            remaining = obj.expiry_date - timezone.now()
            return max(0, remaining.days)
        return 0

    def to_representation(self, instance):
        """
        Monetization Logic: Protects contact info based on 'active_buttons' JSON.
        """
        rep = super().to_representation(instance)
        buttons = instance.active_buttons or {}

        # If button is False/Missing, mask the data
        if not buttons.get('call'):
            rep['contact_phone'] = "Contact hidden"
        
        if not buttons.get('viber'):
            rep['viber_contact'] = None
            
        if not buttons.get('telegram'):
            rep['telegram_username'] = None
            
        if not buttons.get('whatsapp'):
            rep['whatsapp_number'] = None

        return rep