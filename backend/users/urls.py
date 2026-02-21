from django.urls import path, include
from .views import RegisterView, LoginView
# from .views import FirebaseSyncView

urlpatterns = [
    # Full path becomes: http://127.0.0.1:8000/api/users/sync/
    # Hit this first. If 404, redirect user to registration.
    path('login/', LoginView.as_view(), name='login'),
    
    # Hit this only for new accounts.
    path('register/', RegisterView.as_view(), name='register'),

]