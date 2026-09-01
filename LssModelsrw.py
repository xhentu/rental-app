# from datetime import timedelta
# from django.conf import settings
# from django.contrib.postgres.indexes import GinIndex
# from django.db import models
# from django.utils import timezone


# class Listing(models.Model):
#     # --- Enums & Choices ---
#     class StatusChoices(models.TextChoices):
#         ACTIVE = 'active', 'Active'
#         COMPLETED = 'completed', 'Completed'
#         EXPIRED = 'expired', 'Expired'
#         DELETED = 'deleted', 'Deleted'

#     class FurnishingChoices(models.TextChoices):
#         FULLY = 'fully', 'Fully Furnished'
#         PARTIAL = 'partial', 'Partially Furnished'
#         UNFURNISHED = 'unfurnished', 'Unfurnished / Hall'

#     OFFER_CHOICES = [
#         ('sale', 'For Sale'),
#         ('rent', 'For Rent'),
#         ('buy', 'Want to Buy'),
#         ('tenant', 'Want to Rent'),
#     ]

#     CATEGORY_CHOICES = [
#         ('house', 'House'),
#         ('condo', 'Condo'),
#         ('apartment', 'Apartment'),
#         ('shop', 'Shop'),
#         ('office', 'Office'),
#         ('hostel', 'Hostel'),
#         ('industrial', 'Industrial Zone'),
#         ('warehouse', 'Warehouse'),
#         ('land', 'Plot of Land'),
#         ('other', 'Other'),
#     ]

#     # --- Relations & Ownership ---
#     landlord = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='listings'
#     )

#     # ==========================================
#     # 1. OFFER CASE
#     # ==========================================
#     offer_type = models.CharField(max_length=10, choices=OFFER_CHOICES, db_index=True)
#     property_type = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_index=True)
#     price = models.DecimalField(max_digits=16, decimal_places=2, db_index=True)
#     payment_terms = models.JSONField(
#         default=dict, 
#         blank=True, 
#         help_text="Stores owner_direct, bank_transfer, installment, price_negotiable, etc."
#     )

#     # ==========================================
#     # 2. LOCATION CASE
#     # ==========================================
#     region = models.CharField(max_length=50, db_index=True)
#     township = models.CharField(max_length=50, db_index=True)
#     quarter = models.CharField(max_length=100, blank=True)
#     road = models.CharField(max_length=100, blank=True)
#     latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
#     longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
#     landmarks = models.JSONField(default=list, blank=True)

#     # ==========================================
#     # 3. EXTERIOR CASE
#     # ==========================================
#     width = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
#     length = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
#     building_area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_index=True)
#     land_area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_index=True)
#     exterior_specs = models.JSONField(
#         default=dict, 
#         blank=True, 
#         help_text="Land shape, land type, drainage, container access, parking bays, etc."
#     )

#     # ==========================================
#     # 4. INTERIOR CASE
#     # ==========================================
#     bedrooms = models.PositiveSmallIntegerField(default=0, db_index=True)
#     bathrooms = models.PositiveSmallIntegerField(default=0)
#     floor_level = models.SmallIntegerField(null=True, blank=True, db_index=True, help_text="0=Ground, 1=1st Floor, etc.")
#     furnishing = models.CharField(
#         max_length=15, 
#         choices=FurnishingChoices.choices, 
#         default=FurnishingChoices.UNFURNISHED, 
#         db_index=True
#     )
#     interior_specs = models.JSONField(
#         default=dict, 
#         blank=True, 
#         help_text="Floor material, room structure layout, mezzanine details, ceiling height."
#     )

#     # ==========================================
#     # 5. BASIC INFO CASE
#     # ==========================================
#     title = models.CharField(max_length=150)
#     remark = models.CharField(max_length=200, blank=True)
#     primary_thumbnail_url = models.URLField(max_length=500, blank=True, null=True)
#     contacts = models.JSONField(
#         default=dict, 
#         blank=True, 
#         help_text="Primary phone, secondary phones, Viber, Telegram, WhatsApp numbers."
#     )
#     active_buttons = models.JSONField(default=dict, blank=True)

#     # ==========================================
#     # 6. PROPERTY SPECIAL FEATURES CASE
#     # ==========================================
#     special_features = models.JSONField(
#         default=dict, 
#         blank=True, 
#         help_text="Category-specific specs: hostel gender, transformer KVA, power phase, generator, etc."
#     )
#     amenities = models.JSONField(
#         default=list, 
#         blank=True, 
#         help_text="List of tag strings: ['lift', 'swimming_pool', '24h_security', 'gym']"
#     )

#     # ==========================================
#     # 7. FIXED AND NON-EDITABLE DATA CASE
#     # ==========================================
#     status = models.CharField(
#         max_length=15, 
#         choices=StatusChoices.choices, 
#         default=StatusChoices.ACTIVE, 
#         db_index=True
#     )
#     is_boosted = models.BooleanField(default=False, db_index=True)
#     is_premium = models.BooleanField(default=False, db_index=True)
    
#     created_at = models.DateTimeField(auto_now_add=True, db_index=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     expiry_date = models.DateTimeField(db_index=True, blank=True)

#     class Meta:
#         indexes = [
#             # Main UI Search Filters
#             models.Index(fields=['township', 'offer_type', 'property_type', 'status'], name='idx_listing_main_search'),
            
#             # Feed Ranking Index
#             models.Index(fields=['is_boosted', '-created_at'], name='idx_listing_feed_sort'),
            
#             # Common Multi-field Filters
#             models.Index(fields=['price', 'building_area'], name='idx_listing_price_area'),
#             models.Index(fields=['bedrooms', 'floor_level'], name='idx_listing_rooms_floor'),

#             # GIN Indexes for Deep JSON Searches
#             GinIndex(fields=['landmarks'], name='idx_landmarks_gin'),
#             GinIndex(fields=['amenities'], name='idx_amenities_gin'),
#             GinIndex(fields=['special_features'], name='idx_special_features_gin'),
#             GinIndex(fields=['interior_specs'], name='idx_interior_specs_gin'),
#             GinIndex(fields=['exterior_specs'], name='idx_exterior_specs_gin'),
#         ]

#     def save(self, *args, **kwargs):
#         # 1. Compute total building area automatically if dimensions are provided
#         if self.width and self.length and not self.building_area:
#             self.building_area = self.width * self.length

#         # 2. Premium items get boosted visibility
#         if self.is_premium:
#             self.is_boosted = True

#         # 3. Set standard 90-day post lifespan
#         if not self.id and not self.expiry_date:
#             self.expiry_date = timezone.now() + timedelta(days=90)

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.title} ({self.get_property_type_display()})"


# class ListingImage(models.Model):
#     listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
#     image_url = models.URLField(max_length=500)
#     thumbnail_url = models.URLField(max_length=500, blank=True, null=True)
#     is_primary = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-is_primary', 'created_at']

from django.db import models


class Listing(models.Model):

    class OfferChoices(models.IntegerChoices):
        SALE = 1, 'For Sale'
        RENT = 2, 'For Rent'
        BUY = 3, 'Want to Buy'
        TENANT = 4, 'Want to Rent'

    class CategoryChoices(models.IntegerChoices):
        HOUSE = 1, 'House'
        CONDO = 2, 'Condo'
        APARTMENT = 3, 'Apartment'
        SHOP = 4, 'Shop'
        OFFICE = 5, 'Office'
        HOSTEL = 6, 'Hostel'
        INDUSTRIAL = 7, 'Industrial Zone'
        WAREHOUSE = 8, 'Warehouse'
        LAND = 9, 'Plot of Land'
        OTHER = 99, 'Other'

    # ==========================================
    # SECTOR 1: OFFER CASE
    # ==========================================
    offer_type = models.PositiveSmallIntegerField(
        choices=OfferChoices.choices, db_index=True,
        help_text="1: Sale, 2: Rent, 3: Buy, 4: Tenant"
    )
    
    property_type = models.PositiveSmallIntegerField(
        choices=CategoryChoices.choices, db_index=True,
        help_text="1: House, 2: Condo, 3: Apt, 4: Shop, 5: Office, 6: Hostel, 7: Industrial, 8: Warehouse, 9: Land, 99: Other"
    )

    sub_property_type = models.CharField(
        max_length=100, blank=True, db_index=True
    )

    title = models.CharField(max_length=150)
    price = models.PositiveBigIntegerField(db_index=True)

    # ==========================================
    # SECTOR 2: LOCATION CASE
    # ==========================================
    region = models.ForeignKey(
        Region, 
        on_delete=models.PROTECT, 
        related_name='listings',
        db_index=True,
        help_text="Mapped region ID translated on client side"
    )
    
    township = models.ForeignKey(
        Township, 
        on_delete=models.PROTECT, 
        related_name='listings',
        db_index=True,
        help_text="Mapped township ID translated on client side"
    )
    
    # Specific street / ward details (free text input)
    quarter = models.CharField(max_length=100, blank=True)
    road = models.CharField(max_length=100, blank=True)
    
    # Combined Lat & Long pair: {"lat": 16.8661, "lng": 96.1951}
    coordinates = models.JSONField(default=dict, blank=True)
    
    # Array of strings for nearby landmarks: ["Junction City", "Inya Lake"]
    landmarks = models.JSONField(default=list, blank=True)

    class Meta:
        indexes = [
            # Main location filtering index
            models.Index(fields=['township', 'region'], name='idx_listing_location'),
            # GIN Index for fast array lookups on landmarks
            GinIndex(fields=['landmarks'], name='idx_landmarks_gin'),
        ]

    # ==========================================
    # SECTOR 3: LAND CASE
    # ==========================================
    class LandTypeChoices(models.IntegerChoices):
        GRANT = 1, 'Grant Land'             # ဂရန်မြေ
        FREEHOLD = 2, 'Ancestral/Freehold'  # ဘိုးဘွားပိုင်မြေ
        PERMIT = 3, 'Permit Land'           # ပါမစ်မြေ
        LICENSE = 4, 'License Land'         # လိုင်စင်မြေ
        SLIP = 5, 'Slip Land'               # စလစ်မြေ
        GRANT_APPLIED = 6, 'Grant Applied'  # ဂရန်လျှောက်ထားဆဲ
        VILLAGE = 7, 'Village Land'         # ရွာမြေ
        OTHER = 99, 'Other'                 # အခြား

    # --- Essential Land SQL Columns ---
    land_type = models.PositiveSmallIntegerField(
        choices=LandTypeChoices.choices, null=True, blank=True, db_index=True,
        help_text="1: Grant, 2: Freehold, 3: Permit, 4: License, 5: Slip, 6: Grant Applied, 7: Village, 99: Other"
    )

    # Land Plot Dimensions (in feet)
    land_width = models.PositiveSmallIntegerField(null=True, blank=True)
    land_length = models.PositiveSmallIntegerField(null=True, blank=True)

    # Total Plot Area in Sq Ft for fast B-Tree range queries
    land_area = models.PositiveIntegerField(
        null=True, blank=True, db_index=True,
    )

    # --- JSONB Bucket (Extra/Niche Land Attributes) ---
    # Example: {"shape": "rectangular", "corner_plot": true, "road_width_ft": 20, "has_garden": true}
    land_features = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [
            GinIndex(fields=['land_features'], name='idx_land_features_gin'),
        ]
    
    # ==========================================
    # SECTOR 4: BUILDING CASE
    # ==========================================
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
        UNFURNISHED = 1, 'Unfurnished'                 # မပြင်ဆင်ရသေး
        SEMI_FURNISHED = 2, 'Semi-Furnished'           # အသင့်အတင့် ပြင်ဆင်ပြီး
        FULLY_FURNISHED = 3, 'Fully Furnished'         # အပြည့်အဝ ပြင်ဆင်ပြီး
        HALL = 4, 'Hall / Bare Shell'                  # ဟောခန်း
        UNDER_CONSTRUCTION = 5, 'Under Construction'   # ဆောက်လုပ်ဆဲ

    # --- Enums (Using help_text for documentation) ---
    facing_direction = models.PositiveSmallIntegerField(
        choices=FacingChoices.choices, null=True, blank=True, db_index=True,
        help_text="Facing direction: 1=N, 2=S, 3=E, 4=W, 5=NE, 6=NW, 7=SE, 8=SW"
    )
    furnishing = models.PositiveSmallIntegerField(
        choices=FurnishingChoices.choices, null=True, blank=True, db_index=True,
        help_text="Completion status: 1=Unfurnished, 2=Semi, 3=Full, 4=Hall, 5=Under Construction"
    )

    # --- Building Dimensions & Heights ---
    building_width = models.PositiveSmallIntegerField(null=True, blank=True)
    building_length = models.PositiveSmallIntegerField(null=True, blank=True)
    building_height = models.PositiveSmallIntegerField(null=True, blank=True)
    building_area = models.PositiveIntegerField(null=True, blank=True, db_index=True)

    # --- Vertical & Floor Data ---
    total_floors = models.PositiveSmallIntegerField(
        default=1, null=True, blank=True,
        help_text="Total story count of the building structure"
    )
    floor_level = models.PositiveSmallIntegerField(
        null=True, blank=True, db_index=True,
        help_text="Specific unit level (0: Ground floor, 1: 1st floor, etc.)"
    )

    # --- Dynamic Room Structure (JSONB) ---
    # Example payload:
    # {
    #   "master_bedroom": 2,
    #   "single_bedroom": 3,
    #   "bathroom": 2,
    #   "living_room": 1,
    #   "kitchen": 1,
    #   "shrine_room": 1,
    #   "dining_room": 1
    # }
    room_structure = models.JSONField(default=dict, blank=True)

    # --- Industrial, Utility & Special Building Features (JSONB) ---
    # Example payload:
    # {
    #   "construction_type": 1,     // 1: Steel Structure, 2: RC, 3: Brick
    #   "has_lift": true,
    #   "has_generator": true,
    #   "has_3phase_power": true,   // Critical for industrial sites
    #   "transformer_kva": 315,
    #   "floor_load_capacity": 500, // kg/sqm
    #   "water_supply": "tube_well"
    # }
    building_features = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [
            GinIndex(fields=['room_structure'], name='idx_room_structure_gin'),
            GinIndex(fields=['building_features'], name='idx_bldg_features_gin'),
        ]



##########################################################

class Region(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)  # e.g., 1: Yangon, 2: Mandalay
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Township(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)  # e.g., 101: Kamayut, 102: Sanchaung
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='townships')
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.region.name})"