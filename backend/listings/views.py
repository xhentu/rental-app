import json
import time

from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import ListingFilter
from .models import Listing
from .pagination import ListingCursorPagination
from .serializers import ListingDetailSerializer, ListingFeedSerializer
from .tasks import update_public_feed_cache


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
    The 'Feed' - Publicly accessible, optimized for database performance and bandwidth.
    - Serves page 1 directly from Redis RAM for lightning-fast speeds.
    - Falls back to indexed PostgreSQL Cursor Pagination for infinite scrolls, searches, and deep filters.
    """
    queryset = Listing.objects.filter(
        is_active=True,
        is_deleted=False,
        is_completed=False
    ).select_related('landlord').prefetch_related('images')
    
    serializer_class = ListingFeedSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = ListingCursorPagination  # 🌟 UPGRADE: Stops database-killing offset calculations
    
    # Advanced search and filtering capabilities integration
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ListingFilter             # 🌟 UPGRADE: Points to your custom advanced GIN filter maps
    search_fields = ['title', 'township', 'region', 'road', 'remark']

    def list(self, request, *args, **kwargs):
        # 1. Detect query parameters to determine what the user is doing
        has_cursor = request.query_params.get('cursor') is not None
        
        # Check if the user is currently applying any query filter strings
        filter_keys = [
            'township', 'region', 'offer_type', 'property_type', 'hostel_type', 
            'owner_direct', 'installment_available', 'is_presale', 'min_price', 
            'max_price', 'search', 'aircon', 'fully_repaired', 'master_bed'
        ]
        has_filters = any(param in request.query_params for param in filter_keys)
        
        # Pull-to-refresh implementation flag
        force_refresh = request.query_params.get('force_refresh', 'false').lower() == 'true'
        if force_refresh:
            update_public_feed_cache.delay()

        # 2. Redis RAM Cache Shield: If it's a clean initial Page 1 load, pull directly from memory
        if not has_cursor and not has_filters:
            cached_data = cache.get("public_first_page_feed")
            if cached_data is not None:
                time.sleep(2)
                return Response({
                    "next": self._calculate_safe_next_cursor(),
                    "previous": None,
                    "results": cached_data
                }, status=status.HTTP_200_OK)
        
        print("⏳ Simulating network delay for pagination testing...")
        time.sleep(2)

        # 3. Fallback: If user is filtering or scrolling past page 1, hit PostgreSQL using indexes
        return super().list(request, *args, **kwargs)

    def _calculate_safe_next_cursor(self):
        """
        Calculates if a second page of records exists and encodes a safe timeline cursor link.
        """
        try:
            active_qs = Listing.objects.filter(is_active=True, is_deleted=False, is_completed=False)
            total_records = active_qs.count()
            
            # If the DB has 20 or fewer rows total, everything fits on page 1. No page 2 exists!
            if total_records <= 20:
                return None
                
            # Safely extract the 20th item to act as our time anchor point
            target_instance = active_qs.order_by('-created_at')[19:20].get()
            
            paginator = self.paginator
            cursor = paginator.encode_cursor(paginator.cursor_class(instance=target_instance, reverse=False))
            return f"{self.request.build_absolute_uri(self.request.path)}?cursor={cursor}"
        except Exception:
            return None


class ListingDetailView(generics.RetrieveAPIView):
    """
    The 'Details' - Full data payload for a single property view page.
    """
    queryset = Listing.objects.filter(is_active=True, is_deleted=False).prefetch_related('images')
    serializer_class = ListingDetailSerializer
    permission_classes = [permissions.AllowAny]


class ListingCreateView(generics.CreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print("\n📥 ==================== DJANGO INBOUND REQUEST ====================")
        print(f"👤 USER: {request.user} (ID: {request.user.id})")
        
        print("📄 RAW POST DATA STRINGS:")
        for key, value in request.data.items():
            if key in ['floor_data', 'room_structure', 'features', 'landmarks', 'active_buttons']:
                try:
                    print(f"   🔹 {key}: {json.loads(value)}")
                except Exception:
                    print(f"   🔹 {key} (Raw JSON string parse error): {value}")
            else:
                print(f"   🔹 {key}: {value}")
                
        print(f"🖼️  RAW UPLOADED FILES: {request.FILES.getlist('uploaded_images')}")
        print("==================================================================\n")
        
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        instance = serializer.save(landlord=self.request.user)
        
        print("\n💾 ==================== POSTGRESQL DATABASE SAVED ====================")
        print(f"✅ LISTING ID INSTANCE CREATED: {instance.id}")
        print(f"📌 TITLE: {instance.title}")
        print(f"📌 AREA TEXT GENERATED: {instance.area_dimension_text}")
        print(f"📌 EXPIRY DATE SET: {instance.expiry_date}")
        
        print(f"📊 SAVED FLOOR DATA: {instance.floor_data}")
        print(f"📊 SAVED ROOM STRUCTURE: {instance.room_structure}")
        print(f"📊 SAVED FEATURES MAP: {instance.features}")
        print("======================================================================\n")
        
        # 🌟 UPGRADE: Whenever a landlord creates a brand new post, immediately trigger
        # a background cache rebuild so it pops onto the public front page instantly!
        update_public_feed_cache.delay()

# Old
# from django.shortcuts import get_object_or_404 
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import filters, generics, permissions, status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView

# import time

# from .models import Listing
# from .serializers import ListingDetailSerializer, ListingFeedSerializer
# from django.core.cache import cache
# from .serializers import ListingDetailSerializer, ListingFeedSerializer
# from .pagination import ListingCursorPagination  # 🌟 NEW: For time-coordinated scrolling
# from .filters import ListingFilter                # 🌟 NEW: For advanced GIN-indexed filtering
# from .tasks import update_public_feed_cache 


# class ToggleFavoriteView(APIView):
#     """
#     Endpoint for Tenants to Save/Unsave a listing.
#     URL: /api/listings/<id>/favorite/
#     """
#     permission_classes = [IsAuthenticated]

#     def post(self, request, pk):
#         user = request.user
#         listing = get_object_or_404(Listing, pk=pk)

#         if listing in user.saved_listings.all():
#             user.saved_listings.remove(listing)
#             return Response({"message": "Removed from favorites", "is_favorite": False})
#         else:
#             user.saved_listings.add(listing)
#             return Response({"message": "Added to favorites", "is_favorite": True})


# class ListingListView(generics.ListAPIView):
#     """
#     The 'Feed' - Publicly accessible, optimized for database performance and bandwidth.
#     """
#     # Optimized: select_related joins user data, prefetch_related caches images in a single batch query
#     queryset = Listing.objects.filter(is_active=True).select_related('landlord').prefetch_related('images')
#     serializer_class = ListingFeedSerializer  # Matches split class
#     permission_classes = [permissions.AllowAny]
    
#     # Adding search and filter capabilities
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['township', 'offer_type', 'property_type', 'owner_direct']
#     search_fields = ['title', 'township', 'region']
#     ordering_fields = ['price', 'created_at']


# class ListingDetailView(generics.RetrieveAPIView):
#     """
#     The 'Details' - Full data payload for a single property view page.
#     """
#     # Optimized: prefetch all related full resolution imagery for the detail page gallery
#     queryset = Listing.objects.filter(is_active=True).prefetch_related('images')
#     serializer_class = ListingDetailSerializer  # Matches split class
#     permission_classes = [permissions.AllowAny]


# # listings/views.py

# class ListingCreateView(generics.CreateAPIView):
#     queryset = Listing.objects.all()
#     serializer_class = ListingDetailSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         print("\n📥 ==================== DJANGO INBOUND REQUEST ====================")
#         print(f"👤 USER: {request.user} (ID: {request.user.id})")
        
#         # 1. Inspect raw POST fields text strings sent by Flutter Multipart request
#         print("📄 RAW POST DATA STRINGS:")
#         for key, value in request.data.items():
#             # If it's one of our encoded JSON fields, let's pretty print it
#             if key in ['floor_data', 'room_structure', 'features', 'landmarks', 'active_buttons']:
#                 try:
#                     print(f"   🔹 {key}: {json.loads(value)}")
#                 except:
#                     print(f"   🔹 {key} (Raw JSON string parse error): {value}")
#             else:
#                 print(f"   🔹 {key}: {value}")
                
#         # 2. Inspect raw file arrays caught by server memory
#         print(f"🖼️  RAW UPLOADED FILES: {request.FILES.getlist('uploaded_images')}")
#         print("==================================================================\n")
        
#         return super().create(request, *args, **kwargs)

#     def perform_create(self, serializer):
#         # This triggers model .save()
#         instance = serializer.save(landlord=self.request.user)
        
#         print("\n💾 ==================== POSTGRESQL DATABASE SAVED ====================")
#         print(f"✅ LISTING ID INSTANCE CREATED: {instance.id}")
#         print(f"📌 TITLE: {instance.title}")
#         print(f"📌 AREA TEXT GENERATED: {instance.area_dimension_text}")
#         print(f"📌 EXPIRY DATE SET: {instance.expiry_date}")
        
#         # Checking JSON data structures stored inside DB columns
#         print(f"📊 SAVED FLOOR DATA: {instance.floor_data}")
#         print(f"📊 SAVED ROOM STRUCTURE: {instance.room_structure}")
#         print(f"📊 SAVED FEATURES MAP: {instance.features}")
#         print("======================================================================\n")# listings/views.py
#      # 🌟 NEW: To handle background cache triggers


# class ToggleFavoriteView(APIView):
#     """
#     Endpoint for Tenants to Save/Unsave a listing.
#     URL: /api/listings/<id>/favorite/
#     """
#     permission_classes = [IsAuthenticated]

#     def post(self, request, pk):
#         user = request.user
#         listing = get_object_or_404(Listing, pk=pk)

#         if listing in user.saved_listings.all():
#             user.saved_listings.remove(listing)
#             return Response({"message": "Removed from favorites", "is_favorite": False})
#         else:
#             user.saved_listings.add(listing)
#             return Response({"message": "Added to favorites", "is_favorite": True})


# class ListingListView(generics.ListAPIView):
#     """
#     The 'Feed' - Publicly accessible, optimized for database performance and bandwidth.
#     - Serves page 1 directly from Redis RAM for lightning-fast speeds.
#     - Falls back to indexed PostgreSQL Cursor Pagination for infinite scrolls, searches, and deep filters.
#     """
#     queryset = Listing.objects.filter(
#         is_active=True,
#         is_deleted=False,
#         is_completed=False
#     ).select_related('landlord').prefetch_related('images')
    
#     serializer_class = ListingFeedSerializer
#     permission_classes = [permissions.AllowAny]
#     pagination_class = ListingCursorPagination  # 🌟 UPGRADE: Stops database-killing offset calculations
    
#     # Advanced search and filtering capabilities integration
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter]
#     filterset_class = ListingFilter             # 🌟 UPGRADE: Points to your custom advanced GIN filter maps
#     search_fields = ['title', 'township', 'region', 'road', 'remark']

#     def list(self, request, *args, **kwargs):
#         # 1. Detect query parameters to determine what the user is doing
#         has_cursor = request.query_params.get('cursor') is not None
        
#         # Check if the user is currently applying any query filter strings
#         filter_keys = [
#             'township', 'region', 'offer_type', 'property_type', 'hostel_type', 
#             'owner_direct', 'installment_available', 'is_presale', 'min_price', 
#             'max_price', 'search', 'aircon', 'fully_repaired', 'master_bed'
#         ]
#         has_filters = any(param in request.query_params for param in filter_keys)
        
#         # Pull-to-refresh implementation flag
#         force_refresh = request.query_params.get('force_refresh', 'false').lower() == 'true'
#         if force_refresh:
#             update_public_feed_cache.delay()

#         # 2. Redis RAM Cache Shield: If it's a clean initial Page 1 load, pull directly from memory
#         if not has_cursor and not has_filters:
#             cached_data = cache.get("public_first_page_feed")
#             if cached_data is not None:
#                 time.sleep(2)
#                 return Response({
#                     "next": self._calculate_safe_next_cursor(),
#                     "previous": None,
#                     "results": cached_data
#                 }, status=status.HTTP_200_OK)
        
#         print("⏳ Simulating network delay for pagination testing...")
#         time.sleep(2)

#         # 3. Fallback: If user is filtering or scrolling past page 1, hit PostgreSQL using indexes
#         return super().list(request, *args, **kwargs)

#     def _calculate_safe_next_cursor(self):
#         """
#         Calculates if a second page of records exists and encodes a safe timeline cursor link.
#         """
#         try:
#             active_qs = Listing.objects.filter(is_active=True, is_deleted=False, is_completed=False)
#             total_records = active_qs.count()
            
#             # If the DB has 20 or fewer rows total, everything fits on page 1. No page 2 exists!
#             if total_records <= 20:
#                 return None
                
#             # Safely extract the 20th item to act as our time anchor point
#             target_instance = active_qs.order_by('-created_at')[19:20].get()
            
#             paginator = self.paginator
#             cursor = paginator.encode_cursor(paginator.cursor_class(instance=target_instance, reverse=False))
#             return f"{self.request.build_absolute_uri(self.request.path)}?cursor={cursor}"
#         except Exception:
#             return None


# class ListingDetailView(generics.RetrieveAPIView):
#     """
#     The 'Details' - Full data payload for a single property view page.
#     """
#     queryset = Listing.objects.filter(is_active=True, is_deleted=False).prefetch_related('images')
#     serializer_class = ListingDetailSerializer
#     permission_classes = [permissions.AllowAny]


# class ListingCreateView(generics.CreateAPIView):
#     queryset = Listing.objects.all()
#     serializer_class = ListingDetailSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         print("\n📥 ==================== DJANGO INBOUND REQUEST ====================")
#         print(f"👤 USER: {request.user} (ID: {request.user.id})")
        
#         print("📄 RAW POST DATA STRINGS:")
#         for key, value in request.data.items():
#             if key in ['floor_data', 'room_structure', 'features', 'landmarks', 'active_buttons']:
#                 try:
#                     print(f"   🔹 {key}: {json.loads(value)}")
#                 except:
#                     print(f"   🔹 {key} (Raw JSON string parse error): {value}")
#             else:
#                 print(f"   🔹 {key}: {value}")
                
#         print(f"🖼️  RAW UPLOADED FILES: {request.FILES.getlist('uploaded_images')}")
#         print("==================================================================\n")
        
#         return super().create(request, *args, **kwargs)

#     def perform_create(self, serializer):
#         instance = serializer.save(landlord=self.request.user)
        
#         print("\n💾 ==================== POSTGRESQL DATABASE SAVED ====================")
#         print(f"✅ LISTING ID INSTANCE CREATED: {instance.id}")
#         print(f"📌 TITLE: {instance.title}")
#         print(f"📌 AREA TEXT GENERATED: {instance.area_dimension_text}")
#         print(f"📌 EXPIRY DATE SET: {instance.expiry_date}")
        
#         print(f"📊 SAVED FLOOR DATA: {instance.floor_data}")
#         print(f"📊 SAVED ROOM STRUCTURE: {instance.room_structure}")
#         print(f"📊 SAVED FEATURES MAP: {instance.features}")
#         print("======================================================================\n")
        
#         # 🌟 UPGRADE: Whenever a landlord creates a brand new post, immediately trigger
#         # a background cache rebuild so it pops onto the public front page instantly!
#         update_public_feed_cache.delay()

# just check it first, its listings.views.py and that's listings.urls.py below
# # listings/urls.py
# from django.urls import path
# from .views import (
#     ListingListView,
#     ListingDetailView,
#     ListingCreateView,
#     ToggleFavoriteView
# )

# urlpatterns = [
#     # 1. Public Feed API (Optimized for bandwidth/fast scrolling using ListingFeedSerializer)
#     # URL: GET /api/listings/
#     path('', ListingListView.as_view(), name='listing-list'),
    
#     # 2. Detail View API (Pulls full heavy fields using ListingDetailSerializer)
#     # URL: GET /api/listings/<id>/
#     path('<int:pk>/', ListingDetailView.as_view(), name='listing-detail'),
    
#     # 3. Listing Creation Pipeline (Authenticated only)
#     # URL: POST /api/listings/create/
#     path('create/', ListingCreateView.as_view(), name='listing-create'),
    
#     # 4. Toggle Saved/Favorites System (Authenticated only)
#     # URL: POST /api/listings/<id>/favorite/
#     path('<int:pk>/favorite/', ToggleFavoriteView.as_view(), name='listing-favorite'),
# ]