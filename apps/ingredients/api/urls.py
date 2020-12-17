from django.urls import path
from .views import IngredientAPIView, IngredientUpdateAPIView


urlpatterns = [
    path('', IngredientAPIView.as_view(), name='ingredients-list-add'),
    path('<pk>/', IngredientUpdateAPIView.as_view(), name='ingredients-update')
]
