from django.db.models import Q
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

from ...models import User
from ..serializers.user import InventorySerializer, UserSerializer, ChangePasswordSerializer
from apps.ingredients.models import Ingredient


class InventoryAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    http_method_names = ('get', 'put', 'delete', 'head', 'options')

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return InventorySerializer
        return InventorySerializer

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        pk = request.data.get('id')
        name = request.data.get('name')

        if pk is None and name is None:
            raise ValidationError({
                'detail': 'Ingredient id or name provided does not match any results in the database.'
            })

        if pk is not None:
            try:
                pk = int(pk)
            except:
                raise ValidationError({
                    'id': ['A valid integer is required.']
                })

        try:
            ingredient = Ingredient.objects.get(
                (Q(pk=pk) | Q(name__iexact=name))
            )
        except Ingredient.DoesNotExist:
            raise ValidationError({
                'detail': 'Ingredient id or name provided does not match any results in the database.'
            })
        else:
            user = request.user
            if user.inventory.filter(pk=ingredient.id).exists():
                user.inventory.remove(ingredient)
            else:
                raise ValidationError({
                    'detail': 'User does not own the ingredient provided in their inventory.'
                })

        serializer = InventorySerializer(user).data
        return Response(serializer, status=status.HTTP_202_ACCEPTED)


class UserRetrieveAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return UserSerializer
        return UserSerializer

    def get_object(self):
        return self.request.user


class UserPasswordUpdateAPIView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.version == 'v1':
            return ChangePasswordSerializer
        return ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            response = {
                'status': 'success',
                'message': 'Password updated successfully.'
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
