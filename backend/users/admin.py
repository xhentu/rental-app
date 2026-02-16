from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import User

# This makes your custom fields (firebase_uid, etc.) visible in Admin
class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('firebase_uid', 'phone_number', 'is_landlord')}),
    )

admin.site.register(User, CustomUserAdmin)