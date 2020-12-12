from django.urls import path, include


app_name = 'core'

urlpatterns = [
    path('auth/', include('apps.authentication.urls')),
    path('ingredients/', include('apps.ingredients.urls'))
]
