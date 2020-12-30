from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from ..views.auth import RegistrationAPIView, CustomTokenRefreshView


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_pair'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegistrationAPIView.as_view(), name='register')
]
