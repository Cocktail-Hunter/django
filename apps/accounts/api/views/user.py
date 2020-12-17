from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from ...models import User
from ..serializers.user import InventorySerializer


class InventoryAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return InventorySerializer
        return InventorySerializer

    def get_object(self):
        return self.request.user
