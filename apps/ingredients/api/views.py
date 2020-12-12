import json
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
        queryset = Ingredient.objects.all()
        user = self.request.user

        if not user.is_authenticated:
            queryset = queryset.exclude(
                ~Q(state=IngredientState.APPROVED) |
                Q(public=False)
            )
        else:
            if not user.is_admin:
                queryset = queryset.exclude(
                    ~Q(added_by__id=user.id) &
                    (~Q(state=IngredientState.APPROVED) | Q(state=False))
                )

        state = self.request.query_params.get('type')
        public = self.request.query_params.get('public')

        if state is not None:
            if not isinstance(state, int):
                states = IngredientState.names
                if state.upper() in states:
                    state = states.index(state.upper())

            queryset = queryset.exclude(
                ~Q(state=state)
            )

        if public is not None:
            public = json.loads(public)
            queryset = queryset.exclude(
                ~Q(public=public)
            )

        return queryset
