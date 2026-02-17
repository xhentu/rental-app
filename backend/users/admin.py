from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 1. Columns to show in the main table list
    list_display = (
        'email', 
        'phone_number', 
        'first_name', 
        'last_name', 
        'is_verified_landlord', 
        'is_banned', 
        'date_joined'
    )
    
    # 2. Sidebar filters for quick management
    list_filter = (
        'is_verified_landlord', 
        'is_banned', 
        'is_staff', 
        'date_joined'
    )
    
    # 3. Powerful search (Search by UID, Email, or Name)
    search_fields = (
        'email', 
        'phone_number', 
        'firebase_uid', 
        'first_name', 
        'last_name'
    )
    
    # 4. Organizing the detail page (When you click a user)
    fieldsets = (
        (None, {'fields': ('firebase_uid', 'email', 'phone_number', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'profile_picture')}),
        ('Status & Monetization', {
            'fields': ('is_verified_landlord', 'is_banned', 'ban_reason'),
            'description': 'Manage VIP status and security bans here.'
        }),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # 5. Safety: Make system IDs read-only so you don't accidentally break the Firebase link
    readonly_fields = ('firebase_uid', 'last_login', 'date_joined')
    
    # Default sorting (Newest users first)
    ordering = ('-date_joined',)