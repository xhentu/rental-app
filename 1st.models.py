from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.contrib.postgres.indexes import GinIndex

class Listing(models.Model):
    # --- Relations & Ownership ---
    landlord = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')

    # --- 1. Offer & Property Type ---
    OFFER_CHOICES = [('sale', 'For Sale'), ('rent', 'For Rent'), ('buy', 'Want to Buy'), ('tenant', 'Want to Rent')]
    offer_type = models.CharField(max_length=10, choices=OFFER_CHOICES, db_index=True)
    
    CATEGORY_CHOICES = [
        ('house', 'House'), 
        ('condo', 'Condo'), 
        ('apartment', 'Apartment'),
        ('shop', 'Shop'),
        ('office', 'Office'),
        ('hostel', 'Hostel'), 
        ('industrial', 'Industrial Zone'),
        ('warehouse', 'Warehouse'), 
        ('land', 'Plot of Land'),
    ]
    property_type = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_index=True)

    # --- 2. Location Details ---
    region = models.CharField(max_length=50, db_index=True)    
    township = models.CharField(max_length=50, db_index=True)
    quarter = models.CharField(max_length=100, blank=True) 
    road = models.CharField(max_length=100, blank=True)
    landmarks = models.JSONField(default=list, blank=True) 
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # --- 3. Dimension, Structure, Exterior & Interior (Hybrid JSON) ---
    width = models.DecimalField(max_digits=8, decimal_places=2)
    length = models.DecimalField(max_digits=8, decimal_places=2)
    area_dimension_text = models.CharField(max_length=50, blank=True, editable=False)

    floor_data = models.JSONField(default=dict, blank=True)
    room_structure = models.JSONField(default=dict, blank=True)
    features = models.JSONField(default=dict, blank=True)

    # --- 4. Basic Info & Sales Info ---
    title = models.CharField(max_length=150)
    remark = models.CharField(max_length=200, blank=True)
    price = models.DecimalField(max_digits=16, decimal_places=2, db_index=True)
    HOSTEL_GENDER_CHOICES = [
        ('Male', 'Male Only'), 
        ('Female', 'Female Only'), 
        ('Both', 'Both'), 
        ('Family', 'Family')
    ] 
    hostel_type = models.CharField(max_length=20, choices=HOSTEL_GENDER_CHOICES, blank=True, null=True, db_index=True)
    type_of_land = models.CharField(max_length=150, blank=True, null=True)
    
    owner_direct = models.BooleanField(default=False, db_index=True) 
    price_negotiable = models.BooleanField(default=True)
    installment_available = models.BooleanField(default=False, db_index=True)
    bank_transfer_accepted = models.BooleanField(default=False)
    is_presale = models.BooleanField(default=False, db_index=True)
    
    payment_details = models.JSONField(default=dict, blank=True)

    # --- 5. Contact Info & Monetized Buttons ---
    active_buttons = models.JSONField(default=dict, blank=True)
    contact_phone = models.CharField(max_length=20)
    contact_phone1 = models.CharField(max_length=20, blank=True, null=True)
    contact_phone2 = models.CharField(max_length=20, blank=True, null=True)
    viber_contact = models.CharField(max_length=100, blank=True, null=True)
    telegram_username = models.CharField(max_length=100, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)

    # --- 6. Fixed & Non-Editable Data ---
    is_active = models.BooleanField(default=True, db_index=True)
    is_boosted = models.BooleanField(default=False, db_index=True)
    is_premium = models.BooleanField(default=False, db_index=True)
    is_completed = models.BooleanField(default=False, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField(db_index=True, blank=True)

    class Meta:
        indexes = [
            # Main search index 
            models.Index(fields=['township', 'offer_type', 'is_active'], name='idx_listing_main_search'),
            
            # Sort index - Optimized to drop the hyphen from boolean fields for index compatibility
            models.Index(fields=['is_boosted', '-created_at'], name='idx_listing_feed_sort'),
            models.Index(fields=['price'], name='idx_listing_price_sort'),

            # GIN Indexes for deep JSON searching
            GinIndex(fields=['features'], name='idx_features_gin'),
            GinIndex(fields=['room_structure'], name='idx_rooms_gin'),
            GinIndex(fields=['landmarks'], name='idx_landmarks_gin'),
        ]

    def save(self, *args, **kwargs):
        # 1. Automatically format dimensions text string
        self.area_dimension_text = f"{self.width} x {self.length} ft"
        
        # 2. FIX/UPGRADE: Premium accounts automatically gain boosted sorting visibility
        if self.is_premium:
            self.is_boosted = True
            
        # 3. FIX/UPGRADE: If marked completed (sold/rented), take it out of the public visibility pool automatically
        if self.is_completed:
            self.is_active = False

        # 4. Initialize standard 90-day listing lifespan on first post creation
        if not self.id:
            self.expiry_date = timezone.now() + timedelta(days=90)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.get_property_type_display()})"


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(max_length=500)
    thumbnail_url = models.URLField(max_length=500, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'created_at']