from django.urls import path, include


app_name = 'accounts'

urlpatterns = [
    path('auth/', include('apps.accounts.api.urls.auth')),
    path('user/', include('apps.accounts.api.urls.user')),
]
