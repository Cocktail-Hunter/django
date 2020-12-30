from django.urls import path

from ..views.user import InventoryAPIView, UserRetrieveAPIView, UserPasswordUpdateAPIView


urlpatterns = [
    path('inventory/', InventoryAPIView.as_view(), name='inventory'),
    path('', UserRetrieveAPIView.as_view(), name='user'),
    path(
        'change-password/',
        UserPasswordUpdateAPIView.as_view(),
        name='update-password'
    ),
]
