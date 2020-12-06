from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailOrUsernameBackend(ModelBackend):
    '''
    Allow users to authenticate using case insensitive username
    or using email which provides a way for users who forgot their
    username to authenticate themselves
    '''

    def authenticate(self, request, username=None, password=None, **kwargs):

        user_model = get_user_model()

        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)

        case_insensitive_username_field = f'{user_model.USERNAME_FIELD}__iexact'

        try:
            user = user_model.objects.get(
                Q(**{case_insensitive_username_field: username}) |
                Q(email__iexact=username)
            )
        except user_model.DoesNotExist:
            return None
        else:
            return user
