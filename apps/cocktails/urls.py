from django.urls import path, include


app_name = 'cocktails'

urlpatterns = [
    path('', include('apps.cocktails.api.urls'), name='cocktails-urls')
]
