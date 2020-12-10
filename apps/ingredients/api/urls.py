from django.urls import path
from .views import AddIngredientAPIView


urlpatterns = [
    path('add/', AddIngredientAPIView.as_view(), name='token_pair'),
]
