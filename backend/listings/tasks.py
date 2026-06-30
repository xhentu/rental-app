# listings/tasks.py
from celery import shared_task
from django.core.cache import cache
from django.utils import timezone
from .models import Listing
from .serializers import ListingFeedSerializer

@shared_task(name="listings.tasks.update_public_feed_cache")
def update_public_feed_cache():
    """
    Background worker that runs dynamically to build the ideal 20-item front-page feed.
    Fills gaps seamlessly if boosted or ordinary pools run low, storing results directly in Redis.
    """
    now = timezone.now()
    
    # Absolute visibility conditions for safe public ingestion
    base_query = Listing.objects.filter(
        is_active=True,
        is_deleted=False,
        is_completed=False,
        expiry_date__gt=now
    ).select_related('landlord').prefetch_related('images').order_by('-created_at')

    # 1. Target ideal allocation cap of 12 boosted items (60%)
    boosted_pool = list(base_query.filter(is_boosted=True)[:12])
    boosted_count = len(boosted_pool)
    
    # 2. Compute dynamic remainder space to meet hard target metric of 20 elements
    needed_ordinary = max(0, 20 - boosted_count)
    ordinary_pool = list(base_query.filter(is_boosted=False)[:needed_ordinary])
    ordinary_count = len(ordinary_pool)
    
    # 3. Vice-Versa Balancing Flow
    # If ordinary items are sparse but we have overflow boosted items, fill the remaining gap
    current_total = boosted_count + ordinary_count
    if current_total < 20 and boosted_count == 12:
        extra_boosted_needed = 20 - current_total
        extra_boosted = list(base_query.filter(is_boosted=True)[12:12 + extra_boosted_needed])
        boosted_pool.extend(extra_boosted)

    # 4. Construct unified matrix and clamp hard to exactly 20 items max
    final_mix = boosted_pool + ordinary_pool
    final_mix = final_mix[:20]

    # 5. Serialize data structure and push directly to Redis Database 1 RAM
    serializer = ListingFeedSerializer(final_mix, many=True)
    cache.set("public_first_page_feed", serializer.data, timeout=86400)  # Safe 24-hour retention
    
    return f"Cache built successfully. Served mix total: {len(final_mix)} items."


@shared_task(name="deactivate_expired_listings")
def auto_deactivate_expired_listings():
    """
    Your original Janitor task, updated to instantly refresh the Redis cache 
    if any active listings are taken down.
    """
    now = timezone.now()
    expired_listings = Listing.objects.filter(
        is_active=True, 
        expiry_date__lte=now
    )
    count = expired_listings.count()
    expired_listings.update(is_active=False)
    
    # 🌟 The Upgrade: Force refresh the feed cache since listings just changed state
    if count > 0:
        update_public_feed_cache.delay()
        
    return f"🧹 Janitor: Deactivated {count} listings at {now}"