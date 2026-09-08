"""Offer case"""
offerchoices - Essential, column, emun and integer choices, no need to mention extra, search info
property_type - Essential, column, emun and integer choices, no need to mention extra, search info
sub_property_type - essential, column, maybe free text field, maybe hybrid fix integer choice + user 
    input data, probably search info, need to handle it with extra care
title - essential, column, free text field, no need to mention extra
price - essential, column, and index
"""Location case"""
region - Essential, column, emun and integer choices and ForeignKey, no need to mention extra, search info
township - Essential, column, emun and integer choices and ForeignKey, no need to mention extra, search info
quarter - essential, column, free text field, no need to mention extra, and most likely display data
road - essential, column, free text field, no need to mention extra, and most likely display data
lat + long - haven't deceded to use postgis, but be able to pin the property on map with coord is a good thing
    probably not search data, but usable, column or bucket?, better be column, but if we need to reduce -> then
    it will be a thing to reduce to bucket and Combine two data
landmarks - just need to put some data, important? -> yes as display info, valuable info for user, but not for
    server. bucket for flexiblity and multiple data.
"""Land case"""
land_type - a good display info, probably a good search info too, but decide not to index, but be able to search
land_width - essential, column, no need to mention extra, probably not search info but valuable info
land_length - same as above
land_area - essential, column, probably search info, no need to mention extra. both display info and search info
land_features - good json, can store many specific land info, like parking, pool, ya so many
"""Building case"""
facing_choice - i think its just a good display data, i dont think people would search through facing of a 
    building, just my thoughts, maybe into a bucket?
furnishing - also a display data as above i thought.
building_width - essential, column, no need to mention extra, probably not search info but valuable info
building_length - same as above
building_area - essential, column, probably search info, no need to mention extra. both display info and search info
building_height - just a property specific data for likely industrial and warehouse. maybe better in bucket
floor - for landed houses, some offices, and shop, ya probably a good column candidate and also a potential 
    bucket
floor_level - for condo and apartment, a valuable display data, maybe even a search a info, probably not indexed 
    for now
bedrooms - number of bedrooms is a valuable display info, potential good info to be indexed. but maybe not
room_structure - good json field for flexiblity and multiple, essential
building_features - maybe some of the above json buckets come into this, for extra information, and display info
    would come into this. good for amenities.
year_built - a good data, column
"""Property Special Features"""
property_special_features - only one in this sector, maybe we can even remove and put the specific info into
    other sector json fields. not sure yet.
"""Basic info, sales info and contract case"""
operational_status - a good information for user to show and see. but also can be put into buckets, not 
    necessarily a column thing
is_owner_direct - a good information for boolean column, but i think index is not necessary
featured_image - url field for main image necessary for N1 case.
sales_info - good display data. and bucket for many things. is_bank_loan_available, is_nego? ya so many data 
    but less important than is_owner_direct case. things like that.
rental_info - after a thought, i think we should split into sales info and rental info.
contact_info - necessary data. and bucket, count number of active buttons displayed and calculate the cost of
    cost.
status - ya, necessary for cases active, pending, finished, deleted -> essential for a post to be alive or 
    dead.
PricePeriod or least contract term - ya, a good info for renting
available_from - a good bucket data, probably into some JSONField
deposit_amount - a good bucket data, probably into some JSONField
"""system admin case"""
landlord - ForeignKey auto connected
created_at - good data and also necessary for db and maybe even auto in db
updated_at - a good data but not so much
expires_at - ya, we need to calculate this and change the status from the sector above automatically with
    celery. also necessary Data
post_cost - the thing is monetization of the app -> base cost + plut number of buttons display for contact
    must be calculated
is_boosted - monetization data, necessary


class Listing(models.Model):

    class OfferChoices(models.IntegerChoices):
        SALE = 1, 'For Sale'
        RENT = 2, 'For Rent'

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

    sub_property_type = models.CharField(max_length=100, blank=True, db_index=True)
    title = models.CharField(max_length=150)
    price = models.PositiveBigIntegerField(db_index=True)

    # ==========================================
    # SECTOR 2: LOCATION CASE
    # ==========================================
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name='listings', db_index=True)
    township = models.ForeignKey(Township, on_delete=models.PROTECT, related_name='listings', db_index=True)
    quarter = models.CharField(max_length=100, blank=True)
    road = models.CharField(max_length=100, blank=True)
    # Combined Lat & Long pair: {"lat": 16.8661, "lng": 96.1951}
    coordinates = models.JSONField(default=dict, blank=True)
    # Array of strings for nearby landmarks: ["Junction City", "Inya Lake"]
    landmarks = models.JSONField(default=list, blank=True)

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
    land_area = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    # Example: {"shape": "rectangular", "corner_plot": true, "road_width_ft": 20, "has_garden": true}
    land_features = models.JSONField(default=dict, blank=True)

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

    # ==========================================
    # SECTOR 5: PROPERTY SPECIAL FEATURES CASE
    # ==========================================
    # Yes, we still don't know what to put exactly. I am gonna leave just one JSON field for now.
    property_special_features = models.JSONField(default=dict, blank=True)

    # ==========================================
    # SECTOR 6: BASIC INFO, SALES INFO, CONTACT CASE
    # ==========================================
    class OperationalChoices(models.IntegerChoices):
        VACANT = 1, 'Vacant'                       # လွတ်
        OPERATING = 2, 'Operating / Running'      # ဖွင့်လှစ်ထားဆဲ
        HIATUS = 3, 'Hiatus / Temporary Closed'   # ခေတ္တရပ်နား
        UNDER_RENOVATION = 4, 'Under Renovation'   # ပြင်ဆင်ဆဲ

    # --- Direct SQL Columns (High-Frequency Search Filters) ---
    is_owner_direct = models.BooleanField(default=False, db_index=True, null=True, blank=True)
    operational_status = models.PositiveSmallIntegerField(
        choices=OperationalChoices.choices, default=OperationalChoices.VACANT, db_index=True,
        help_text="1: Vacant, 2: Operating, 3: Hiatus, 4: Under Renovation"
    )
    featured_image = models.URLField(max_length=500)

    # --- Sales & Financial Terms (Display JSONB) ---
    # Example payload:
    # {
    #   "min_lease_months": 6,
    #   "advance_months": 6,
    #   "deposit_amount": 500000,
    #   "maintenance_fee_monthly": 30000,
    #   "accepted_banks": ["KBZ", "AYA", "CB"],
    #   "tax_responsibility": "split_50_50"
    # }
    sales_info = models.JSONField(
        default=dict, blank=True,
        help_text="Granular lease terms, advance/deposit, bank options, tax split details"
    )

    # --- Status & Operational Lifecycle (Display/Admin JSONB) ---
    # Example payload:
    # {
    #   "marketplace_status": "active", // "draft", "active", "pending", "sold", "rented", "archived"
    #   "available_from_date": "2026-10-01",
    #   "viewing_notice": "1_day_ahead",
    #   "rejection_reason": null
    # }
    status_info = models.JSONField(default=dict, blank=True)

    # --- Contact Channels & Socials (Display JSONB) ---
    # Example payload:
    # {
    #   "contact_person": "U Ba",
    #   "contact_role": "direct_owner",
    #   "primary_phone": "09123456789",
    #   "additional_phones": ["09987654321"],
    #   "social_links": {
    #     "viber": "09123456789",
    #     "telegram": "https://t.me/agent_username",
    #     "facebook_messenger": "https://m.me/page_name"
    #   }
    # }
    contact_info = models.JSONField(default=dict, blank=True)

    # ==========================================
    # SECTOR 7: SYSTEM & ADMIN META CASE (FIXED DATA)
    # ==========================================

    landlord = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField(default=default_expiry_date, db_index=True,)
    post_cost = models.PositiveIntegerField(default=0)
    is_boosted = models.BooleanField(default=False, db_index=True)

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

"""New One"""

from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone

def default_expiry_date():
    return timezone.now() + timedelta(days=30)

class Region(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Township(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="townships")
    name = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["region", "name"], name="uq_township_region_name"),
        ]

    def __str__(self):
        return f"{self.name} ({self.region.name})"

class Listing(models.Model):

    # ============================================================
    # ENUMS
    # ============================================================

    class OfferChoices(models.IntegerChoices):
        SALE = 1, "For Sale"
        RENT = 2, "For Rent"

    class CategoryChoices(models.IntegerChoices):
        HOUSE = 1, "House"
        CONDO = 2, "Condo"
        APARTMENT = 3, "Apartment"
        SHOP = 4, "Shop"
        OFFICE = 5, "Office"
        HOSTEL = 6, "Hostel"
        INDUSTRIAL = 7, "Industrial Zone"
        WAREHOUSE = 8, "Warehouse"
        LAND = 9, "Plot of Land"
        OTHER = 99, "Other"

    class PropertySubtypeChoices(models.IntegerChoices):
        # General / residential
        DETACHED_HOUSE = 1, "Detached House"
        SEMI_DETACHED_HOUSE = 2, "Semi-Detached House"
        BUNGALOW = 3, "Bungalow"

        # Apartment / condo
        STUDIO = 10, "Studio"
        DUPLEX = 11, "Duplex"
        PENTHOUSE = 12, "Penthouse"

        # Shop
        RETAIL = 20, "Retail"
        RESTAURANT = 21, "Restaurant"
        SHOWROOM = 22, "Showroom"

        # Office
        SERVICED_OFFICE = 30, "Serviced Office"
        STANDARD_OFFICE = 31, "Standard Office"

        # Hostel
        MALE_HOSTEL = 40, "Male Hostel"
        FEMALE_HOSTEL = 41, "Female Hostel"
        MIXED_HOSTEL = 42, "Mixed Hostel"

        # Industrial / warehouse
        FACTORY = 50, "Factory"
        WORKSHOP = 51, "Workshop"
        STORAGE_WAREHOUSE = 52, "Storage Warehouse"

        OTHER = 99, "Other"

    class LandTypeChoices(models.IntegerChoices):
        GRANT = 1, "Grant Land"
        FREEHOLD = 2, "Ancestral / Freehold"
        PERMIT = 3, "Permit Land"
        LICENSE = 4, "License Land"
        SLIP = 5, "Slip Land"
        GRANT_APPLIED = 6, "Grant Applied"
        VILLAGE = 7, "Village Land"
        OTHER = 99, "Other"

    class FacingChoices(models.IntegerChoices):
        NORTH = 1, "North"
        SOUTH = 2, "South"
        EAST = 3, "East"
        WEST = 4, "West"
        NORTH_EAST = 5, "North-East"
        NORTH_WEST = 6, "North-West"
        SOUTH_EAST = 7, "South-East"
        SOUTH_WEST = 8, "South-West"

    class FurnishingChoices(models.IntegerChoices):
        UNFURNISHED = 1, "Unfurnished"
        SEMI_FURNISHED = 2, "Semi-Furnished"
        FULLY_FURNISHED = 3, "Fully Furnished"
        HALL = 4, "Hall / Bare Shell"
        UNDER_CONSTRUCTION = 5, "Under Construction"

    class OperationalChoices(models.IntegerChoices):
        VACANT = 1, "Vacant"
        OPERATING = 2, "Operating / Running"
        HIATUS = 3, "Hiatus / Temporarily Closed"
        UNDER_RENOVATION = 4, "Under Renovation"

    class ListingStatusChoices(models.IntegerChoices):
        ACTIVE = 1, "Active"
        PENDING = 2, "Pending"
        SOLD_OR_RENTED = 3, "Sold / Rented"
        ARCHIVED = 4, "Archived"

    # ============================================================
    # SECTOR 1: OFFER CASE
    # ============================================================

    offer_type = models.PositiveSmallIntegerField(choices=OfferChoices.choices)
    property_type = models.PositiveSmallIntegerField(choices=CategoryChoices.choices)

    # Controlled subtype.
    property_subtype = models.PositiveSmallIntegerField(choices=PropertySubtypeChoices.choices, null=True, blank=True)

    # User-created subtype when the controlled vocabulary does not contain the required option.
    property_subtype_custom = models.CharField(max_length=100, blank=True)

    title = models.CharField(max_length=150)
    price = models.PositiveBigIntegerField(db_index=True)

    # ============================================================
    # SECTOR 2: LOCATION CASE
    # ============================================================

    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="listings")
    township = models.ForeignKey(Township, on_delete=models.PROTECT, related_name="listings")
    quarter = models.CharField(max_length=100, blank=True)
    road = models.CharField(max_length=100, blank=True)
    coordinates = models.JSONField(default=dict, blank=True)
    # Example:
    # [
    #     "Junction City",
    #     "Inya Lake",
    #     "Yangon University"
    # ]
    landmarks = models.JSONField(default=list, blank=True)

    # ============================================================
    # SECTOR 3: LAND CASE
    # ============================================================

    land_type = models.PositiveSmallIntegerField(choices=LandTypeChoices.choices, null=True, blank=True)
    land_width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    land_length = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    land_area = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    # Property-specific land information.
    #
    # Examples:
    # {
    #     "shape": "rectangular",
    #     "corner_plot": true,
    #     "road_width_ft": 40,
    #     "parking": true,
    #     "pool": false
    # }
    land_features = models.JSONField(default=dict, blank=True)

    # ============================================================
    # SECTOR 4: BUILDING CASE
    # ============================================================

    facing_direction = models.PositiveSmallIntegerField(choices=FacingChoices.choices, null=True, blank=True)
    furnishing = models.PositiveSmallIntegerField(choices=FurnishingChoices.choices, null=True, blank=True)
    building_width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    building_length = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    building_area = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    # Only applies where meaningful.
    # Specialized values such as industrial clear height
    # can live inside building_features.
    building_height = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Number of floors in the whole building.
    total_floors = models.PositiveSmallIntegerField(null=True, blank=True)

    # The specific floor occupied by this property.
    # Mainly relevant to apartment / condo / office / shop.
    floor_level = models.PositiveSmallIntegerField(null=True, blank=True)

    bedrooms = models.PositiveSmallIntegerField(null=True, blank=True)
    year_built = models.PositiveSmallIntegerField(null=True, blank=True)

    # Detailed room composition.
    #
    # Example:
    # {
    #     "master_bedroom": 2,
    #     "single_bedroom": 1,
    #     "living_room": 1,
    #     "dining_room": 1,
    #     "kitchen": 1,
    #     "maid_room": 1
    # }
    room_structure = models.JSONField(default=dict, blank=True)

    # General building information / amenities.
    #
    # Examples:
    # {
    #     "has_lift": true,
    #     "has_generator": true,
    #     "has_water_tank": true,
    #     "has_solar": false,
    #     "clear_height_ft": 20,
    #     "power_capacity_kva": 100
    # }
    building_features = models.JSONField(default=dict, blank=True)

    # ============================================================
    # SECTOR 5: PROPERTY SPECIAL FEATURES
    # ============================================================

    # Reserved for information that belongs specifically
    # to a particular property type and does not fit naturally
    # into the general land/building/rental/sales buckets.
    #
    # Example:
    # {
    #     "allowed_businesses": ["restaurant", "retail"],
    #     "grease_trap": true
    # }
    #
    # This field can be removed later if we determine that
    # all type-specific information fits better elsewhere.
    property_special_features = models.JSONField(default=dict, blank=True)

    # ============================================================
    # SECTOR 6: BASIC / SALES / RENTAL / CONTRACT / CONTACT
    # ============================================================

    operational_status = models.PositiveSmallIntegerField(choices=OperationalChoices.choices, default=OperationalChoices.VACANT)
    is_owner_direct = models.BooleanField(default=False)

    # Direct URL used by feed/list views.
    featured_image = models.URLField(max_length=500)

    # ----------------------------
    # SALES INFORMATION
    # ----------------------------

    sales_info = models.JSONField(default=dict, blank=True)

    # Examples:
    # {
    #     "is_negotiable": true,
    #     "is_bank_loan_available": true,
    #     "ownership_transfer_fee": 100000,
    #     "payment_terms": "..."
    # }

    # ----------------------------
    # RENTAL INFORMATION
    # ----------------------------

    rental_info = models.JSONField(default=dict, blank=True)

    # Examples:
    # {
    #     "price_period": "monthly",
    #     "minimum_lease_months": 6,
    #     "available_from": "2026-10-01",
    #     "deposit_amount": 500000,
    #     "advance_months": 2,
    #     "maintenance_fee_monthly": 50000
    # }

    # ----------------------------
    # CONTACT INFORMATION
    # ----------------------------

    contact_info = models.JSONField(default=dict, blank=True)

    # Example:
    # {
    #     "phone": "...",
    #     "secondary_phone": "...",
    #     "viber": "...",
    #     "telegram": "...",
    #     "messenger": "..."
    # }

    status = models.PositiveSmallIntegerField(choices=ListingStatusChoices.choices, default=ListingStatusChoices.ACTIVE)

    # ============================================================
    # SECTOR 7: SYSTEM / ADMIN META
    # ============================================================

    landlord = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(default=default_expiry_date)

    # Final calculated amount associated with posting.
    #
    # Actual calculation should happen server-side before
    # the listing is accepted as an active post.
    post_cost = models.PositiveIntegerField(default=0)
    is_boosted = models.BooleanField(default=False)

    # ============================================================
    # MODEL META
    # ============================================================

    class Meta:
        ordering = ["-is_boosted", "-created_at"]

    def __str__(self):
        return f"[{self.id}] {self.title} - {self.price}"

# =================================
# UNCOMMENTED ONE / NO DESCRIPTION
# =================================
from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone


def default_expiry_date():
    return timezone.now() + timedelta(days=30)


class Region(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Township(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="townships")
    name = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["region", "name"], name="uq_township_region_name"),
        ]

    def __str__(self):
        return f"{self.name} ({self.region.name})"


class Listing(models.Model):

    # ============================================================
    # ENUMS
    # ============================================================

    class OfferChoices(models.IntegerChoices):
        SALE = 1, "For Sale"
        RENT = 2, "For Rent"

    class CategoryChoices(models.IntegerChoices):
        HOUSE = 1, "House"
        CONDO = 2, "Condo"
        APARTMENT = 3, "Apartment"
        SHOP = 4, "Shop"
        OFFICE = 5, "Office"
        HOSTEL = 6, "Hostel"
        INDUSTRIAL = 7, "Industrial Zone"
        WAREHOUSE = 8, "Warehouse"
        LAND = 9, "Plot of Land"
        OTHER = 99, "Other"

class PropertySubtypeChoices(models.IntegerChoices):

    DETACHED_HOUSE = 101, "Detached House"
    SEMI_DETACHED_HOUSE = 102, "Semi-Detached House"
    TERRACED_HOUSE = 103, "Terraced House"
    TOWNHOUSE = 104, "Townhouse"
    BUNGALOW = 105, "Bungalow"
    VILLA = 106, "Villa"

    STUDIO = 201, "Studio"
    STANDARD_UNIT = 202, "Standard Unit"
    DUPLEX = 203, "Duplex"
    PENTHOUSE = 204, "Penthouse"

    STANDARD_APARTMENT = 301, "Standard Apartment"
    STUDIO_APARTMENT = 302, "Studio Apartment"
    DUPLEX_APARTMENT = 303, "Duplex Apartment"
    PENTHOUSE_APARTMENT = 304, "Penthouse Apartment"
    SERVICED_APARTMENT = 305, "Serviced Apartment"
    MINI_APARTMENT = 306, "Mini Apartment"

    RETAIL_SHOP = 401, "Retail Shop"
    SHOWROOM = 402, "Showroom"
    RESTAURANT = 403, "Restaurant"
    CAFE = 404, "Cafe"
    STREET_SHOP = 405, "Street Shop"
    SHOP_HOUSE = 406, "Shop House"

    STANDARD_OFFICE = 501, "Standard Office"
    SERVICED_OFFICE = 502, "Serviced Office"
    OFFICE_FLOOR = 503, "Office Floor"
    OFFICE_BUILDING = 504, "Office Building"

    MALE_HOSTEL = 601, "Male Hostel"
    FEMALE_HOSTEL = 602, "Female Hostel"
    MIXED_HOSTEL = 603, "Mixed Hostel"
    STUDENT_HOSTEL = 604, "Student Hostel"
    WORKER_HOSTEL = 605, "Worker Hostel"

    FACTORY = 701, "Factory"
    WORKSHOP = 702, "Workshop"
    INDUSTRIAL_BUILDING = 703, "Industrial Building"
    INDUSTRIAL_COMPOUND = 704, "Industrial Compound"
    MANUFACTURING_FACILITY = 705, "Manufacturing Facility"

    STORAGE_WAREHOUSE = 801, "Storage Warehouse"
    DISTRIBUTION_WAREHOUSE = 802, "Distribution Warehouse"
    COLD_STORAGE = 803, "Cold Storage"
    LOGISTICS_WAREHOUSE = 804, "Logistics Warehouse"

    RESIDENTIAL_LAND = 901, "Residential Land"
    COMMERCIAL_LAND = 902, "Commercial Land"
    INDUSTRIAL_LAND = 903, "Industrial Land"
    AGRICULTURAL_LAND = 904, "Agricultural Land"
    MIXED_USE_LAND = 905, "Mixed-Use Land"

    OTHER = 999, "Other"

    class LandTypeChoices(models.IntegerChoices):
        GRANT = 1, "Grant Land"
        FREEHOLD = 2, "Ancestral / Freehold"
        PERMIT = 3, "Permit Land"
        LICENSE = 4, "License Land"
        SLIP = 5, "Slip Land"
        GRANT_APPLIED = 6, "Grant Applied"
        VILLAGE = 7, "Village Land"
        OTHER = 99, "Other"

    class FacingChoices(models.IntegerChoices):
        NORTH = 1, "North"
        SOUTH = 2, "South"
        EAST = 3, "East"
        WEST = 4, "West"
        NORTH_EAST = 5, "North-East"
        NORTH_WEST = 6, "North-West"
        SOUTH_EAST = 7, "South-East"
        SOUTH_WEST = 8, "South-West"

    class FurnishingChoices(models.IntegerChoices):
        UNFURNISHED = 1, "Unfurnished"
        SEMI_FURNISHED = 2, "Semi-Furnished"
        FULLY_FURNISHED = 3, "Fully Furnished"
        HALL = 4, "Hall / Bare Shell"
        UNDER_CONSTRUCTION = 5, "Under Construction"

    class PricePeriodChoices(models.IntegerChoices):
        MONTH = 1, "Per Month"
        YEAR = 2, "Per Year"
        WEEK = 3, "Per Week"
        DAY = 4, "Per Day"

    class OperationalChoices(models.IntegerChoices):
        VACANT = 1, "Vacant"
        OPERATING = 2, "Operating / Running"
        HIATUS = 3, "Hiatus / Temporarily Closed"
        UNDER_RENOVATION = 4, "Under Renovation"

    class ListingStatusChoices(models.IntegerChoices):
        ACTIVE = 1, "Active"
        PENDING = 2, "Pending"
        SOLD_OR_RENTED = 3, "Sold / Rented"
        ARCHIVED = 4, "Archived"

    # ============================================================
    # SECTOR 1: OFFER CASE
    # ============================================================

    offer_type = models.PositiveSmallIntegerField(choices=OfferChoices.choices, db_index=True)
    property_type = models.PositiveSmallIntegerField(choices=CategoryChoices.choices, db_index=True)
    property_subtype = models.PositiveSmallIntegerField(choices=PropertySubtypeChoices.choices, null=True, blank=True)
    property_subtype_custom = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=150)
    price = models.PositiveBigIntegerField(db_index=True)

    # ============================================================
    # SECTOR 2: LOCATION CASE
    # ============================================================

    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="listings", db_index=True)
    township = models.ForeignKey(Township, on_delete=models.PROTECT, related_name="listings", db_index=True)
    quarter = models.CharField(max_length=100, blank=True)
    road = models.CharField(max_length=100, blank=True)
    coordinates = models.JSONField(default=dict, blank=True)
    landmarks = models.JSONField(default=list, blank=True)

    # ============================================================
    # SECTOR 3: LAND CASE
    # ============================================================

    land_type = models.PositiveSmallIntegerField(choices=LandTypeChoices.choices, null=True, blank=True)
    land_width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_index=True)
    land_length = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_index=True)
    land_area = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    land_features = models.JSONField(default=dict, blank=True)

    # ============================================================
    # SECTOR 4: BUILDING CASE
    # ============================================================

    facing_direction = models.PositiveSmallIntegerField(choices=FacingChoices.choices, null=True, blank=True)
    furnishing = models.PositiveSmallIntegerField(choices=FurnishingChoices.choices, null=True, blank=True, db_index=True)
    building_width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_index=True)
    building_length = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_index=True)
    building_area = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_floors = models.PositiveSmallIntegerField(null=True, blank=True, db_index=True)
    floor_level = models.PositiveSmallIntegerField(null=True, blank=True, db_index=True)
    bedrooms = models.PositiveSmallIntegerField(null=True, blank=True, db_index=True)
    year_built = models.PositiveSmallIntegerField(null=True, blank=True)
    room_structure = models.JSONField(default=dict, blank=True)
    building_features = models.JSONField(default=dict, blank=True)

    # ============================================================
    # SECTOR 5: PROPERTY SPECIAL FEATURES
    # ============================================================

    property_special_features = models.JSONField(default=dict, blank=True)

    # ============================================================
    # SECTOR 6: BASIC / SALES / RENTAL / CONTRACT / CONTACT
    # ============================================================

    operational_status = models.PositiveSmallIntegerField(choices=OperationalChoices.choices, default=OperationalChoices.VACANT)
    is_owner_direct = models.BooleanField(default=False, db_index=True)
    featured_image = models.URLField(max_length=500)
    sales_info = models.JSONField(default=dict, blank=True)
    rental_info = models.JSONField(default=dict, blank=True)
    contact_info = models.JSONField(default=dict, blank=True)
    price_period = models.PositiveSmallIntegerField(choices=PricePeriodChoices.choices, null=True, blank=True, db_index=True)
    
    # ============================================================
    # SECTOR 7: SYSTEM / ADMIN META
    # ============================================================

    landlord = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(default=default_expiry_date)
    post_cost = models.PositiveIntegerField(default=0)
    is_boosted = models.BooleanField(default=False)
    status = models.PositiveSmallIntegerField(choices=ListingStatusChoices.choices, default=ListingStatusChoices.ACTIVE, db_index=True)

    # ============================================================
    # MODEL META
    # ============================================================

    class Meta:
    ordering = ["-is_boosted", "-created_at"]

    indexes = [
        models.Index(
            fields=["status", "-created_at"],
            name="idx_listing_status_created",
        ),
        models.Index(
            fields=["township", "property_type", "-created_at"],
            name="idx_listing_township_type_created",
        ),
        models.Index(
            fields=["offer_type", "property_type", "-created_at"],
            name="idx_listing_offer_type_created",
        ),
        models.Index(
            fields=["is_boosted", "-created_at"],
            name="idx_listing_boosted_created",
        ),
        models.Index(
            fields=["expires_at", "status"],
            name="idx_listing_expiry_status",
        ),
        models.GinIndex(
            fields=["building_features"],
            name="idx_listing_building_features_gin",
        ),
        models.GinIndex(
            fields=["sales_info"],
            name="idx_listing_sales_info_gin",
        ),
        models.GinIndex(
            fields=["rental_info"],
            name="idx_listing_rental_info_gin",
        ),
    ]

    def __str__(self):
        return f"[{self.id}] {self.title} - {self.price}"