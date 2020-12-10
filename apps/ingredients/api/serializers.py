from rest_framework import serializers

from ..models import Ingredient, IngredientState


class AddIngredientSerializer(serializers.ModelSerializer):
    '''
    Serialize data between JSON and Python readable dictionary format
    '''
    class Meta:
        '''
        Meta data for the serializer
        e.g. what model/table is this serializer for?
        '''
        model = Ingredient
        fields = ('name', 'public')
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
        if not validated_data.get('is_public'):
            validated_data['state'] = IngredientState.APPROVED

        return super().create(validated_data)
