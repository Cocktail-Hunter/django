from django.db.models import Q
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models import Ingredient, IngredientState
from .serializers import IngredientSerializer


class IngredientAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return IngredientSerializer
        return IngredientSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Ingredient.objects.filter(
            Q(added_by__id=user.id) |
            Q(public=True),
            # and
            Q(added_by__id=user.id) |
            Q(state=IngredientState.APPROVED)
        )
        return queryset
