from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # We use the 'display_name' property we defined in the Model
    list_display = ('firebase_uid', 'email', 'display_name', 'is_verified_landlord', 'is_banned', 'last_login')
    list_filter = ('is_verified_landlord', 'is_banned', 'is_staff', 'date_joined')
    search_fields = ('email', 'phone_number', 'firebase_uid', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    # Organizes the detail page into clear sections
    fieldsets = (
        ('System Anchor', {
            'fields': ('firebase_uid', 'password'),
            'description': 'Unique identifier from Firebase and internal Django hash.'
        }),
        ('Contact Info', {'fields': ('email', 'phone_number')}),
        ('Profile', {'fields': ('first_name', 'last_name', 'profile_picture', 'settings')}),
        ('Status & Verification', {
            'fields': ('is_verified_landlord', 'is_banned', 'ban_reason'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',),
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
        }),
    )

    # These fields cannot be edited in the UI
    readonly_fields = ('firebase_uid', 'last_login', 'date_joined')

    # This makes the "settings" JSON look a bit better in the admin
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'settings' in form.base_fields:
            form.base_fields['settings'].widget.attrs['rows'] = 5
        return form