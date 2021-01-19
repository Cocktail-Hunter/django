import json
from django.db.models import Q, Count
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from ..models import Cocktail, CocktailState
from .serializers import CocktailSerializer
from apps.core.parsers import MultipartJsonParser
from apps.ingredients.models import Ingredient


class CocktailAPIView(ListAPIView):
    '''
    User must be authenticated to view this endpoint.
    This endpoint will return a list of all available cocktails that are public and/or
    private ones that the user has authored.

    If user is admin, the user will be able to view everyone's cocktails, including
    private ones.

    This endpoint takes 2 optional parameters to filter the data returned:

    - state (PENDING, 0) | (APPROVED, 1) | (DENIED, 2)
    - public Boolean

    The request body should contain 3 key values:

    - ingredients : Array<Integer>
    - flexibility : Integer
    - alcohol : Boolean
    '''
    permission_classes = (IsAuthenticated,)
    http_method_names = ('post', 'head', 'options')

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return CocktailSerializer
        return CocktailSerializer

    def get_queryset(self):
        queryset = Cocktail.objects.all()
        user = self.request.user

        if not user.is_authenticated:
            queryset = queryset.exclude(
                ~Q(state=CocktailState.APPROVED) |
                Q(public=False)
            )
        else:
            if not user.is_admin:
                queryset = queryset.exclude(
                    ~Q(author__id=user.id) &
                    (~Q(state=CocktailState.APPROVED) | Q(state=False))
                )

        state = self.request.query_params.get('state')
        public = self.request.query_params.get('public')

        if state is not None:
            if not isinstance(state, int):
                states = CocktailState.names
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

        data = self.request.data
        ingredients = data.get('ingredients')
        flexibility = data.get('flexibility')
        alcohol = data.get('alcohol')

        if not isinstance(alcohol, int) and alcohol is not None:
            try:
                alcohol = json.loads(alcohol)
            except:
                raise ValidationError({
                    'alcohol': ['Must be a boolean.']
                })

        if flexibility is None:
            flexibility = 0

        if not isinstance(flexibility, int):
            raise ValidationError({
                'flexibility': ['Must be an integer.']
            })

        if ingredients is None:
            raise ValidationError({
                'ingredients': ['This field is required.']
            })

        if not isinstance(ingredients, list):
            raise ValidationError({
                'ingredients': ['Must be an array of integer.']
            })

        if len(ingredients) == 0:
            raise ValidationError({
                'ingredients': ['Must be an array of integer.']
            })

        if not all(isinstance(ingredient, int) for ingredient in ingredients):
            raise ValidationError({
                'ingredients': ['Must be an array of integer.']
            })

        if alcohol is not None:
            queryset = queryset.filter(alcoholic=alcohol)

        queryset = queryset.filter(
            ingredients__pk__in=ingredients
        ).annotate(
            num_ingredients=Count('ingredients')
        ).filter(
            num_ingredients__lte=len(ingredients) + flexibility
        )

        matches = Cocktail.objects.none()
        for cocktail in queryset:
            not_match_count = 0

            for ingredient in cocktail.ingredients.all():
                if ingredient.pk not in ingredients:
                    not_match_count += 1

            if not_match_count <= flexibility:
                if not matches.filter(id=cocktail.pk).exists():
                    matches |= queryset.filter(id=cocktail.pk)

        return matches.distinct()

    def post(self, request, *args, **kwargs):
        return super().get(request, args, kwargs)


class CocktailsAddAPIView(CreateAPIView):
    '''
    Takes a set of information required (name, picture, etc) to add a
    new cocktail and returns the data of the newly added cocktail.
    '''
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultipartJsonParser,)
    queryset = Cocktail.objects.all()

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return CocktailSerializer
        return CocktailSerializer

    def perform_create(self, serializer):
        public = self.request.data.get('public')
        ingredients = self.request.data.get('ingredients')

        if ingredients is None:
            raise ValidationError({
                'ingredients': ['This field is required']
            })

        if not isinstance(ingredients, list):
            raise ValidationError({
                'ingredients': ['Must be an array of integer.']
            })

        if not all(isinstance(ingredient, int) for ingredient in ingredients):
            raise ValidationError({
                'ingredients': ['Must be an array of integer.']
            })
        cocktail = serializer.save()

        for ingredient_id in ingredients:
            try:
                ingredient = Ingredient.objects.get(pk=ingredient_id)
            except Ingredient.DoesNotExist:
                raise ValidationError({
                    'detail': f'Ingredient of ID \'{ingredient_id}\' does not exist.'
                })

            if public and not ingredient.public:
                ingredient.public = True
                ingredient.state = IngredientState.PENDING
            cocktail.ingredients.add(ingredient)

        return cocktail


class CocktailDetailUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Cocktail.objects.all()

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return CocktailSerializer
        return CocktailSerializer
