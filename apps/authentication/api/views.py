from django.http import HttpResponse
from rest_framework.generics import CreateAPIView

from ..models import User
from .serializers import RegistrationSerializer


class RegistrationAPIView(CreateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return RegistrationSerializer
        return RegistrationSerializer
