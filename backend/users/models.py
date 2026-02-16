from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # The bridge to Firebase
    firebase_uid = models.CharField(max_length=128, unique=True, db_index=True)
    
    # We use email as the primary identifier
    email = models.EmailField(unique=True)
    
    # Profile fields
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.URLField(max_length=500, blank=True, null=True)

    # We don't need Django to handle passwords
    password = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"