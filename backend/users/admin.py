from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 1. Update list_display: replaced display_name with full_name for clarity
    list_display = ('firebase_uid', 'email', 'full_name', 'is_verified_landlord', 'is_banned', 'last_login')
    list_filter = ('is_verified_landlord', 'is_banned', 'is_staff', 'date_joined')
    
    # 2. Update search_fields: removed first_name and last_name
    search_fields = ('email', 'phone_number', 'firebase_uid', 'full_name')
    ordering = ('-date_joined',)

    # 3. Update fieldsets: this is where the layout of the "Edit User" page is defined
    fieldsets = (
        ('System Anchor', {
            'fields': ('firebase_uid', 'password'),
            'description': 'Unique identifier from Firebase and internal Django hash.'
        }),
        ('Contact Info', {'fields': ('email', 'phone_number')}),
        ('Profile', {'fields': ('full_name', 'profile_picture', 'settings')}), # ✅ Swapped here
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

    # 4. Read-only fields remain the same
    readonly_fields = ('firebase_uid', 'last_login', 'date_joined')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'settings' in form.base_fields:
            form.base_fields['settings'].widget.attrs['rows'] = 5
        return form