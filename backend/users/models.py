from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.db import models

class UserManager(DefaultUserManager):
    def create_user(self, email=None, phone_number=None, password=None, full_name="", **extra_fields):
        if not email and not phone_number:
            raise ValueError("Either an email or a phone number must be set.")
        
        if email:
            email = self.normalize_email(email)

        user = self.model(email=email, phone_number=phone_number, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, phone_number=None, full_name="Admin User", **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not email:
            email = "admin@estate.com"

        return self.create_user(email=email, phone_number=phone_number, password=password, full_name=full_name, **extra_fields)

class User(AbstractUser):
    username = None  # Remove default username field
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=17, unique=True, null=True, blank=True)
    
    full_name = models.CharField(max_length=255, blank=True)
    profile_picture = models.URLField(max_length=500, blank=True, null=True)
    
    is_verified_landlord = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    ban_reason = models.TextField(blank=True, null=True)

    saved_listings = models.ManyToManyField('listings.Listing', blank=True, related_name='favorited_by')
    settings = models.JSONField(default=dict, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # Email is now the primary login identifier for admin/CLI
    REQUIRED_FIELDS = []

    @property
    def display_name(self):
        return self.full_name if self.full_name else (self.email or self.phone_number)

    def __str__(self):
        identifier = self.email or self.phone_number
        return f"{self.display_name} ({identifier})"