from django.urls import path, include


app_name = 'core'

urlpatterns = [
    path('', include('apps.accounts.urls', namespace='auth')),
    path('ingredients/', include('apps.ingredients.urls', namespace='ingredients'))
]
