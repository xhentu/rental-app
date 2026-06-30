# listings/serializers.py
from rest_framework import serializers
from .models import Listing, ListingImage

class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ['id', 'image_url', 'thumbnail_url', 'is_primary']

# 1. LIGHTWEIGHT FEED SERIALIZER (Optimized for fast scrolling)
class ListingFeedSerializer(serializers.ModelSerializer):
    # Only pull the primary image thumbnail for the feed card
    cover_image = serializers.SerializerMethodField()
    property_type_display = serializers.CharField(source='get_property_type_display', read_only=True)
    offer_type_display = serializers.CharField(source='get_offer_type_display', read_only=True)

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'price', 'offer_type', 'offer_type_display',
            'property_type', 'property_type_display', 'region', 'township', 
            'cover_image', 'is_boosted', 'is_premium', 'created_at'
        ]

    def get_cover_image(self, obj):
        # Grab the primary cover image or fallback to the first image
        primary_img = obj.images.filter(is_primary=True).first() or obj.images.first()
        if primary_img:
            return primary_img.thumbnail_url or primary_img.image_url
        return None

# 2. HEAVY DETAIL SERIALIZER (Pull everything for the dedicated property page)
class ListingDetailSerializer(serializers.ModelSerializer):
    images = ListingImageSerializer(many=True, read_only=True)
    property_type_display = serializers.CharField(source='get_property_type_display', read_only=True)
    offer_type_display = serializers.CharField(source='get_offer_type_display', read_only=True)
    hostel_type_display = serializers.CharField(source='get_hostel_type_display', read_only=True)
    all_contact_numbers = serializers.SerializerMethodField()

    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields = ['landlord', 'area_dimension_text', 'is_active', 'expiry_date', 'created_at', 'updated_at']

    def get_all_contact_numbers(self, obj):
        numbers = [obj.contact_phone, obj.contact_phone1, obj.contact_phone2]
        return [n for n in numbers if n and n.strip()]