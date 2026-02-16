""" this second models.py is created to look models with some color for visual and it might be harder 
in plain text , nothing but a comparisim"""

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # 1. The Anchor: This is the UNIQUE 'username' in Django's backend
    # We store the Firebase UID here.
    firebase_uid = models.CharField(max_length=128, unique=True, db_index=True)
    
    # 2. Identifiers
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    
    # 3. Display Data (Can be non-unique)
    profile_picture = models.URLField(max_length=500, blank=True, null=True)
    
    # 4. Status & Monetization
    is_verified = models.BooleanField(default=False) # VIP / Trusted Landlord
    is_banned = models.BooleanField(default=False)   # Security / Scam prevention
    
    # We clear the password field since Firebase handles it
    password = models.CharField(max_length=128, blank=True, null=True)

    # Tell Django to use email for certain lookups if preferred
    REQUIRED_FIELDS = ['firebase_uid'] 

    def __str__(self):
        return f"{self.first_name} {self.last_name} (@{self.firebase_uid})"

class User(AbstractUser):
    # This is the unique system ID (e.g., "AIzaSy...") 
    # By setting this as the 'username', we allow 'first_name' to be anything.
    username = models.CharField(max_length=128, unique=True) 
    firebase_uid = models.CharField(max_length=128, unique=True, db_index=True)
    
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.URLField(max_length=500, blank=True, null=True)

    # Monetization & Security
    is_verified_landlord = models.BooleanField(default=False) # VIP
    is_banned = models.BooleanField(default=False)
    ban_reason = models.TextField(blank=True, null=True) # Good for support tickets

    # Django requires a password field, but we leave it blank/unused
    password = models.CharField(max_length=128, blank=True, null=True)

    USERNAME_FIELD = 'email' # Allows logging in via email in Admin panel
    REQUIRED_FIELDS = ['username', 'firebase_uid']

    def __str__(self):
        # This allows multiple "John Does" to exist while you see their ID
        return f"{self.first_name} {self.last_name} ({self.email})"

from django.contrib.auth.models import AbstractUser
from django.db import models
from firebase_admin import auth as firebase_auth

class User(AbstractUser):
    # System identification
    firebase_uid = models.CharField(max_length=128, unique=True, db_index=True)
    
    # Base Django 'username' will store the firebase_uid to allow 
    # many users with the same First/Last name (Display Name)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.URLField(max_length=500, blank=True, null=True)

    # Monetization & Security
    is_verified_landlord = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    ban_reason = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'firebase_uid']

    def save(self, *args, **kwargs):
        # Logic: If user is banned in Django, disable them in Firebase too
        if self.pk: # Only check if user already exists
            old_user = User.objects.get(pk=self.pk)
            if self.is_banned and not old_user.is_banned:
                try:
                    firebase_auth.update_user(self.firebase_uid, disabled=True)
                    firebase_auth.revoke_refresh_tokens(self.firebase_uid)
                except Exception as e:
                    print(f"Firebase ban sync failed: {e}")
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (@{self.email})"