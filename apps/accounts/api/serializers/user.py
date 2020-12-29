from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from ...models import User
from apps.ingredients.models import Ingredient, IngredientState
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

        try:
            ingredient = Ingredient.objects.get(
                (Q(pk=pk) | Q(name__iexact=name))
            )
        except Ingredient.DoesNotExist:
            raise serializers.ValidationError({
                'detail': 'Ingredient id or name provided does not match any results in the database.'
            })
        else:
            if (not ingredient.public or ingredient.state == IngredientState.PENDING) and ingredient.added_by.id != user.id:
                raise PermissionDenied({
                    'detail': 'You are not permitted to add this ingredient to your inventory.'
                })
            if not user.inventory.filter(pk=ingredient.id).exists():
                user.inventory.add(ingredient)
            else:
                raise serializers.ValidationError({
                    'detail': 'User already owns the ingredient provided in their inventory.'
                })

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        '''
        Meta data for the serializer
        e.g. what model/table is this serializer for?
        '''
        model = User
        exclude = ('password', 'inventory')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        '''
        Meta data for the serializer
        e.g. what model/table is this serializer for?
        '''
        model = User
        exclude = ('password', 'inventory')
