from decimal import Decimal
from rest_framework import serializers
from .models import Listing, ListingImage, Region, Township


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
        read_only_fields = ["id", "created_at"]


class ListingSerializer(serializers.ModelSerializer):
    images = ListingImageSerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        fields = [
            "id",
            "offer_type",
            "property_type",
            "property_subtype",
            "property_subtype_custom",
            "title",
            "price",
            "price_period",
            "region",
            "township",
            "quarter",
            "road",
            "coordinates",
            "landmarks",
            "land_type",
            "land_width",
            "land_length",
            "land_area",
            "land_features",
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
            "property_special_features",
            "operational_status",
            "is_owner_direct",
            "sales_info",
            "rental_info",
            "contact_info",
            "featured_image",
            "images",
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
    # HELPER VALIDATORS
    # ============================================================

    @staticmethod
    def _validate_json_type(value, expected_type, type_name, field_name):
        if value is None:
            return expected_type()
        if not isinstance(value, expected_type):
            raise serializers.ValidationError(f"{field_name} must be a JSON {type_name}.")
        return value

    @staticmethod
    def _validate_positive_decimal(value, field_name):
        if value is not None and value <= 0:
            raise serializers.ValidationError(f"{field_name} must be greater than zero.")
        return value

    # ============================================================
    # FIELD VALIDATORS
    # ============================================================

    def validate_coordinates(self, value):
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise serializers.ValidationError("coordinates must be a JSON object.")

        if not value:
            return value

        if "latitude" not in value or "longitude" not in value:
            raise serializers.ValidationError("coordinates must contain both latitude and longitude.")

        try:
            lat = Decimal(str(value["latitude"]))
            lng = Decimal(str(value["longitude"]))
        except Exception:
            raise serializers.ValidationError("latitude and longitude must be valid numbers.")

        if not (Decimal("-90") <= lat <= Decimal("90")):
            raise serializers.ValidationError("latitude must be between -90 and 90.")

        if not (Decimal("-180") <= lng <= Decimal("180")):
            raise serializers.ValidationError("longitude must be between -180 and 180.")

        return {"latitude": float(lat), "longitude": float(lng)}

    def validate_landmarks(self, value):
        return self._validate_json_type(value, list, "list", "landmarks")

    def validate_land_features(self, value):
        return self._validate_json_type(value, dict, "object", "land_features")

    def validate_room_structure(self, value):
        return self._validate_json_type(value, dict, "object", "room_structure")

    def validate_building_features(self, value):
        return self._validate_json_type(value, dict, "object", "building_features")

    def validate_property_special_features(self, value):
        return self._validate_json_type(value, dict, "object", "property_special_features")

    def validate_sales_info(self, value):
        return self._validate_json_type(value, dict, "object", "sales_info")

    def validate_rental_info(self, value):
        return self._validate_json_type(value, dict, "object", "rental_info")

    def validate_contact_info(self, value):
        return self._validate_json_type(value, dict, "object", "contact_info")

    # Numeric Bounds
    def validate_land_width(self, val): return self._validate_positive_decimal(val, "land_width")
    def validate_land_length(self, val): return self._validate_positive_decimal(val, "land_length")
    def validate_building_width(self, val): return self._validate_positive_decimal(val, "building_width")
    def validate_building_length(self, val): return self._validate_positive_decimal(val, "building_length")
    def validate_land_area(self, val): return self._validate_positive_decimal(val, "land_area")
    def validate_building_area(self, val): return self._validate_positive_decimal(val, "building_area")

    def validate_total_floors(self, val):
        if val is not None and val < 1:
            raise serializers.ValidationError("total_floors must be at least 1.")
        return val

    def validate_floor_level(self, val):
        if val is not None and val < 0:
            raise serializers.ValidationError("floor_level cannot be negative.")
        return val

    def validate_bedrooms(self, val):
        if val is not None and val < 0:
            raise serializers.ValidationError("bedrooms cannot be negative.")
        return val

    # ============================================================
    # CROSS-FIELD VALIDATION (PARTIAL-UPDATE AWARE)
    # ============================================================

    def validate(self, attrs):
        # Resolve current instance state for PATCH operations
        instance = getattr(self, "instance", None)

        def get_field(name):
            if name in attrs:
                return attrs[name]
            return getattr(instance, name, None) if instance else None

        offer_type = get_field("offer_type")
        property_type = get_field("property_type")
        property_subtype = get_field("property_subtype")
        property_subtype_custom = (get_field("property_subtype_custom") or "").strip()
        price_period = get_field("price_period")
        sales_info = get_field("sales_info")
        rental_info = get_field("rental_info")
        region = get_field("region")
        township = get_field("township")

        # 1. Subtype check
        if property_subtype == Listing.PropertySubtypeChoices.OTHER:
            if not property_subtype_custom:
                raise serializers.ValidationError({
                    "property_subtype_custom": "This field is required when property_subtype is Other."
                })
        elif property_subtype_custom:
            raise serializers.ValidationError({
                "property_subtype_custom": "Custom subtype should only be provided when property_subtype is Other."
            })

        # 2. Offer Type rules
        if offer_type == Listing.OfferChoices.RENT:
            if sales_info:
                raise serializers.ValidationError({"sales_info": "Sales info must not be provided for a rental listing."})
            if price_period is None:
                raise serializers.ValidationError({"price_period": "Price period is required for rental listings."})

        elif offer_type == Listing.OfferChoices.SALE:
            if rental_info:
                raise serializers.ValidationError({"rental_info": "Rental info must not be provided for a sale listing."})
            if price_period is not None:
                raise serializers.ValidationError({"price_period": "Price period should not be provided for a sale listing."})

        # 3. Region / Township foreign key check
        if region and township:
            if township.region_id != region.id:
                raise serializers.ValidationError({"township": "The selected township does not belong to the selected region."})

        # 4. Land specific checks
        if property_type != Listing.CategoryChoices.LAND:
            land_fields = ["land_type", "land_width", "land_length", "land_area", "land_features"]
            errors = {}
            for field in land_fields:
                val = get_field(field)
                if val not in (None, "", {}, []):
                    errors[field] = "This field is only applicable to Plot of Land listings."
            if errors:
                raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        # Automatically assign landlord from request user context
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["landlord"] = request.user
        return super().create(validated_data)