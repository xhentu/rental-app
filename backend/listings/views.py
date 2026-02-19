from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Listing

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