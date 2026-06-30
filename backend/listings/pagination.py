# listings/pagination.py
from rest_framework.pagination import CursorPagination

class ListingCursorPagination(CursorPagination):
    # Sends exactly 20 items per scroll event to match your layout strategy
    page_size = 20  
    
    # Sorts everything universally by time when fetching from the database
    ordering = '-created_at'  
    
    # The URL parameter key Flutter will look for (e.g., ?cursor=XYZ)
    cursor_query_param = 'cursor'