from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    # Controls columns displayed in the user list view
    list_display = (
        'email', 
        'phone_number', 
        'full_name', 
        'is_verified_landlord', 
        'is_banned', 
        'is_staff'
    )
    
    # Adds clickable filters on the right sidebar
    list_filter = (
        'is_verified_landlord', 
        'is_banned', 
        'is_staff', 
        'is_superuser', 
        'is_active'
    )
    
    # Search box functionality
    search_fields = ('email', 'phone_number', 'full_name')
    
    # Default ordering in the admin list
    ordering = ('-date_joined',)

    # Groups fields logically inside the detail/edit form view
    fieldsets = (
        (None, {
            'fields': ('email', 'phone_number', 'password')
        }),
        ('Personal Info', {
            'fields': ('full_name', 'profile_picture')
        }),
        ('Status & Security', {
            'fields': ('is_verified_landlord', 'is_banned', 'ban_reason')
        }),
        ('App Preferences', {
            'fields': ('saved_listings', 'settings'),
            'classes': ('collapse',)  # Keeps advanced JSON/relation fields collapsed by default
        }),
        ('Permissions & Roles', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

    # Fields that should be read-only in the admin panel
    readonly_fields = ('last_login', 'date_joined')