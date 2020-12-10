from rest_framework import serializers
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import User


class RegistrationSerializer(serializers.ModelSerializer):
    '''
    Serialize data between JSON and Python readable dictionary format
    '''
    tokens = serializers.SerializerMethodField()

    class Meta:
        '''
        Meta data for the serializer
        e.g. what model/table is this serializer for?
        '''
        model = User
        fields = ('username', 'email', 'password', 'tokens')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_tokens(self, user):
        token_pairs = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(token_pairs),
            'access': str(token_pairs.access_token)
        }
        return tokens

    def create(self, validated_data):
        '''
        Create user from serialized data from valid POST request
        '''
        user = User(
            username=validated_data.get('username'),
            email=validated_data.get('email')
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user
