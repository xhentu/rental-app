from django.contrib import admin
from django.utils.html import format_html
from .models import Listing, ListingImage

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1
    readonly_fields = ['preview']
    fields = ['image_url', 'thumbnail_url', 'is_primary', 'preview']

    def preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="width: 100px; height: auto; border-radius: 5px;" />', obj.image_url)
        return "No Image"

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    # 1. Quick View List
    list_display = ['title', 'landlord', 'price', 'offer_type', 'property_type', 'is_active', 'is_boosted', 'created_at']
    list_filter = ['offer_type', 'property_type', 'is_active', 'is_boosted', 'region', 'township']
    search_fields = ['title', 'landlord__username', 'township', 'contact_phone']
    list_editable = ['is_active', 'is_boosted'] # Quick toggle from the list view
    
    # 2. Add the Image Inline
    inlines = [ListingImageInline]

    # 3. Organized Edit Form
    fieldsets = (
        ('Ownership', {
            'fields': ('landlord', 'owner_direct')
        }),
        ('Core Details', {
            'fields': (('title', 'property_type', 'offer_type'), 'price', 'remark')
        }),
        ('Dimensions', {
            'fields': (('width', 'length'), 'area_dimension_text')
        }),
        ('Location', {
            'fields': ('region', 'township', 'quarter', 'road', 'landmarks', ('latitude', 'longitude'))
        }),
        ('Status & Logistics', {
            'fields': (('is_active', 'is_completed'), ('is_boosted', 'is_premium'), 'expiry_date')
        }),
        ('Monetization & Contact', {
            'classes': ('collapse',), # Hide by default to save space
            'fields': ('active_buttons', 'contact_phone', 'viber_contact', 'telegram_username', 'whatsapp_number')
        }),
        ('Advanced Metadata', {
            'classes': ('collapse',),
            'fields': ('features', 'payment_details', 'is_installment_available', 'is_presale')
        }),
    )

    readonly_fields = ['area_dimension_text', 'created_at', 'updated_at']

    # Custom styling for JSONFields can be added here later using custom widgets