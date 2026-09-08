from decimal import Decimal

from rest_framework import serializers

from .models import (
    Listing,
    ListingImage,
    Region,
    Township,
)


class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = [
            "id",
            "image_url",
            "thumbnail_url",
            "is_primary",
            "sort_order",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]


class ListingSerializer(serializers.ModelSerializer):
    images = ListingImageSerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = [
            # ---------------------------------
            # Classification
            # ---------------------------------
            "id",
            "offer_type",
            "property_type",
            "property_subtype",
            "property_subtype_custom",

            # ---------------------------------
            # Basic
            # ---------------------------------
            "title",
            "price",
            "price_period",

            # ---------------------------------
            # Location
            # ---------------------------------
            "region",
            "township",
            "quarter",
            "road",
            "coordinates",
            "landmarks",

            # ---------------------------------
            # Land
            # ---------------------------------
            "land_type",
            "land_width",
            "land_length",
            "land_area",
            "land_features",

            # ---------------------------------
            # Building
            # ---------------------------------
            "facing_direction",
            "furnishing",
            "building_width",
            "building_length",
            "building_area",
            "total_floors",
            "floor_level",
            "bedrooms",
            "year_built",
            "room_structure",
            "building_features",

            # ---------------------------------
            # Other
            # ---------------------------------
            "property_special_features",
            "operational_status",
            "is_owner_direct",

            # ---------------------------------
            # Sales / Rental / Contact
            # ---------------------------------
            "sales_info",
            "rental_info",
            "contact_info",

            # ---------------------------------
            # Images
            # ---------------------------------
            "featured_image",
            "images",

            # ---------------------------------
            # System
            # ---------------------------------
            "landlord",
            "created_at",
            "updated_at",
            "expires_at",
            "post_cost",
            "is_boosted",
            "status",
        ]

        read_only_fields = [
            "id",
            "landlord",
            "created_at",
            "updated_at",
            "expires_at",
            "post_cost",
            "is_boosted",
            "status",
        ]

    # ============================================================
    # BASIC JSON VALIDATION
    # ============================================================

    @staticmethod
    def validate_json_object(value, field_name):
        """
        These JSONField values are intended to be JSON objects,
        not lists, strings, numbers, etc.
        """
        if value is None:
            return {}

        if not isinstance(value, dict):
            raise serializers.ValidationError(
                f"{field_name} must be a JSON object."
            )

        return value

    @staticmethod
    def validate_json_list(value, field_name):
        """
        Used for fields that intentionally contain a JSON list.
        """
        if value is None:
            return []

        if not isinstance(value, list):
            raise serializers.ValidationError(
                f"{field_name} must be a JSON list."
            )

        return value

    # ============================================================
    # FIELD-LEVEL VALIDATION
    # ============================================================

    def validate_coordinates(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError(
                "coordinates must be a JSON object."
            )

        # Coordinates are for map display only.
        # We deliberately do not turn this into a PostGIS/radius system.

        if not value:
            return value

        latitude = value.get("latitude")
        longitude = value.get("longitude")

        if latitude is None or longitude is None:
            raise serializers.ValidationError(
                "coordinates must contain both latitude and longitude."
            )

        try:
            latitude = Decimal(str(latitude))
            longitude = Decimal(str(longitude))
        except Exception:
            raise serializers.ValidationError(
                "latitude and longitude must be valid numbers."
            )

        if not Decimal("-90") <= latitude <= Decimal("90"):
            raise serializers.ValidationError(
                "latitude must be between -90 and 90."
            )

        if not Decimal("-180") <= longitude <= Decimal("180"):
            raise serializers.ValidationError(
                "longitude must be between -180 and 180."
            )

        return value

    def validate_landmarks(self, value):
        return self.validate_json_list(value, "landmarks")

    def validate_land_features(self, value):
        return self.validate_json_object(value, "land_features")

    def validate_room_structure(self, value):
        return self.validate_json_object(value, "room_structure")

    def validate_building_features(self, value):
        return self.validate_json_object(value, "building_features")

    def validate_property_special_features(self, value):
        return self.validate_json_object(
            value,
            "property_special_features",
        )

    def validate_sales_info(self, value):
        return self.validate_json_object(value, "sales_info")

    def validate_rental_info(self, value):
        return self.validate_json_object(value, "rental_info")

    def validate_contact_info(self, value):
        return self.validate_json_object(value, "contact_info")

    # ============================================================
    # DIMENSION VALIDATION
    # ============================================================

    @staticmethod
    def validate_positive_decimal(value, field_name):
        if value is None:
            return value

        if value <= 0:
            raise serializers.ValidationError(
                f"{field_name} must be greater than zero."
            )

        return value

    def validate_land_width(self, value):
        return self.validate_positive_decimal(value, "land_width")

    def validate_land_length(self, value):
        return self.validate_positive_decimal(value, "land_length")

    def validate_building_width(self, value):
        return self.validate_positive_decimal(value, "building_width")

    def validate_building_length(self, value):
        return self.validate_positive_decimal(value, "building_length")

    def validate_land_area(self, value):
        return self.validate_positive_decimal(value, "land_area")

    def validate_building_area(self, value):
        return self.validate_positive_decimal(value, "building_area")

    # ============================================================
    # INTEGER VALIDATION
    # ============================================================

    def validate_total_floors(self, value):
        if value is not None and value < 1:
            raise serializers.ValidationError(
                "total_floors must be at least 1."
            )

        return value

    def validate_floor_level(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "floor_level cannot be negative."
            )

        return value

    def validate_bedrooms(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "bedrooms cannot be negative."
            )

        return value

    # ============================================================
    # CROSS-FIELD VALIDATION
    # ============================================================

    def validate(self, attrs):
        offer_type = attrs.get("offer_type")
        property_type = attrs.get("property_type")
        property_subtype = attrs.get("property_subtype")
        property_subtype_custom = (
            attrs.get("property_subtype_custom", "")
            or ""
        )

        price_period = attrs.get("price_period")

        sales_info = attrs.get("sales_info")
        rental_info = attrs.get("rental_info")

        region = attrs.get("region")
        township = attrs.get("township")

        # --------------------------------------------------------
        # 1. Property subtype / custom subtype
        # --------------------------------------------------------

        OTHER_SUBTYPE = Listing.PropertySubtypeChoices.OTHER

        if property_subtype == OTHER_SUBTYPE:
            if not property_subtype_custom.strip():
                raise serializers.ValidationError({
                    "property_subtype_custom": (
                        "This field is required when property_subtype "
                        "is Other."
                    )
                })

        elif property_subtype_custom.strip():
            raise serializers.ValidationError({
                "property_subtype_custom": (
                    "Custom subtype should only be provided when "
                    "property_subtype is Other."
                )
            })

        # --------------------------------------------------------
        # 2. Rental vs sale information
        # --------------------------------------------------------

        if offer_type == Listing.OfferChoices.RENT:
            if sales_info:
                raise serializers.ValidationError({
                    "sales_info": (
                        "Sales information must not be provided "
                        "for a rental listing."
                    )
                })

            if price_period is None:
                raise serializers.ValidationError({
                    "price_period": (
                        "Price period is required for rental listings."
                    )
                })

        elif offer_type == Listing.OfferChoices.SALE:
            if rental_info:
                raise serializers.ValidationError({
                    "rental_info": (
                        "Rental information must not be provided "
                        "for a sale listing."
                    )
                })

            if price_period is not None:
                raise serializers.ValidationError({
                    "price_period": (
                        "Price period should not be provided "
                        "for a sale listing."
                    )
                })

        # --------------------------------------------------------
        # 3. Region / township consistency
        # --------------------------------------------------------

        if region is not None and township is not None:
            if township.region_id != region.id:
                raise serializers.ValidationError({
                    "township": (
                        "The selected township does not belong "
                        "to the selected region."
                    )
                })

        # --------------------------------------------------------
        # 4. Land-specific consistency
        # --------------------------------------------------------

        if property_type != Listing.CategoryChoices.LAND:
            land_fields = [
                "land_type",
                "land_width",
                "land_length",
                "land_area",
                "land_features",
            ]

            supplied_land_fields = [
                field
                for field in land_fields
                if attrs.get(field) not in (None, "", {}, [])
            ]

            if supplied_land_fields:
                raise serializers.ValidationError({
                    field: (
                        "This field is only applicable to "
                        "Plot of Land listings."
                    )
                    for field in supplied_land_fields
                })

        return attrs