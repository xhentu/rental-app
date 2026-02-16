from django.urls import path
from .views import FirebaseSyncView

urlpatterns = [
    # Full path becomes: http://127.0.0.1:8000/api/users/sync/
    path('sync/', FirebaseSyncView.as_view(), name='firebase_sync'),
]