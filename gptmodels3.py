from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q


class Region(models.Model):
    """
    Top-level administrative region/state.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class Township(models.Model):
    """
    Township belongs to exactly one Region.
    """

    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="townships",
    )

    name = models.CharField(
        max_length=100,
    )

    class Meta:
        ordering = ["region", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["region", "name"],
                name="uniq_township_region_name",
            ),
        ]
        indexes = [
            models.Index(fields=["region", "name"]),
        ]

    def __str__(self):
        return f"{self.name}, {self.region.name}"


class Listing(models.Model):
    """
    Main real-estate listing.

    Architecture:
        SQL columns
            -> universal/fundamental/search-summary information

        JSON fields
            -> property-type-specific and flexible details

        ListingImage
            -> repeating image relationship

    Intentionally has NO description field.
    The structured listing data itself represents the property.
    """

    # ------------------------------------------------------------------
    # ENUMS
    # ------------------------------------------------------------------

    class OfferType(models.IntegerChoices):
        RENT = 1, "Rent"
        SALE = 2, "Sale"
        RENT_OR_SALE = 3, "Rent or Sale"
        OTHER = 99, "Other"

    class PropertyType(models.IntegerChoices):
        LANDED_HOUSE = 1, "Landed House"
        APARTMENT = 2, "Apartment"
        CONDO = 3, "Condo"
        SHOP = 4, "Shop"
        OFFICE = 5, "Office"
        INDUSTRIAL = 6, "Industrial"
        PLOT_OF_LAND = 7, "Plot of Land"
        OTHER = 99, "Other"

    class PricePeriod(models.IntegerChoices):
        MONTH = 1, "Monthly"
        WEEK = 2, "Weekly"
        DAY = 3, "Daily"
        YEAR = 4, "Yearly"
        ONE_TIME = 5, "One time"
        OTHER = 99, "Other"

    class Furnishing(models.IntegerChoices):
        UNFURNISHED = 1, "Unfurnished"
        SEMI_FURNISHED = 2, "Semi-furnished"
        FULLY_FURNISHED = 3, "Fully furnished"
        UNKNOWN = 99, "Unknown"

    class Facing(models.IntegerChoices):
        NORTH = 1, "North"
        SOUTH = 2, "South"
        EAST = 3, "East"
        WEST = 4, "West"
        NORTH_EAST = 5, "North-East"
        NORTH_WEST = 6, "North-West"
        SOUTH_EAST = 7, "South-East"
        SOUTH_WEST = 8, "South-West"
        UNKNOWN = 99, "Unknown"

    class Status(models.IntegerChoices):
        DRAFT = 1, "Draft"
        ACTIVE = 2, "Active"
        RESERVED = 3, "Reserved"
        SOLD = 4, "Sold"
        RENTED = 5, "Rented"
        EXPIRED = 6, "Expired"
        ARCHIVED = 7, "Archived"

    class OperationalStatus(models.IntegerChoices):
        VACANT = 1, "Vacant"
        OCCUPIED = 2, "Occupied"
        OWNER_OCCUPIED = 3, "Owner occupied"
        UNDER_CONSTRUCTION = 4, "Under construction"
        RENOVATION = 5, "Under renovation"
        UNKNOWN = 99, "Unknown"

    # ------------------------------------------------------------------
    # IDENTITY / OWNERSHIP
    # ------------------------------------------------------------------

    id = models.BigAutoField(
        primary_key=True,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="property_listings",
    )

    is_owner_direct = models.BooleanField(
        default=True,
        help_text="Whether the listing is directly from the owner rather than an intermediary.",
    )

    offer_type = models.PositiveSmallIntegerField(
        choices=OfferType.choices,
        db_index=True,
    )

    # ------------------------------------------------------------------
    # PROPERTY CLASSIFICATION
    #
    # IMPORTANT:
    # Exactly two levels:
    #
    #       property_type
    #           └── property_subtype
    #
    # No family -> type -> subtype hierarchy.
    # ------------------------------------------------------------------

    property_type = models.PositiveSmallIntegerField(
        choices=PropertyType.choices,
        db_index=True,
    )

    property_subtype = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text=(
            "Subtype directly under property_type. "
            "Examples: restaurant, retail, warehouse, hostel, etc."
        ),
    )

    title = models.CharField(
        max_length=255,
    )

    # ------------------------------------------------------------------
    # PRICE / TRANSACTION SUMMARY
    # ------------------------------------------------------------------

    price = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0")),
        ],
        db_index=True,
    )

    price_period = models.PositiveSmallIntegerField(
        choices=PricePeriod.choices,
        default=PricePeriod.MONTH,
        db_index=True,
    )

    is_negotiable = models.BooleanField(
        default=False,
    )

    # ------------------------------------------------------------------
    # LOCATION
    # ------------------------------------------------------------------

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

    quarter = models.CharField(
        max_length=150,
        blank=True,
        default="",
    )

    road = models.CharField(
        max_length=200,
        blank=True,
        default="",
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(Decimal("-90")),
            MaxValueValidator(Decimal("90")),
        ],
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(Decimal("-180")),
            MaxValueValidator(Decimal("180")),
        ],
    )

    # Flexible location information:
    #
    # {
    #     "landmarks": [
    #         {"name": "...", "distance_m": 500},
    #         ...
    #     ],
    #     "location_notes": "...",
    #     "access_notes": "..."
    # }
    #
    location_details = models.JSONField(
        default=dict,
        blank=True,
    )

    # ------------------------------------------------------------------
    # CORE PROPERTY MEASUREMENTS
    #
    # These are columns because land/building size are fundamental
    # property facts, even when a particular property type doesn't
    # use every field.
    # ------------------------------------------------------------------

    land_width = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0"))],
    )

    land_length = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0"))],
    )

    land_area = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0"))],
        db_index=True,
    )

    building_width = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0"))],
    )

    building_length = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0"))],
    )

    building_area = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0"))],
        db_index=True,
    )

    building_height = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0"))],
    )

    # ------------------------------------------------------------------
    # CORE BUILDING / ROOM SUMMARY
    #
    # Summary goes in columns.
    # Detailed composition goes into room_structure JSON.
    #
    # Example:
    # bedrooms = 3
    #
    # room_structure = {
    #     "master_bedroom": 2,
    #     "single_bedroom": 1,
    #     "living_room": 1,
    #     ...
    # }
    # ------------------------------------------------------------------

    bedrooms = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        db_index=True,
    )

    bathrooms = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        db_index=True,
    )

    floor_level = models.SmallIntegerField(
        null=True,
        blank=True,
    )

    total_floors = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    furnishing = models.PositiveSmallIntegerField(
        choices=Furnishing.choices,
        null=True,
        blank=True,
    )

    facing = models.PositiveSmallIntegerField(
        choices=Facing.choices,
        null=True,
        blank=True,
    )

    parking_spaces = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    year_built = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    # ------------------------------------------------------------------
    # RENTAL CORE
    #
    # Rental is the primary business use case, so these aren't buried
    # inside JSON.
    # ------------------------------------------------------------------

    available_from = models.DateField(
        null=True,
        blank=True,
        db_index=True,
    )

    minimum_lease_months = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    advance_months = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    deposit_amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0"))],
    )

    maintenance_fee_monthly = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0"))],
    )

    # ------------------------------------------------------------------
    # JSON: ROOM DETAIL
    # ------------------------------------------------------------------

    room_structure = models.JSONField(
        default=dict,
        blank=True,
        help_text=(
            "Detailed room composition. "
            "Summary room counts remain in bedrooms/bathrooms."
        ),
    )

    # ------------------------------------------------------------------
    # JSON: LAND-SPECIFIC DETAILS
    #
    # Examples:
    # {
    #     "land_use": "residential",
    #     "land_shape": "rectangular",
    #     "corner_plot": true,
    #     "road_width_ft": 40,
    #     "soil_type": "...",
    #     "flood_risk": "low",
    #     "title_type": "..."
    # }
    # ------------------------------------------------------------------

    land_features = models.JSONField(
        default=dict,
        blank=True,
    )

    # ------------------------------------------------------------------
    # JSON: BUILDING DETAILS
    #
    # Examples:
    # {
    #     "structure_type": "RC",
    #     "construction_material": "...",
    #     "roof_type": "...",
    #     "elevator_count": 2,
    #     "staircases": 2,
    #     "generator": {...},
    #     "transformer": {...}
    # }
    # ------------------------------------------------------------------

    building_features = models.JSONField(
        default=dict,
        blank=True,
    )

    # ------------------------------------------------------------------
    # JSON: PROPERTY-TYPE-SPECIFIC DETAILS
    #
    # This is the important escape hatch for the wide property universe.
    #
    # Shop:
    # {
    #     "allowed_businesses": ["restaurant", "retail"],
    #     "frontage_width_ft": 20,
    #     "ceiling_height_ft": 14,
    #     ...
    # }
    #
    # Hostel:
    # {
    #     "hostel_type": "...",
    #     "capacity": 30,
    #     "male_female": "mixed",
    #     ...
    # }
    #
    # Industrial:
    # {
    #     "floor_load_kg_m2": 2000,
    #     "loading_bay": true,
    #     "crane": {...},
    #     "power_capacity_kva": 500,
    #     ...
    # }
    # ------------------------------------------------------------------

    property_features = models.JSONField(
        default=dict,
        blank=True,
    )

    # ------------------------------------------------------------------
    # JSON: AMENITIES / SERVICES
    #
    # Examples:
    # {
    #     "air_conditioning": true,
    #     "water_supply": true,
    #     "internet": true,
    #     "security": true,
    #     "lift": true,
    #     ...
    # }
    # ------------------------------------------------------------------

    amenities = models.JSONField(
        default=dict,
        blank=True,
    )

    # ------------------------------------------------------------------
    # JSON: TRANSACTION-SPECIFIC DETAILS
    #
    # Used for sale/legal/transaction information that isn't central
    # enough to every listing to deserve its own SQL column.
    # ------------------------------------------------------------------

    transaction_details = models.JSONField(
        default=dict,
        blank=True,
    )

    # ------------------------------------------------------------------
    # CONTACT
    #
    # Flexible because different listing sources/accounts may expose
    # different contact methods.
    #
    # {
    #     "phone": "...",
    #     "phone_2": "...",
    #     "viber": "...",
    #     "telegram": "...",
    #     "whatsapp": "...",
    #     "contact_name": "..."
    # }
    # ------------------------------------------------------------------

    contact_info = models.JSONField(
        default=dict,
        blank=True,
    )

    # ------------------------------------------------------------------
    # UI / ACTIONS
    #
    # Example:
    # {
    #     "call": true,
    #     "message": true,
    #     "viber": true,
    #     "telegram": true
    # }
    # ------------------------------------------------------------------

    active_buttons = models.JSONField(
        default=dict,
        blank=True,
    )

    # ------------------------------------------------------------------
    # MEDIA
    #
    # Keep a cached featured image reference here for fast feed queries.
    # Full image collection lives in ListingImage.
    # ------------------------------------------------------------------

    featured_image_url = models.URLField(
        max_length=1000,
        blank=True,
        default="",
    )

    # ------------------------------------------------------------------
    # LIFECYCLE
    # ------------------------------------------------------------------

    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )

    operational_status = models.PositiveSmallIntegerField(
        choices=OperationalStatus.choices,
        default=OperationalStatus.UNKNOWN,
    )

    is_boosted = models.BooleanField(
        default=False,
    )

    is_premium = models.BooleanField(
        default=False,
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    post_cost = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0"))],
    )

    # ------------------------------------------------------------------
    # DATABASE INDEXES / CONSTRAINTS
    # ------------------------------------------------------------------

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            # Main rental search path
            models.Index(
                fields=[
                    "township",
                    "property_type",
                    "price",
                ],
                name="listing_rent_search_idx",
            ),

            # Apartment / condo room search
            models.Index(
                fields=[
                    "township",
                    "property_type",
                    "bedrooms",
                    "price",
                ],
                name="listing_room_search_idx",
            ),

            # General feed
            models.Index(
                fields=[
                    "status",
                    "-created_at",
                ],
                name="listing_feed_idx",
            ),

            # Availability
            models.Index(
                fields=[
                    "status",
                    "available_from",
                ],
                name="listing_available_idx",
            ),

            # Property classification
            models.Index(
                fields=[
                    "property_type",
                    "property_subtype",
                ],
                name="listing_type_subtype_idx",
            ),

            # Area searches
            models.Index(
                fields=[
                    "property_type",
                    "land_area",
                ],
                name="listing_land_area_idx",
            ),

            models.Index(
                fields=[
                    "property_type",
                    "building_area",
                ],
                name="listing_build_area_idx",
            ),

            # Expiry processing
            models.Index(
                fields=[
                    "status",
                    "expires_at",
                ],
                name="listing_expiry_idx",
            ),

            # Direct owner filtering
            models.Index(
                fields=[
                    "is_owner_direct",
                    "status",
                ],
                name="listing_owner_direct_idx",
            ),
        ]

        constraints = [
            models.CheckConstraint(
                condition=Q(price__gte=0),
                name="listing_price_nonnegative",
            ),

            models.CheckConstraint(
                condition=(
                    Q(land_area__isnull=True) |
                    Q(land_area__gte=0)
                ),
                name="listing_land_area_nonnegative",
            ),

            models.CheckConstraint(
                condition=(
                    Q(building_area__isnull=True) |
                    Q(building_area__gte=0)
                ),
                name="listing_building_area_nonnegative",
            ),
        ]

    def __str__(self):
        return f"{self.title} ({self.pk})"


class ListingImage(models.Model):
    """
    Images belonging to a listing.

    Kept separate because one listing can have many images and because
    media metadata may grow independently from the core listing row.
    """

    id = models.BigAutoField(
        primary_key=True,
    )

    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image_url = models.URLField(
        max_length=1000,
    )

    sort_order = models.PositiveSmallIntegerField(
        default=0,
    )

    is_featured = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["sort_order", "id"]

        indexes = [
            models.Index(
                fields=["listing", "sort_order"],
                name="listing_image_order_idx",
            ),
        ]

    def __str__(self):
        return f"Image {self.pk} for Listing {self.listing_id}"