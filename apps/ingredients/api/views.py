from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from ..models import Ingredient
from .serializers import AddIngredientSerializer


class AddIngredientAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return AddIngredientSerializer
        return AddIngredientSerializer
