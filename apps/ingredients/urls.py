from django.urls import path, include


app_name = 'ingredients'

urlpatterns = [
    path('', include('apps.ingredients.api.urls'), name='ingredients-urls')
]
