from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

class Listing(models.Model):
    # --- Relations & Ownership ---
    landlord = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='listings'
    )

    # --- Basic Info ---
    OFFER_CHOICES = [('sale', 'For Sale'), ('rent', 'For Rent')]
    offer_type = models.CharField(max_length=10, choices=OFFER_CHOICES)
    
    CATEGORY_CHOICES = [
        ('house', 'House'),
        ('condo', 'Condo'),
        ('apartment', 'Apartment'),
        ('warehouse', 'Warehouse'),
        ('land', 'Plot of Land'),
    ]
    property_type = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2) 
    
    # --- Installment & Presale Logic ---
    is_installment_available = models.BooleanField(default=False)
    is_presale = models.BooleanField(default=False)
    # Optional: You can store installment terms like {"down_payment": "30%", "period": "2 years"}
    payment_details = models.JSONField(default=dict, blank=True)

    # --- Dimensions ---
    width = models.DecimalField(max_digits=10, decimal_places=2, help_text="in feet")
    length = models.DecimalField(max_digits=10, decimal_places=2, help_text="in feet")
    # Computed string for display, e.g., "40 x 60"
    area_dimension_text = models.CharField(max_length=100, blank=True) 

    # --- Location Details ---
    region = models.CharField(max_length=100)    
    township = models.CharField(max_length=100)  
    quarter = models.CharField(max_length=100, blank=True) # Ward (e.g., 10 Quarter)
    road = models.CharField(max_length=255, blank=True)
    
    # Landmarks now includes the "Street" and nearby spots
    # Example: ["No. 45 Street", "Near Sein Gay Har", "Near Bus Stop"]
    landmarks = models.JSONField(default=list, blank=True)
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # --- Flexible Features ---
    # {"rooms": 3, "master_bedroom": 1, "floor": "Ground", "tags": ["corner_unit"]}
    features = models.JSONField(default=dict, blank=True)

    # --- Contact Info & Monetized Buttons ---
    # Store: {"call": True, "viber": True, "telegram": False}
    active_buttons = models.JSONField(default=dict, blank=True)
    contact_phone = models.CharField(max_length=20)
    viber_contact = models.CharField(max_length=100, blank=True, null=True)
    telegram_username = models.CharField(max_length=100, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)

    # --- Status & Logistics ---
    is_active = models.BooleanField(default=True)
    is_boosted = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False) # Sold/Rented
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        # 1. Calculate Area Text automatically
        if not self.area_dimension_text:
            self.area_dimension_text = f"{self.width} x {self.length} ft"
        
        # 2. Set Expiry on first creation
        if not self.id:
            self.expiry_date = timezone.now() + timedelta(days=90)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.property_type})"


class ListingImage(models.Model):
    listing = models.ForeignKey(
        Listing, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    # We store the URL from your future Cloud Storage (IBM S3 / Neon)
    image_url = models.URLField(max_length=500)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'created_at']