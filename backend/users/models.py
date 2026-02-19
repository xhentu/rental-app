from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.db import models
from firebase_admin import auth as firebase_admin_auth

class UserManager(DefaultUserManager):
    def create_user(self, firebase_uid, email=None, password=None, **extra_fields):
        if not firebase_uid:
            raise ValueError("The Firebase UID must be set")
        email = self.normalize_email(email)
        # Map firebase_uid to username for AbstractUser internal logic
        extra_fields.setdefault('username', firebase_uid) 
        user = self.model(firebase_uid=firebase_uid, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, firebase_uid, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(firebase_uid, email, password, **extra_fields)

class User(AbstractUser):
    """
    Custom User Model for a Rental Estate App.
    Supports multi-method login (Google, Email, Phone) via Firebase.
    Allows duplicate names by using firebase_uid as the unique anchor.
    """
    objects = UserManager()
    # --- System Identifiers ---
    # firebase_uid is our 'Source of Truth'. 
    # db_index=True makes lookups lightning fast.
    firebase_uid = models.CharField(max_length=128, unique=True, db_index=True)
    
    # Login identifiers (Firebase links these together for us)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=17, unique=True, null=True, blank=True)
    
    # --- Profile Data ---
    profile_picture = models.URLField(max_length=500, blank=True, null=True)
    
    # --- Relationships (Tenant/Landlord logic) ---
    # Favorite Listings: Using a string 'listings.Listing' to avoid circular imports.
    # This creates a bridge table in Postgres: perfect for performance.
    saved_listings = models.ManyToManyField(
        'listings.Listing', 
        blank=True, 
        related_name='favorited_by'
    )

    # --- Modern Extensibility ---
    # JSONB field for app settings (Dark mode, Language, Notifications).
    # Since you're using Postgres, this is very efficient.
    settings = models.JSONField(default=dict, blank=True)

    # --- Status & Security ---
    is_verified_landlord = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    ban_reason = models.TextField(blank=True, null=True)

    # Django Settings
    USERNAME_FIELD = 'firebase_uid' 
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        # 1. Sync internal Django username
        if not self.username:
            self.username = self.firebase_uid

        # 2. Automated Firebase Ban/Release Logic
        if self.pk:
            try:
                # Get the current status from the DB before the save
                old_instance = User.objects.get(pk=self.pk)
                
                # CASE: Newly Banned
                if self.is_banned and not old_instance.is_banned:
                    firebase_admin_auth.update_user(self.firebase_uid, disabled=True)
                    firebase_admin_auth.revoke_refresh_tokens(self.firebase_uid)
                    print(f"✅ User {self.firebase_uid} DISABLED in Firebase.")
                
                # CASE: Unbanned (Released)
                elif not self.is_banned and old_instance.is_banned:
                    firebase_admin_auth.update_user(self.firebase_uid, disabled=False)
                    print(f"✅ User {self.firebase_uid} RE-ENABLED in Firebase.")

            except Exception as e:
                # We don't want to crash the save if Firebase is unreachable
                print(f"⚠️ Firebase Sync Error: {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (@{self.firebase_uid})"
