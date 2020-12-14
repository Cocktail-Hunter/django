from rest_framework import serializers

from ..models import Ingredient, IngredientState


class IngredientSerializer(serializers.ModelSerializer):
    '''
    Serialize data between JSON and Python readable dictionary format
    '''
    state = serializers.SerializerMethodField('get_state')
    added_by = serializers.SerializerMethodField('get_author')

    class Meta:
        '''
        Meta data for the serializer
        e.g. what model/table is this serializer for?
        '''
        model = Ingredient
        exclude = ('cocktaildb_id',)
        read_only_fields = ('state', 'added_by')
        extra_kwargs = {
            'public': {'required': True}
        }

    def create(self, validated_data):
        '''
        Set the appropriate data that has not been passed through
        the request body like 'added_by'
        '''
        validated_data['added_by'] = self.context.get('request').user

        # Set the ingredient to the appropriate state
        if not validated_data.get('public'):
            validated_data['state'] = IngredientState.APPROVED

        return super().create(validated_data)

    def get_state(self, ingredient):
        return ingredient.get_state_display()

    def get_author(self, ingredient):
        return {
            'id': ingredient.added_by.id,
            'username': ingredient.added_by.username
        }
