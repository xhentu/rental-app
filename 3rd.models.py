from datetime import timedelta
from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.utils import timezone


def default_expiry_date():
    """Automatically sets expiration to 30 days from creation."""
    return timezone.now() + timedelta(days=30)


# ==========================================
# SECTOR 2: LOCATION LOOKUP MODELS
# ==========================================

class Region(models.Model):
    """Static seed table matching client-side Dart integer keys."""
    id = models.PositiveSmallIntegerField(primary_key=True)  # e.g., 1: Yangon, 2: Mandalay
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Township(models.Model):
    """Static seed table matching client-side Dart integer keys."""
    id = models.PositiveSmallIntegerField(primary_key=True)  # e.g., 101: Kamayut, 102: Sanchaung
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='townships')
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.region.name})"


# ==========================================
# MAIN LISTING MODEL (ALL 7 SECTORS)
# ==========================================

class Listing(models.Model):

    # ------------------------------------------
    # CHOICE ENUMS (Client-Side Translated)
    # ------------------------------------------
    class OfferChoices(models.IntegerChoices):
        FOR_SALE = 1, 'For Sale'
        FOR_RENT = 2, 'For Rent'

    class PropertyTypeChoices(models.IntegerChoices):
        RESIDENTIAL = 1, 'Residential'
        COMMERCIAL = 2, 'Commercial'
        INDUSTRIAL = 3, 'Industrial'
        HOSTEL = 4, 'Hostel / Co-living'

    class LandTypeChoices(models.IntegerChoices):
        GRANT = 1, 'Grant Land'
        FREEHOLD = 2, 'Ancestral/Freehold'
        PERMIT = 3, 'Permit Land'
        LICENSE = 4, 'License Land'
        SLIP = 5, 'Slip Land'
        GRANT_APPLIED = 6, 'Grant Applied'
        VILLAGE = 7, 'Village Land'
        OTHER = 99, 'Other'

    class FacingChoices(models.IntegerChoices):
        NORTH = 1, 'North'
        SOUTH = 2, 'South'
        EAST = 3, 'East'
        WEST = 4, 'West'
        NORTH_EAST = 5, 'North-East'
        NORTH_WEST = 6, 'North-West'
        SOUTH_EAST = 7, 'South-East'
        SOUTH_WEST = 8, 'South-West'

    class FurnishingChoices(models.IntegerChoices):
        UNFURNISHED = 1, 'Unfurnished'
        SEMI_FURNISHED = 2, 'Semi-Furnished'
        FULLY_FURNISHED = 3, 'Fully Furnished'
        HALL = 4, 'Hall / Bare Shell'
        UNDER_CONSTRUCTION = 5, 'Under Construction'

    class OperationalChoices(models.IntegerChoices):
        VACANT = 1, 'Vacant'
        OPERATING = 2, 'Operating / Running'
        HIATUS = 3, 'Hiatus / Temporary Closed'
        UNDER_RENOVATION = 4, 'Under Renovation'

    # ==========================================
    # SECTOR 1: OFFER CASE
    # ==========================================
    offer_type = models.PositiveSmallIntegerField(
        choices=OfferChoices.choices,
        db_index=True,
        help_text="1: For Sale, 2: For Rent"
    )
    property_type = models.PositiveSmallIntegerField(
        choices=PropertyTypeChoices.choices,
        db_index=True,
        help_text="1: Residential, 2: Commercial, 3: Industrial, 4: Hostel"
    )
    sub_property_type = models.PositiveSmallIntegerField(
        db_index=True,
        help_text="Client-side mapped integer for Condos, Apartments, Warehouses, etc."
    )
    title = models.CharField(max_length=255)
    price = models.BigIntegerField(
        db_index=True,
        help_text="Raw price stored in Lakhs or base MMK currency unit"
    )

    # ==========================================
    # SECTOR 2: LOCATION CASE
    # ==========================================
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name='listings',
        db_index=True
    )
    township = models.ForeignKey(
        Township,
        on_delete=models.PROTECT,
        related_name='listings',
        db_index=True
    )
    quarter = models.CharField(max_length=100, blank=True)
    road = models.CharField(max_length=100, blank=True)
    coordinates = models.JSONField(
        default=dict, 
        blank=True,
        help_text='Latitude & Longitude pair: {"lat": 16.8661, "lng": 96.1951}'
    )
    landmarks = models.JSONField(
        default=list, 
        blank=True,
        help_text='Array of landmark strings: ["Junction City", "Inya Lake"]'
    )

    # ==========================================
    # SECTOR 3: LAND CASE
    # ==========================================
    land_type = models.PositiveSmallIntegerField(
        choices=LandTypeChoices.choices,
        null=True,
        blank=True,
        db_index=True,
        help_text="1: Grant, 2: Freehold, 3: Permit, 4: License, 5: Slip, 6: Grant Applied, 7: Village, 99: Other"
    )
    width = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Measured in feet")
    length = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Measured in feet")
    area_sqft = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        db_index=True,
        help_text="Total plot area in square feet for range queries"
    )
    land_features = models.JSONField(
        default=dict, 
        blank=True,
        help_text='Extra land specs: {"shape": "rectangular", "corner_plot": true, "road_width_ft": 20}'
    )

    # ==========================================
    # SECTOR 4: BUILDING CASE
    # ==========================================
    facing_direction = models.PositiveSmallIntegerField(
        choices=FacingChoices.choices,
        null=True,
        blank=True,
        db_index=True,
        help_text="Facing: 1=N, 2=S, 3=E, 4=W, 5=NE, 6=NW, 7=SE, 8=SW"
    )
    furnishing = models.PositiveSmallIntegerField(
        choices=FurnishingChoices.choices,
        null=True,
        blank=True,
        db_index=True,
        help_text="1=Unfurnished, 2=Semi, 3=Full, 4=Hall, 5=Under Construction"
    )
    building_width = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Measured in feet")
    building_length = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Measured in feet")
    building_height = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Clear height in feet")
    building_area = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        db_index=True,
        help_text="Usable floor area in square feet"
    )
    total_floors = models.PositiveSmallIntegerField(default=1, help_text="Total story count")
    floor_level = models.PositiveSmallIntegerField(
        null=True, 
        blank=True, 
        db_index=True,
        help_text="Unit floor level (0: Ground floor, 1: 1st floor, etc.)"
    )
    room_structure = models.JSONField(
        default=dict, 
        blank=True,
        help_text='Room map: {"master_bedroom": 2, "single_bedroom": 1, "bathroom": 2}'
    )
    building_features = models.JSONField(
        default=dict, 
        blank=True,
        help_text='Building utilities: {"has_lift": true, "has_3phase_power": true, "transformer_kva": 315}'
    )

    # ==========================================
    # SECTOR 5: PROPERTY SPECIAL FEATURES
    # ==========================================
    special_features = models.JSONField(
        default=dict, 
        blank=True,
        help_text="Property-type specific JSON bucket (hostel rules, office workstations, warehouse loading bays)"
    )

    # ==========================================
    # SECTOR 6: SALES, STATUS & CONTACT CASE
    # ==========================================
    is_owner_direct = models.BooleanField(default=False, db_index=True)
    is_bank_loan_available = models.BooleanField(default=False, db_index=True)
    is_negotiable = models.BooleanField(default=True, db_index=True)
    operational_status = models.PositiveSmallIntegerField(
        choices=OperationalChoices.choices,
        default=OperationalChoices.VACANT,
        db_index=True,
        help_text="1: Vacant, 2: Operating, 3: Hiatus, 4: Under Renovation"
    )
    featured_image_url = models.URLField(max_length=500, blank=True)
    sales_info = models.JSONField(
        default=dict, 
        blank=True,
        help_text='Lease terms: {"min_lease_months": 6, "advance_months": 6, "deposit_amount": 500000}'
    )
    status_info = models.JSONField(
        default=dict, 
        blank=True,
        help_text='Lifecycle: {"marketplace_status": "active", "available_from_date": "2026-10-01"}'
    )
    contact_info = models.JSONField(
        default=dict, 
        blank=True,
        help_text='Contacts: {"contact_person": "U Ba", "primary_phone": "09123456789", "social_links": {...}}'
    )

    # ==========================================
    # SECTOR 7: SYSTEM META & FIXED CASE
    # ==========================================
    landlord = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listings',
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField(default=default_expiry_date, db_index=True)
    post_cost = models.PositiveIntegerField(default=0)
    is_boosted = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ['-is_boosted', '-created_at']
        indexes = [
            # Compound index for general location searches
            models.Index(fields=['township', 'region'], name='idx_location_lookup'),
            
            # Feed sorting index: Boosted first, then newest
            models.Index(fields=['-is_boosted', '-created_at'], name='idx_boost_created'),
            
            # Expiry lookup index for background cron jobs
            models.Index(fields=['expiry_date'], name='idx_expiry_lookup'),

            # GIN Indexes for fast JSON containment lookups
            GinIndex(fields=['landmarks'], name='idx_landmarks_gin'),
            GinIndex(fields=['land_features'], name='idx_land_features_gin'),
            GinIndex(fields=['room_structure'], name='idx_room_structure_gin'),
            GinIndex(fields=['building_features'], name='idx_bldg_features_gin'),
            GinIndex(fields=['special_features'], name='idx_special_features_gin'),
            GinIndex(fields=['sales_info'], name='idx_sales_info_gin'),
            GinIndex(fields=['status_info'], name='idx_status_info_gin'),
            GinIndex(fields=['contact_info'], name='idx_contact_info_gin'),
        ]

    def __str__(self):
        return f"[{self.id}] {self.title} - {self.price} Lakhs"