from django.db.models import Q
from rest_framework import serializers

from ...models import User
from apps.ingredients.models import Ingredient
from apps.ingredients.api.serializers import IngredientSerializer


class InventorySerializer(serializers.ModelSerializer):
    inventory = IngredientSerializer(many=True, read_only=True)
    id = serializers.IntegerField(write_only=True, required=False)
    name = serializers.CharField(write_only=True, required=False)

    class Meta:
        '''
        Meta data for the serializer
        e.g. what model/table is this serializer for?
        '''
        model = User
        fields = ('inventory', 'id', 'name')

    def update(self, user, validated_data):
        pk = validated_data.get('id')
        name = validated_data.get('name')

        if pk is None and name is None:
            raise serializers.ValidationError({
                'detail': 'Ingredient id or name provided does not match any results in the database.'
            })

        if pk is not None:
            try:
                pk = int(pk)
            except:
                raise serializers.ValidationError({
                    'detail': 'Id should be an integer'
                })

        try:
            ingredient = Ingredient.objects.get(
                (Q(pk=pk) | Q(name=name))
            )
        except Ingredient.DoesNotExist:
            raise serializers.ValidationError({
                'detail': 'Ingredient id or name provided does not match any results in the database.'
            })
        else:
            user.inventory.add(ingredient)

        return user
