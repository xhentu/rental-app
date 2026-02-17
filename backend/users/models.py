from django.contrib.auth.models import AbstractUser
from django.db import models
from firebase_admin import auth as firebase_admin_auth

class User(AbstractUser):
    # --- System Identifiers ---
    # We use firebase_uid as the unique 'username' to allow many 'John Does'
    firebase_uid = models.CharField(max_length=128, unique=True, db_index=True)
    
    # Login methods (Firebase handles the connection between these)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=17, unique=True, null=True, blank=True)
    
    # --- Profile Data ---
    profile_picture = models.URLField(max_length=500, blank=True, null=True)
    # first_name and last_name are already in AbstractUser

    # --- Status & Security ---
    is_verified_landlord = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    ban_reason = models.TextField(blank=True, null=True)

    # Django technicalities
    USERNAME_FIELD = 'firebase_uid' # The internal unique ID
    REQUIRED_FIELDS = ['email']      # For creating superusers

    def save(self, *args, **kwargs):
        # Sync Ban Status to Firebase
        if self.pk:
            try:
                # Check if is_banned was just flipped to True
                old_instance = User.objects.get(pk=self.pk)
                if self.is_banned and not old_instance.is_banned:
                    firebase_admin_auth.update_user(self.firebase_uid, disabled=True)
                    firebase_admin_auth.revoke_refresh_tokens(self.firebase_uid)
            except Exception as e:
                print(f"Firebase Sync Error: {e}")
        
        # Ensure 'username' matches 'firebase_uid' for Django's internal checks
        if not self.username:
            self.username = self.firebase_uid
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email or self.phone_number})"