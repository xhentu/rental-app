# listings/filters.py
import django_filters
from .models import Listing

class ListingFilter(django_filters.FilterSet):
    # 1. Price Range Filters (Crucial for budget matching)
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    
    # 2. Size Range Filters
    min_width = django_filters.NumberFilter(field_name="width", lookup_expr='gte')
    min_length = django_filters.NumberFilter(field_name="length", lookup_expr='gte')

    # 3. GIN-Indexed JSON Feature Filters
    # Allows Flutter to pass query params like ?aircon=true or ?fully_repaired=true
    aircon = django_filters.BooleanFilter(field_name="features__aircon")
    fully_repaired = django_filters.BooleanFilter(field_name="features__fully_repaired")
    facing = django_filters.CharFilter(field_name="features__facing", lookup_expr='iexact')

    # 4. GIN-Indexed JSON Room Structure Filters
    # Allows querying for specific layout requirements like ?master_bed=1
    master_bed = django_filters.NumberFilter(field_name="room_structure__master_bed", lookup_expr='exact')
    single_bed = django_filters.NumberFilter(field_name="room_structure__single_bed", lookup_expr='exact')
    bathroom = django_filters.NumberFilter(field_name="room_structure__bathroom", lookup_expr='exact')

    class Meta:
        model = Listing
        # Core fields that use standard single-column indexing
        fields = [
            'township', 
            'region',
            'offer_type', 
            'property_type', 
            'hostel_type', 
            'owner_direct', 
            'installment_available',
            'is_presale'
        ]