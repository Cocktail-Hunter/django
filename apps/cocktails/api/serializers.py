from rest_framework import serializers

from ..models import Cocktail, CocktailState
from apps.ingredients.models import Ingredient, IngredientState


class StateSerializerField(serializers.Field):
    def to_representation(self, obj):
        return obj

    def to_internal_value(self, data):
        try:
            data = int(data)
            if 0 <= data <= 2:
                return data

            raise serializers.ValidationError(
                'Value out of range. Must be between 0 and 2.'
            )
        except ValueError:
            if isinstance(data, str):
                data = data.upper()
                if data in CocktailState.names:
                    return CocktailState.names.index(data)

                raise serializers.ValidationError(
                    f'Unrecognisable state. Expected: {CocktailState.names}'
                )

        raise ValidationError('Unexpected state was provided.')


class CocktailSerializer(serializers.ModelSerializer):
    '''
    Serialize data between JSON and Python readable dictionary format
    '''
    state = StateSerializerField(required=False)
    ingredients = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    author = serializers.SerializerMethodField()

    class Meta:
        '''
        Meta data for the serializer
        e.g. what model/table is this serializer for?
        '''
        model = Cocktail
        exclude = ('cocktaildb_id',)
        read_only_fields = ('author',)
        extra_kwargs = {
            'public': {'required': True},
            'alcoholic': {'required': True},
            'picture': {'required': True}
        }

    def save(self):
        '''
        Since setting state is only allowed both during creation and updating
        by admin, handle it in save to handle it once only for both situations.
        '''
        user = self.context.get('request').user

        if not user.is_admin and self.validated_data.get('state') is not None:
            raise serializers.ValidationError({
                'state': ['Only admins are allowed to set state.']
            })

        return super().save()

    def create(self, validated_data):
        '''
        Set the appropriate data that has not been passed through
        the request body like 'author'
        '''
        user = self.context.get('request').user
        validated_data['author'] = user

        # Set the cocktail to the appropriate state
        if not validated_data.get('public'):
            validated_data['state'] = CocktailState.APPROVED

        # Automatically approve cocktails from admins if state is not provided
        if user.is_admin and validated_data.get('state') is None:
            validated_data['state'] = CocktailState.APPROVED

        return super().create(validated_data)

    def update(self, cocktail, validated_data):

        if self.context.get('request').user != cocktail.author:
            raise serializers.ValidationError({
                'detail': 'You do not own this cocktail and therefore not allowed to modify it.'
            })

        if 'public' in validated_data:
            # Set the cocktail to the appropriate state
            if validated_data.get('public'):
                validated_data['state'] = CocktailState.PENDING
            else:
                if cocktail.public and cocktail.state == CocktailState.APPROVED:
                    raise serializers.ValidationError({
                        'detail': 'Public cocktails cannot be reverted back to private once approved.'
                    })
                else:
                    validated_data['state'] = CocktailState.APPROVED

        state = validated_data.get('state')
        if state is not None and state == CocktailState.APPROVED:
            for ingredient in cocktail.ingredients.all():
                if ingredient.state != IngredientState.APPROVED:
                    ingredient.state = IngredientState.APPROVED
                ingredient.save()

        return super().update(cocktail, validated_data)

    def get_author(self, cocktail):
        if cocktail.author is not None:
            return {
                'id': cocktail.author.id,
                'username': cocktail.author.username
            }
        return None
