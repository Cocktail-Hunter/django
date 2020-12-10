from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Ingredient
from .serializers import IngredientSerializer


class IngredientAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Ingredient.objects.all()

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return IngredientSerializer
        return IngredientSerializer
