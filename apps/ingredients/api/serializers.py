from rest_framework import serializers

from ..models import Ingredient, IngredientState


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
                if data in IngredientState.names:
                    return IngredientState.names.index(data)

                raise serializers.ValidationError(
                    f'Unrecognisable state. Expected: {IngredientState.names}'
                )

        raise ValidationError('Unexpected state was provided.')


class IngredientSerializer(serializers.ModelSerializer):
    '''
    Serialize data between JSON and Python readable dictionary format
    '''
    state = StateSerializerField(required=False)
    added_by = serializers.SerializerMethodField('get_author')

    class Meta:
        '''
        Meta data for the serializer
        e.g. what model/table is this serializer for?
        '''
        model = Ingredient
        exclude = ('cocktaildb_id',)
        read_only_fields = ('added_by',)
        extra_kwargs = {
            'public': {'required': True},
            'alcoholic': {'required': True}
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
        the request body like 'added_by'
        '''
        user = self.context.get('request').user
        validated_data['added_by'] = user

        # Set the ingredient to the appropriate state
        if not validated_data.get('public'):
            validated_data['state'] = IngredientState.APPROVED

        # Automatically approve ingredients from admins if state is not provided
        if user.is_admin and validated_data.get('state') is None:
            validated_data['state'] = IngredientState.APPROVED

        return super().create(validated_data)

    def update(self, ingredient, validated_data):

        if self.context.get('request').user != ingredient.added_by:
            raise serializers.ValidationError({
                'detail': 'You do not own this ingredient and therefore not allowed to modify it.'
            })

        if 'public' in validated_data:
            # Set the ingredient to the appropriate state
            if validated_data.get('public'):
                validated_data['state'] = IngredientState.PENDING
            else:
                if ingredient.public and ingredient.state == IngredientState.APPROVED:
                    raise serializers.ValidationError({
                        'detail': 'Public ingredients cannot be reverted back to private once approved.'
                    })
                else:
                    validated_data['state'] = IngredientState.APPROVED

        return super().update(ingredient, validated_data)

    def get_author(self, ingredient):
        if ingredient.added_by is not None:
            return {
                'id': ingredient.added_by.id,
                'username': ingredient.added_by.username
            }
        return None
