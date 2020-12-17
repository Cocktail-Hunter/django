from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from ..views.auth import RegistrationAPIView


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegistrationAPIView.as_view(), name='register')
]
