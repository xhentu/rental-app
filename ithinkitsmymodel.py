# =================================
# UNCOMMENTED ONE / NO DESCRIPTION
# =================================
from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.postgres.indexes import GinIndex

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
        FAMILY_HOSTEL = 606, "Family Hostel"

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
            GinIndex(
                fields=["building_features"],
                name="idx_listing_building_features_gin",
            ),
            GinIndex(
                fields=["sales_info"],
                name="idx_listing_sales_info_gin",
            ),
            GinIndex(
                fields=["rental_info"],
                name="idx_listing_rental_info_gin",
            ),
        ]

    def __str__(self):
        return f"[{self.id}] {self.title} - {self.price}"

class ListingImage(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image_url = models.URLField(max_length=500)
    thumbnail_url = models.URLField(max_length=500, blank=True)

    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_primary", "sort_order", "created_at"]

        indexes = [
            models.Index(
                fields=["listing", "sort_order"],
                name="idx_listing_image_order",
            ),
        ]

    def __str__(self):
        return f"Image for Listing {self.listing_id}"

class ServiceAdvertisement(models.Model):

    class ServiceCategoryChoices(models.TextChoices):
        TRANSPORT = "transport", "Transportation"
        MOVING = "moving", "Moving Service"
        DECORATION = "decoration", "Decoration"
        ELECTRICAL = "electrical", "Electrical Service"
        PLUMBING = "plumbing", "Plumbing & Water"
        WATER = "water", "Water Service"
        LAUNDRY = "laundry", "Laundry Service"
        CLEANING = "cleaning", "Cleaning Service"
        CONSTRUCTION = "construction", "Construction"
        RENOVATION = "renovation", "Renovation"
        REPAIR = "repair", "Repair & Maintenance"
        SECURITY = "security", "Security Service"
        PROPERTY_MANAGEMENT = "property_management", "Property Management"
        MOVING_STORAGE = "moving_storage", "Moving & Storage"
        PEST_CONTROL = "pest_control", "Pest Control"
        INTERNET = "internet", "Internet / Network Service"
        OTHER = "other", "Other"

    class StatusChoices(models.IntegerChoices):
        PENDING = 1, "Pending"
        ACTIVE = 2, "Active"
        EXPIRED = 3, "Expired"
        ARCHIVED = 4, "Archived"

    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="service_advertisements",
    )

    service_category = models.CharField(
        max_length=30,
        choices=ServiceCategoryChoices.choices,
        db_index=True,
    )

    service_name = models.CharField(max_length=150)

    service_description = models.TextField(blank=True)

    region = models.CharField(max_length=50, db_index=True)
    township = models.CharField(max_length=50, db_index=True)

    quarter = models.CharField(max_length=100, blank=True)

    service_area = models.JSONField(
        default=dict,
        blank=True,
    )

    contact_info = models.JSONField(
        default=dict,
        blank=True,
    )

    price_info = models.JSONField(
        default=dict,
        blank=True,
    )

    featured_image = models.URLField(max_length=500, blank=True)

    status = models.PositiveSmallIntegerField(
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        db_index=True,
    )

    starts_at = models.DateTimeField()
    expires_at = models.DateTimeField(db_index=True)

    is_boosted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(
                fields=["status", "service_category", "-created_at"],
                name="idx_service_ad_status_category",
            ),
            models.Index(
                fields=["township", "service_category", "status"],
                name="idx_service_ad_township_category",
            ),
            models.Index(
                fields=["expires_at", "status"],
                name="idx_service_ad_expiry_status",
            ),
        ]

    def __str__(self):
        return self.service_name

class ServiceAdvertisementImage(models.Model):
    advertisement = models.ForeignKey(
        ServiceAdvertisement,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image_url = models.URLField(max_length=500)
    thumbnail_url = models.URLField(max_length=500, blank=True)

    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_primary", "sort_order", "created_at"]

        indexes = [
            models.Index(
                fields=["advertisement", "sort_order"],
                name="idx_service_ad_image_order",
            ),
        ]

    def __str__(self):
        return f"Image for Advertisement {self.advertisement_id}"