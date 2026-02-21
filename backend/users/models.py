from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.db import models
from firebase_admin import auth as firebase_admin_auth

class UserManager(DefaultUserManager):
    def create_user(self, firebase_uid, email=None, password=None, **extra_fields):
        if not firebase_uid:
            raise ValueError("The Firebase UID must be set")
        email = self.normalize_email(email) if email else None
        extra_fields.setdefault('username', firebase_uid) 
        user = self.model(firebase_uid=firebase_uid, email=email, **extra_fields)
        user.set_password(password) # Still sets a dummy password for Django compatibility
        user.save(using=self._db)
        return user

    def create_superuser(self, firebase_uid, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # Superusers need an email usually for admin notifications
        return self.create_user(firebase_uid, email, password, **extra_fields)

class User(AbstractUser):
    objects = UserManager()

    # --- System Identifiers ---
    firebase_uid = models.CharField(max_length=128, unique=True, db_index=True)
    
    # We allow null/blank so phone-only users don't crash the 'unique' check
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=17, unique=True, null=True, blank=True)
    
    # --- Profile Data ---
    profile_picture = models.URLField(max_length=500, blank=True, null=True)
    
    # --- Relationships ---
    saved_listings = models.ManyToManyField(
        'listings.Listing', 
        blank=True, 
        related_name='favorited_by'
    )

    # --- Modern Extensibility ---
    settings = models.JSONField(default=dict, blank=True)

    # --- Status & Security ---
    is_verified_landlord = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    ban_reason = models.TextField(blank=True, null=True)

    # Django Settings
    USERNAME_FIELD = 'firebase_uid' 
    REQUIRED_FIELDS = ['email'] # Only used when creating superuser via CLI

    @property
    def display_name(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.firebase_uid

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.firebase_uid

        # Handle Firebase Banning Logic
        if self.pk:
            try:
                old_instance = User.objects.get(pk=self.pk)
                if self.is_banned and not old_instance.is_banned:
                    firebase_admin_auth.update_user(self.firebase_uid, disabled=True)
                    firebase_admin_auth.revoke_refresh_tokens(self.firebase_uid)
                    print(f"🚫 User {self.firebase_uid} DISABLED in Firebase.")
                elif not self.is_banned and old_instance.is_banned:
                    firebase_admin_auth.update_user(self.firebase_uid, disabled=False)
                    print(f"✅ User {self.firebase_uid} RE-ENABLED in Firebase.")
            except Exception as e:
                print(f"⚠️ Firebase Sync Error: {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.display_name} (@{self.firebase_uid})"