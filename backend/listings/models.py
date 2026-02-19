from django.db import models
from django.conf import settings

class Listing(models.Model):
    # --- Relationships ---
    # The Landlord/Owner. If the user is deleted, their listings are deleted.
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='owned_listings'
    )

    # --- Property Details ---
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    # Rental price per month
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # --- Location ---
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    # Using JSONB (Postgres) for Geo-coordinates [lat, lng]
    coordinates = models.JSONField(default=dict, blank=True)

    # --- Features ---
    bedrooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)
    is_available = models.BooleanField(default=True)
    
    # --- Media ---
    # We store the main image URL (usually from Firebase Storage)
    thumbnail = models.URLField(max_length=500, blank=True, null=True)

    # --- Timestamps ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - ${self.price}"