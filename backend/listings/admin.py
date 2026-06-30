from django.contrib import admin
from .models import Listing, ListingImage

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1 # Allows adding one image directly from the Listing page

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    # Columns shown in the main list view
    list_display = (
        'title', 
        'property_type', 
        'offer_type', 
        'township', 
        'price', 
        'is_active', 
        'is_boosted', 
        'created_at'
    )
    
    # Filters available in the right sidebar
    list_filter = (
        'offer_type', 
        'property_type', 
        'is_active', 
        'is_boosted', 
        'is_premium', 
        'region'
    )
    
    # Fields searchable in the admin search bar
    search_fields = (
        'title', 
        'township', 
        'contact_phone', 
        'contact_phone1', 
        'contact_phone2', 
        'remark'
    )
    
    # Organized layout for editing a Listing
    fieldsets = (
        ('Ownership & Core Type', {
            'fields': ('landlord', 'title', 'offer_type', 'property_type', 'is_presale')
        }),
        ('Pricing & Payment', {
            'fields': ('price', 'price_negotiable', 'installment_available', 'bank_transfer_accepted', 'payment_details')
        }),
        ('Location Details', {
            'fields': ('region', 'township', 'quarter', 'road', 'landmarks', ('latitude', 'longitude'))
        }),
        ('Dimensions & Structure', {
            'fields': (('width', 'length', 'area_dimension_text'), 'floor_data', 'room_structure', 'features', 'type_of_land')
        }),
        ('Contact Information', {
            'description': 'Main and secondary contact details for the landlord/agent.',
            'fields': (
                'contact_phone', 
                'contact_phone1', 
                'contact_phone2', 
                'viber_contact', 
                'telegram_username', 
                'whatsapp_number', 
                'active_buttons'
            )
        }),
        ('Status & Visibility', {
            'classes': ('collapse',), # Hide this section by default for a cleaner look
            'fields': ('is_active', 'is_boosted', 'is_premium', 'is_completed', 'is_deleted', 'expiry_date')
        }),
    )
    
    readonly_fields = ('area_dimension_text', 'created_at', 'updated_at')
    inlines = [ListingImageInline]

@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ('listing', 'is_primary', 'created_at')
    list_filter = ('is_primary',)