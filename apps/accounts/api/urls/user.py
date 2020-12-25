from django.urls import path

from ..views.user import InventoryAPIView, UserRetrieveAPIView


urlpatterns = [
    path('inventory/', InventoryAPIView.as_view(), name='inventory'),
    path('', UserRetrieveAPIView.as_view(), name='user')
]
