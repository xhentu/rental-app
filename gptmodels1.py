from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta


def default_expiry_date():
    return timezone.now() + timedelta(days=90)


class Region(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Township(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="townships",
    )
    name = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["region", "name"],
                name="uq_township_region_name",
            ),
        ]
        indexes = [
            models.Index(
                fields=["region", "name"],
                name="idx_township_region_name",
            ),
        ]

    def __str__(self):
        return self.name


class Listing(models.Model):

    class Offer(models.IntegerChoices):
        SALE = 1, "For Sale"
        RENT = 2, "For Rent"
        BUY = 3, "Want to Buy"
        TENANT = 4, "Want to Rent"

    class PropertyCategory(models.IntegerChoices):
        RESIDENTIAL = 1, "Residential"
        COMMERCIAL = 2, "Commercial"
        INDUSTRIAL = 3, "Industrial"
        HOSTEL = 4, "Hostel"
        LAND = 5, "Land"
        OTHER = 99, "Other"

    class Status(models.IntegerChoices):
        DRAFT = 1, "Draft"
        ACTIVE = 2, "Active"
        PAUSED = 3, "Paused"
        COMPLETED = 4, "Completed"
        EXPIRED = 5, "Expired"
        DELETED = 6, "Deleted"

    class Furnishing(models.IntegerChoices):
        UNFURNISHED = 1, "Unfurnished"
        SEMI = 2, "Semi-Furnished"
        FULL = 3, "Fully Furnished"
        HALL = 4, "Hall / Bare Shell"
        UNDER_CONSTRUCTION = 5, "Under Construction"

    class Facing(models.IntegerChoices):
        NORTH = 1, "North"
        SOUTH = 2, "South"
        EAST = 3, "East"
        WEST = 4, "West"
        NORTH_EAST = 5, "North-East"
        NORTH_WEST = 6, "North-West"
        SOUTH_EAST = 7, "South-East"
        SOUTH_WEST = 8, "South-West"

    # -------------------------------------------------
    # OWNERSHIP
    # -------------------------------------------------

    landlord = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listings",
    )

    # -------------------------------------------------
    # CORE SEARCH
    # -------------------------------------------------

    offer_type = models.PositiveSmallIntegerField(
        choices=Offer.choices
    )

    property_category = models.PositiveSmallIntegerField(
        choices=PropertyCategory.choices
    )

    # Replace with FK lookup table if subtypes become dynamic.
    property_type_id = models.PositiveSmallIntegerField(
        db_index=True,
    )

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    price = models.PositiveBigIntegerField()

    # -------------------------------------------------
    # LOCATION
    # -------------------------------------------------

    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="listings",
    )

    township = models.ForeignKey(
        Township,
        on_delete=models.PROTECT,
        related_name="listings",
    )

    quarter = models.CharField(max_length=100, blank=True)
    road = models.CharField(max_length=100, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    landmarks = models.JSONField(
        default=list,
        blank=True,
    )

    # -------------------------------------------------
    # LAND
    # -------------------------------------------------

    land_type = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    land_width = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    land_length = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    land_area = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    # -------------------------------------------------
    # BUILDING / UNIT
    # -------------------------------------------------

    building_width = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    building_length = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    building_height = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    building_area = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    bedrooms = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    bathrooms = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    total_floors = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    floor_level = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    facing = models.PositiveSmallIntegerField(
        choices=Facing.choices,
        null=True,
        blank=True,
    )

    furnishing = models.PositiveSmallIntegerField(
        choices=Furnishing.choices,
        null=True,
        blank=True,
    )

    # -------------------------------------------------
    # FLEXIBLE PROPERTY DATA
    # -------------------------------------------------

    room_structure = models.JSONField(
        default=dict,
        blank=True,
    )

    property_specs = models.JSONField(
        default=dict,
        blank=True,
    )

    amenities = models.JSONField(
        default=list,
        blank=True,
    )

    transaction_terms = models.JSONField(
        default=dict,
        blank=True,
    )

    # -------------------------------------------------
    # COMMON BUSINESS FILTERS
    # -------------------------------------------------

    is_owner_direct = models.BooleanField(default=False)
    is_negotiable = models.BooleanField(default=True)

    operational_status = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    # -------------------------------------------------
    # CONTACT / PRESENTATION
    # -------------------------------------------------

    contact_info = models.JSONField(
        default=dict,
        blank=True,
    )

    active_buttons = models.JSONField(
        default=dict,
        blank=True,
    )

    featured_image_url = models.URLField(
        max_length=500,
        blank=True,
    )

    # -------------------------------------------------
    # SYSTEM
    # -------------------------------------------------

    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=Status.DRAFT,
    )

    is_boosted = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    expiry_date = models.DateTimeField(
        default=default_expiry_date,
    )

    class Meta:
        indexes = [
            # Main active search
            models.Index(
                fields=[
                    "township",
                    "offer_type",
                    "property_category",
                    "property_type_id",
                    "price",
                ],
                name="idx_listing_search",
                condition=Q(status=Status.ACTIVE),
            ),

            # Feed
            models.Index(
                fields=[
                    "-is_boosted",
                    "-created_at",
                ],
                name="idx_listing_feed",
                condition=Q(status=Status.ACTIVE),
            ),

            # Price search
            models.Index(
                fields=["price"],
                name="idx_listing_price",
                condition=Q(status=Status.ACTIVE),
            ),

            # Area search
            models.Index(
                fields=["building_area"],
                name="idx_listing_building_area",
                condition=Q(status=Status.ACTIVE),
            ),

            models.Index(
                fields=["land_area"],
                name="idx_listing_land_area",
                condition=Q(status=Status.ACTIVE),
            ),

            # Common room filtering
            models.Index(
                fields=["bedrooms", "bathrooms"],
                name="idx_listing_rooms",
                condition=Q(status=Status.ACTIVE),
            ),

            # Expiration worker
            models.Index(
                fields=["expiry_date"],
                name="idx_listing_expiry",
            ),

            # Add GIN only if actual search requirements justify it.
            GinIndex(
                fields=["property_specs"],
                name="idx_listing_property_specs_gin",
            ),
        ]