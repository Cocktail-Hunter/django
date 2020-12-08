from rest_framework import serializers
from rest_framework import status

from ..models import User


class RegistrationSerializer(serializers.ModelSerializer):
    '''
    Serialize data between JSON and Python readable dictionary format
    '''
    class Meta:
        '''
        Meta data for the serializer
        e.g. what model/table is this serializer for?
        '''
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        '''
        Handle data once serializer is saved
        '''
        user = User(
            username=self.validated_data.get('username'),
            email=self.validated_data.get('email')
        )
        password = self.validated_data.get('password')

        user.set_password(password)
        user.save()
        return user
