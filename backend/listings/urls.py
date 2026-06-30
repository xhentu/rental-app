# listings/urls.py
from django.urls import path
from .views import (
    ListingListView,
    ListingDetailView,
    ListingCreateView,
    ToggleFavoriteView
)

urlpatterns = [
    # 1. Public Feed API (Optimized for bandwidth/fast scrolling using ListingFeedSerializer)
    # URL: GET /api/listings/
    path('', ListingListView.as_view(), name='listing-list'),
    
    # 2. Detail View API (Pulls full heavy fields using ListingDetailSerializer)
    # URL: GET /api/listings/<id>/
    path('<int:pk>/', ListingDetailView.as_view(), name='listing-detail'),
    
    # 3. Listing Creation Pipeline (Authenticated only)
    # URL: POST /api/listings/create/
    path('create/', ListingCreateView.as_view(), name='listing-create'),
    
    # 4. Toggle Saved/Favorites System (Authenticated only)
    # URL: POST /api/listings/<id>/favorite/
    path('<int:pk>/favorite/', ToggleFavoriteView.as_view(), name='listing-favorite'),
]