from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404 
from .models import Listing
from .serializers import ListingFeedSerializer, ListingDetailSerializer

class ToggleFavoriteView(APIView):
    """
    Endpoint for Tenants to Save/Unsave a listing.
    URL: /api/listings/<id>/favorite/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        listing = get_object_or_404(Listing, pk=pk)

        if listing in user.saved_listings.all():
            user.saved_listings.remove(listing)
            return Response({"message": "Removed from favorites", "is_favorite": False})
        else:
            user.saved_listings.add(listing)
            return Response({"message": "Added to favorites", "is_favorite": True})

class ListingListView(generics.ListAPIView):
    """
    The 'Feed' - Publicly accessible, optimized for the Celeron/Bandwidth.
    """
    queryset = Listing.objects.filter(is_active=True).select_related('landlord')
    serializer_class = ListingFeedSerializer
    permission_classes = [permissions.AllowAny]
    
    # Adding search and filter capabilities
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['township', 'offer_type', 'property_type', 'owner_direct']
    search_fields = ['title', 'township', 'region']
    ordering_fields = ['price', 'created_at']

class ListingDetailView(generics.RetrieveAPIView):
    """
    The 'Details' - Full info for a single listing.
    """
    queryset = Listing.objects.filter(is_active=True)
    serializer_class = ListingDetailSerializer
    permission_classes = [permissions.AllowAny]

class ListingCreateView(generics.CreateAPIView):
    """
    The 'Creation' - Authenticated only.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Attach the landlord automatically from the Firebase/Django user
        serializer.save(landlord=self.request.user)