import json
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from ..models import Ingredient, IngredientState
from .serializers import IngredientSerializer


class IngredientAPIView(ListCreateAPIView):
    '''
    ## GET Request

    GET requests will return a list of all available ingredients that are public.
    If user is authenticated, the user will be able to view all their own private
    ingredients as well.

    If user is admin, the user will be able to view everyone's ingredients, including
    private ones.

    This endpoint takes 2 optional parameters to filter the data returned:

    - state (PENDING, 0) | (APPROVED, 1) | (DENIED, 2)
    - public Boolean

    ## POST Request

    POST requests will add a new ingredient to the database and only if the user
    is authenticated. Otherwise, the user will receive 401 Unauthorized.

    The request body should contain 2 key values:

    - name : String
    - public : Boolean

    All public ingredients are automatically given the state (PENDING, 0) and
    all private ingredients are automatically given the state (APPROVED, 1)
    '''
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

        state = self.request.query_params.get('state')
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


class IngredientUpdateAPIView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return IngredientSerializer
        return IngredientSerializers
