from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # List view columns
    list_display = ('email', 'phone_number', 'full_name_display', 'is_verified_landlord', 'is_banned')
    list_filter = ('is_verified_landlord', 'is_banned', 'date_joined')
    search_fields = ('email', 'phone_number', 'firebase_uid', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    # Display full name in the list view for convenience
    def full_name_display(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name_display.short_description = 'User Name'

    fieldsets = (
        ('System Anchor', {'fields': ('firebase_uid', 'password')}),
        ('Contact Info', {'fields': ('email', 'phone_number')}),
        ('Profile', {'fields': ('first_name', 'last_name', 'profile_picture', 'settings')}),
        ('Management', {
            'fields': ('is_verified_landlord', 'is_banned', 'ban_reason'),
            'classes': ('collapse',), # Hide by default to keep it clean
        }),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    readonly_fields = ('firebase_uid', 'last_login', 'date_joined')