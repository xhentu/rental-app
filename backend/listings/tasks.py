from celery import shared_task
from django.utils import timezone
from .models import Listing

@shared_task(name="deactivate_expired_listings")
def auto_deactivate_expired_listings():
    now = timezone.now()
    # Find active listings where expiry_date is in the past
    expired_listings = Listing.objects.filter(
        is_active=True, 
        expiry_date__lte=now
    )
    count = expired_listings.count()
    expired_listings.update(is_active=False)
    
    return f"🧹 Janitor: Deactivated {count} listings at {now}"