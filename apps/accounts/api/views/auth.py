from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenRefreshView

from ...models import User
from ..serializers.auth import RegistrationSerializer, CustomTokenRefreshSerializer


class RegistrationAPIView(CreateAPIView):
    '''
    Takes a set of user credentials (username, email and password) to register a
    new user and returns the user's username, email as well as a tokens object
    containing JSON web token pair.
    '''
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return RegistrationSerializer
        return RegistrationSerializer


class CustomTokenRefreshView(TokenRefreshView):
    '''
    Refresh token generator view.
    '''
    serializer_class = CustomTokenRefreshSerializer
