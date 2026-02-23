from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.contrib.postgres.indexes import GinIndex

class Listing(models.Model):
    # --- Relations & Ownership ---
    landlord = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')

    # --- Basic Info ---
    OFFER_CHOICES = [('sale', 'For Sale'), ('rent', 'For Rent')]
    offer_type = models.CharField(max_length=10, choices=OFFER_CHOICES)
    
    CATEGORY_CHOICES = [
        ('house', 'House'), ('condo', 'Condo'), ('apartment', 'Apartment'),
        ('warehouse', 'Warehouse'), ('land', 'Plot of Land'),
    ]
    property_type = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    title = models.CharField(max_length=150)
    remark = models.CharField(max_length=200, blank=True)
    
    # PRICE INDEXED: Critical for range filters and sorting
    price = models.DecimalField(max_digits=12, decimal_places=2, db_index=True)
    
    # OWNER DIRECT INDEXED: For "Show only owner" filter
    owner_direct = models.BooleanField(default=False, db_index=True) 
    
    # --- Installment & Presale ---
    is_installment_available = models.BooleanField(default=False, db_index=True)
    is_presale = models.BooleanField(default=False, db_index=True)
    payment_details = models.JSONField(default=dict, blank=True)

    # --- Dimensions ---
    width = models.DecimalField(max_digits=8, decimal_places=2)
    length = models.DecimalField(max_digits=8, decimal_places=2)
    area_dimension_text = models.CharField(max_length=50, blank=True, editable=False) 

    # --- Location Details ---
    region = models.CharField(max_length=50)    
    township = models.CharField(max_length=50)
    quarter = models.CharField(max_length=50, blank=True) 
    road = models.CharField(max_length=100, blank=True)
    landmarks = models.JSONField(default=list, blank=True)
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # --- Flexible Features ---
    features = models.JSONField(default=dict, blank=True)

    # --- Contact Info & Monetized Buttons ---
    active_buttons = models.JSONField(default=dict, blank=True)
    contact_phone = models.CharField(max_length=20)
    viber_contact = models.CharField(max_length=100, blank=True, null=True)
    telegram_username = models.CharField(max_length=100, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)

    # --- Status & Logistics INDEXED ---
    is_active = models.BooleanField(default=True, db_index=True)
    is_boosted = models.BooleanField(default=False, db_index=True)
    is_premium = models.BooleanField(default=False, db_index=True)
    is_completed = models.BooleanField(default=False, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField(db_index=True)

    class Meta:
        indexes = [
            # Composite Search Index
            models.Index(fields=['township', 'offer_type', 'is_active'], name='idx_listing_main_search'),
            
            # Composite Sort Index (Price + Boost + Date)
            models.Index(fields=['-is_boosted', 'price', '-created_at'], name='idx_listing_price_sort'),

            # JSON Search Indexes
            GinIndex(fields=['features'], name='idx_features_gin'),
            GinIndex(fields=['landmarks'], name='idx_landmarks_gin'),
        ]

    def save(self, *args, **kwargs):
        self.area_dimension_text = f"{self.width} x {self.length} ft"
        if not self.id:
            self.expiry_date = timezone.now() + timedelta(days=90)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.property_type})"

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(max_length=500) # For IBM S3/Cloud storage
    thumbnail_url = models.URLField(max_length=500, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'created_at']