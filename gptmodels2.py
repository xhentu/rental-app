from datetime import timedelta

from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone


def default_expiry_date():
    """
    Default public listing lifetime.

    This can later be replaced by a per-user/per-plan expiry system.
    """
    return timezone.now() + timedelta(days=90)


# ============================================================
# LOCATION
# ============================================================

class Region(models.Model):
    """
    Static / relatively stable administrative region.

    Example:
        1 = Yangon
        2 = Mandalay
    """

    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Township(models.Model):
    """
    Township belongs to exactly one region.

    Listing keeps both region_id and township_id because region
    is expected to be a very common search/filter dimension.
    """

    id = models.PositiveSmallIntegerField(primary_key=True)

    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="townships",
    )

    name = models.CharField(max_length=60)

    class Meta:
        ordering = ["region_id", "id"]

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
        return f"{self.name} ({self.region.name})"


# ============================================================
# LISTING
# ============================================================

class Listing(models.Model):

    # --------------------------------------------------------
    # OFFER
    # --------------------------------------------------------

    class OfferType(models.IntegerChoices):
        FOR_RENT = 1, "For Rent"
        FOR_SALE = 2, "For Sale"
        WANT_TO_RENT = 3, "Want to Rent"
        WANT_TO_BUY = 4, "Want to Buy"

    # --------------------------------------------------------
    # PROPERTY TYPE
    #
    # These are intentionally the main choices exposed to users.
    #
    # Rent-first, but still broad enough for an estate platform.
    # --------------------------------------------------------

    class PropertyType(models.IntegerChoices):
        LANDED_HOUSE = 1, "Landed House"
        APARTMENT = 2, "Apartment"
        CONDO = 3, "Condo"
        SHOP = 4, "Shop"
        OFFICE = 5, "Office"
        INDUSTRIAL = 6, "Industrial"
        LAND = 7, "Plot of Land"
        OTHER = 99, "Other"

    # --------------------------------------------------------
    # LISTING STATUS
    # --------------------------------------------------------

    class Status(models.IntegerChoices):
        DRAFT = 1, "Draft"
        ACTIVE = 2, "Active"
        PAUSED = 3, "Paused"
        COMPLETED = 4, "Completed"
        EXPIRED = 5, "Expired"
        DELETED = 6, "Deleted"

    # --------------------------------------------------------
    # PRICE PERIOD
    #
    # Very important for a rental-focused app.
    #
    # "500,000" is meaningless without knowing whether that is
    # monthly, yearly, or the total asking price.
    # --------------------------------------------------------

    class PricePeriod(models.IntegerChoices):
        MONTHLY = 1, "Monthly"
        YEARLY = 2, "Yearly"
        TOTAL = 3, "Total"
        NEGOTIABLE = 4, "Negotiable"
        CONTACT = 5, "Contact for Price"

    # --------------------------------------------------------
    # FURNISHING
    # --------------------------------------------------------

    class Furnishing(models.IntegerChoices):
        UNFURNISHED = 1, "Unfurnished"
        SEMI_FURNISHED = 2, "Semi-Furnished"
        FULLY_FURNISHED = 3, "Fully Furnished"
        BARE_SHELL = 4, "Bare Shell"
        OTHER = 99, "Other"

    # --------------------------------------------------------
    # FACING
    # --------------------------------------------------------

    class Facing(models.IntegerChoices):
        NORTH = 1, "North"
        SOUTH = 2, "South"
        EAST = 3, "East"
        WEST = 4, "West"
        NORTH_EAST = 5, "North-East"
        NORTH_WEST = 6, "North-West"
        SOUTH_EAST = 7, "South-East"
        SOUTH_WEST = 8, "South-West"

    # --------------------------------------------------------
    # OPERATIONAL STATUS
    #
    # This is different from marketplace Status.
    #
    # Example:
    # marketplace = ACTIVE
    # operational_status = OPERATING
    # --------------------------------------------------------

    class OperationalStatus(models.IntegerChoices):
        VACANT = 1, "Vacant"
        OCCUPIED = 2, "Occupied"
        OPERATING = 3, "Operating / Running"
        TEMPORARILY_CLOSED = 4, "Temporarily Closed"
        UNDER_RENOVATION = 5, "Under Renovation"
        UNDER_CONSTRUCTION = 6, "Under Construction"

    # ========================================================
    # 1. OWNER / POSTER
    # ========================================================

    landlord = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listings",
    )

    is_owner_direct = models.BooleanField(
        default=False,
        help_text="True when the advertiser is the property owner/direct owner.",
    )

    # ========================================================
    # 2. CORE SEARCH IDENTITY
    #
    # These are the fields the search engine is expected to use
    # constantly.
    # ========================================================

    offer_type = models.PositiveSmallIntegerField(
        choices=OfferType.choices,
    )

    property_type = models.PositiveSmallIntegerField(
        choices=PropertyType.choices,
    )

    # --------------------------------------------------------
    # Optional subtype.
    #
    # Examples:
    #   apartment -> studio
    #   apartment -> serviced_apartment
    #   condo -> high_rise_condo
    #   industrial -> warehouse
    #   other -> whatever the user specifies
    #
    # This remains flexible rather than forcing every future
    # subtype into a migration.
    # --------------------------------------------------------

    sub_property_type = models.CharField(
        max_length=60,
        blank=True,
    )

    title = models.CharField(
        max_length=180,
    )

    description = models.TextField(
        blank=True,
    )

    # ========================================================
    # 3. PRICE
    # ========================================================

    price = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        help_text="Price in the app's base currency unit, normally MMK.",
    )

    price_period = models.PositiveSmallIntegerField(
        choices=PricePeriod.choices,
        default=PricePeriod.MONTHLY,
    )

    is_negotiable = models.BooleanField(
        default=True,
    )

    # ========================================================
    # 4. LOCATION
    # ========================================================

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
        max_length=100,
        blank=True,
    )

    road = models.CharField(
        max_length=120,
        blank=True,
    )

    # Coordinates remain normal columns because map/location
    # queries should not need JSON extraction.
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    # Nearby recognizable places.
    #
    # Example:
    # ["Junction City", "Inya Lake", "Hledan Centre"]
    #
    # This is display/search support rather than authoritative
    # geographic data.
    landmarks = models.JSONField(
        default=list,
        blank=True,
    )

    # ========================================================
    # 5. LAND
    #
    # Nullable because apartments/offices/etc. may not have
    # meaningful individual land information.
    # ========================================================

    land_type = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Property-specific land classification.",
    )

    land_width = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Land width in feet.",
    )

    land_length = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Land length in feet.",
    )

    land_area = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Total land area in square feet.",
    )

    # Less-common land information.
    #
    # Example:
    # {
    #     "shape": "rectangular",
    #     "corner_plot": true,
    #     "road_width_ft": 20,
    #     "garden": true
    # }
    land_details = models.JSONField(
        default=dict,
        blank=True,
    )

    # ========================================================
    # 6. BUILDING / UNIT
    #
    # These are particularly important for apartment rentals.
    # ========================================================

    building_width = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Building/unit width in feet.",
    )

    building_length = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Building/unit length in feet.",
    )

    building_area = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Usable/building area in square feet.",
    )

    building_height = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Building height in feet where relevant.",
    )

    total_floors = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    floor_level = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="0 = ground floor, 1 = first floor, etc.",
    )

    bedrooms = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    bathrooms = models.PositiveSmallIntegerField(
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

    # ========================================================
    # 7. RENTAL-SPECIFIC CORE
    #
    # Because RENT is the primary business.
    #
    # These are intentionally columns rather than JSON.
    # ========================================================

    available_from = models.DateField(
        null=True,
        blank=True,
        help_text="Date the property becomes available.",
    )

    minimum_lease_months = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    advance_months = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    deposit_amount = models.PositiveBigIntegerField(
        null=True,
        blank=True,
    )

    maintenance_fee_monthly = models.PositiveBigIntegerField(
        null=True,
        blank=True,
    )

    # ========================================================
    # 8. FLEXIBLE PROPERTY DATA
    #
    # These are deliberately NOT columns.
    #
    # Different property types can put their own details here.
    # ========================================================

    room_structure = models.JSONField(
        default=dict,
        blank=True,
        help_text="""
        Detailed room breakdown.

        Example:
        {
            "master_bedroom": 1,
            "single_bedroom": 2,
            "living_room": 1,
            "kitchen": 1,
            "dining_room": 1
        }
        """,
    )

    amenities = models.JSONField(
        default=list,
        blank=True,
        help_text="""
        Example:
        [
            "lift",
            "parking",
            "security",
            "generator",
            "air_conditioning"
        ]
        """,
    )

    building_details = models.JSONField(
        default=dict,
        blank=True,
        help_text="""
        Building/utility details.

        Example:
        {
            "has_lift": true,
            "has_generator": true,
            "has_3phase_power": false,
            "water_supply": "municipal"
        }
        """,
    )

    property_details = models.JSONField(
        default=dict,
        blank=True,
        help_text="""
        Property-type-specific information.

        Apartment:
        {
            "floor_material": "tile",
            "kitchen_type": "open",
            "balcony": true
        }

        Industrial:
        {
            "loading_dock": true,
            "truck_access": true,
            "floor_load_kg_sqm": 500
        }

        Office:
        {
            "workstations": 30,
            "meeting_rooms": 2
        }
        """,
    )

    transaction_details = models.JSONField(
        default=dict,
        blank=True,
        help_text="""
        Less-common transaction information.

        Example:
        {
            "accepted_banks": ["KBZ", "AYA", "CB"],
            "tax_responsibility": "shared",
            "installment_available": true
        }
        """,
    )

    # ========================================================
    # 9. CONTACT
    #
    # Contact information is not part of the search index.
    # Keep it flexible.
    # ========================================================

    contact_info = models.JSONField(
        default=dict,
        blank=True,
        help_text="""
        Example:
        {
            "contact_person": "U Ba",
            "primary_phone": "09123456789",
            "additional_phones": ["09987654321"],
            "viber": "09123456789",
            "telegram": "username",
            "whatsapp": "09123456789"
        }
        """,
    )

    # ========================================================
    # 10. PRESENTATION / MONETIZATION
    # ========================================================

    featured_image_url = models.URLField(
        max_length=500,
        blank=True,
    )

    active_buttons = models.JSONField(
        default=dict,
        blank=True,
    )

    is_boosted = models.BooleanField(
        default=False,
    )

    is_premium = models.BooleanField(
        default=False,
    )

    # ========================================================
    # 11. PROPERTY OPERATIONAL STATE
    # ========================================================

    operational_status = models.PositiveSmallIntegerField(
        choices=OperationalStatus.choices,
        null=True,
        blank=True,
    )

    # ========================================================
    # 12. MARKETPLACE LIFECYCLE
    # ========================================================

    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=Status.DRAFT,
    )

    # ========================================================
    # 13. SYSTEM
    # ========================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    expiry_date = models.DateTimeField(
        default=default_expiry_date,
    )

    post_cost = models.PositiveIntegerField(
        default=0,
    )

    # ========================================================
    # DATABASE INDEXES
    # ========================================================

    class Meta:

        ordering = [
            "-is_boosted",
            "-created_at",
        ]

        indexes = [

            # ------------------------------------------------
            # PRIMARY RENTAL SEARCH
            #
            # Expected query:
            #
            #   active
            #   rent
            #   township
            #   property type
            #
            # This is probably your single most important
            # index family.
            # ------------------------------------------------

            models.Index(
                fields=[
                    "township",
                    "property_type",
                    "price",
                ],
                name="idx_listing_rent_search",
                condition=Q(
                    status=Status.ACTIVE,
                    offer_type=OfferType.FOR_RENT,
                ),
            ),

            # ------------------------------------------------
            # RENTAL PRICE RANGE
            # ------------------------------------------------

            models.Index(
                fields=[
                    "township",
                    "price",
                ],
                name="idx_listing_town_price",
                condition=Q(
                    status=Status.ACTIVE,
                    offer_type=OfferType.FOR_RENT,
                ),
            ),

            # ------------------------------------------------
            # APARTMENT SEARCH
            #
            # Very likely to be heavily used by your app.
            #
            # Example:
            # Yangon
            # Sanchaung
            # Apartment
            # 2 bedrooms
            # under 800,000
            # ------------------------------------------------

            models.Index(
                fields=[
                    "township",
                    "property_type",
                    "bedrooms",
                    "price",
                ],
                name="idx_listing_apartment_search",
                condition=Q(
                    status=Status.ACTIVE,
                    offer_type=OfferType.FOR_RENT,
                    property_type=PropertyType.APARTMENT,
                ),
            ),

            # ------------------------------------------------
            # CONDO SEARCH
            # ------------------------------------------------

            models.Index(
                fields=[
                    "township",
                    "bedrooms",
                    "price",
                ],
                name="idx_listing_condo_search",
                condition=Q(
                    status=Status.ACTIVE,
                    offer_type=OfferType.FOR_RENT,
                    property_type=PropertyType.CONDO,
                ),
            ),

            # ------------------------------------------------
            # AREA SEARCH
            # ------------------------------------------------

            models.Index(
                fields=[
                    "building_area",
                ],
                name="idx_listing_building_area",
                condition=Q(status=Status.ACTIVE),
            ),

            models.Index(
                fields=[
                    "land_area",
                ],
                name="idx_listing_land_area",
                condition=Q(status=Status.ACTIVE),
            ),

            # ------------------------------------------------
            # FEED
            # ------------------------------------------------

            models.Index(
                fields=[
                    "-is_boosted",
                    "-created_at",
                ],
                name="idx_listing_feed",
                condition=Q(status=Status.ACTIVE),
            ),

            # ------------------------------------------------
            # EXPIRATION WORKER
            # ------------------------------------------------

            models.Index(
                fields=[
                    "expiry_date",
                ],
                name="idx_listing_expiry",
            ),

            # ------------------------------------------------
            # JSONB
            #
            # Start with only the JSON indexes that are likely
            # to matter.
            #
            # Do NOT put GIN indexes on every JSON field.
            # ------------------------------------------------

            GinIndex(
                fields=["amenities"],
                name="idx_listing_amenities_gin",
            ),

            GinIndex(
                fields=["property_details"],
                name="idx_listing_property_details_gin",
            ),
        ]

    # ========================================================
    # VALIDATION
    # ========================================================

    def clean(self):
        errors = {}

        # --------------------------------------------
        # Township must belong to selected region.
        # --------------------------------------------

        if self.township_id and self.region_id:
            if self.township.region_id != self.region_id:
                errors["township"] = (
                    "Selected township does not belong to selected region."
                )

        # --------------------------------------------
        # Price-period sanity.
        # --------------------------------------------

        if self.price_period == self.PricePeriod.CONTACT:
            if self.price is not None:
                errors["price"] = (
                    "Price should be empty when price period is 'Contact for Price'."
                )

        # --------------------------------------------
        # Floor sanity.
        # --------------------------------------------

        if (
            self.floor_level is not None
            and self.total_floors is not None
            and self.floor_level > self.total_floors
        ):
            errors["floor_level"] = (
                "Floor level cannot be greater than total floors."
            )

        # --------------------------------------------
        # Dimensions.
        # --------------------------------------------

        if self.building_width and self.building_length:
            calculated_area = (
                self.building_width * self.building_length
            )

            # Don't silently overwrite user-entered area here.
            # The service layer can calculate it consistently.
            if (
                self.building_area is not None
                and self.building_area != calculated_area
            ):
                errors["building_area"] = (
                    "Building area does not match width × length."
                )

        if self.land_width and self.land_length:
            calculated_land_area = (
                self.land_width * self.land_length
            )

            if (
                self.land_area is not None
                and self.land_area != calculated_land_area
            ):
                errors["land_area"] = (
                    "Land area does not match width × length."
                )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        # Calculate areas when dimensions are supplied.
        #
        # This keeps range-search fields ready for the database.
        if self.building_width and self.building_length:
            self.building_area = (
                self.building_width * self.building_length
            )

        if self.land_width and self.land_length:
            self.land_area = (
                self.land_width * self.land_length
            )

        # Premium listings automatically receive boosted sorting.
        if self.is_premium:
            self.is_boosted = True

        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.pk}] {self.title}"


# ============================================================
# LISTING IMAGES
# ============================================================

class ListingImage(models.Model):

    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image_url = models.URLField(
        max_length=500,
    )

    thumbnail_url = models.URLField(
        max_length=500,
        blank=True,
    )

    is_primary = models.BooleanField(
        default=False,
    )

    sort_order = models.PositiveSmallIntegerField(
        default=0,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = [
            "-is_primary",
            "sort_order",
            "created_at",
        ]

        indexes = [
            models.Index(
                fields=["listing", "-is_primary", "sort_order"],
                name="idx_listing_images",
            ),
        ]

    def __str__(self):
        return f"Image for Listing {self.listing_id}"