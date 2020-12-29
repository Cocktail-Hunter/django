from django.urls import path

from .views import CocktailAPIView, CocktailsAddAPIView, CocktailDetailUpdateAPIView

urlpatterns = [
    path('', CocktailAPIView.as_view(), name='cocktails-list'),
    path('add/', CocktailsAddAPIView.as_view(), name='cocktails-add'),
    path(
        '<pk>/',
        CocktailDetailUpdateAPIView.as_view(),
        name='cocktails-detail-update'
    ),
]
