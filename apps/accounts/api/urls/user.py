from django.urls import path

from ..views.user import InventoryAPIView


urlpatterns = [
    path('inventory/', InventoryAPIView.as_view(), name='token_pair')
]
