from django.urls import path

from .views import CocktailAPIView, CocktailsAddAPIView

urlpatterns = [
    path('', CocktailAPIView.as_view(), name='cocktails-list'),
    path('add/', CocktailsAddAPIView.as_view(), name='cocktails-add'),
]
