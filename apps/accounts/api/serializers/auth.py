from rest_framework import status
from rest_framework import exceptions
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenBackendError, TokenError

from ...models import User


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


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    '''
    Inherit from `TokenRefreshSerializer` and touch the database
    before re-issuing a new access token and ensure that the user
    exists and is active.
    '''

    error_msg = 'No active account found with the given credentials'

    def validate(self, attrs):
        token_payload = attrs.get('refresh')

        if token_payload is not None:
            # Decode token
            try:
                token = token_backend.decode(token_payload)
            except TokenBackendError:
                raise TokenError('Token is invalid or expired')

        try:
            user = User.objects.get(pk=token.get('user_id'))
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                self.error_msg, 'no_active_account'
            )

        if not user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_msg, 'no_active_account'
            )

        return super().validate(attrs)
