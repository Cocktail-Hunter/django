from django.urls import path, include


app_name = 'version1'
urlpatterns = [
    path('auth/', include('apps.authentication.urls')),
    path('ingredients/', include('apps.ingredients.urls'))
]
