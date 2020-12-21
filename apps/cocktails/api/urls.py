from django.urls import path

from .views import CocktailAPIView

urlpatterns = [
    path('', CocktailAPIView.as_view(), name='cocktails-list-add')
]
