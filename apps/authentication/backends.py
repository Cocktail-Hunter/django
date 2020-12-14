from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    '''
    Allow login only using email and not username.
    '''

    def authenticate(self, request, email=None, password=None, **kwargs):
        user_model = get_user_model()

        try:
            user = user_model.objects.get(email__iexact=email)
            return user if user.check_password(password) else None
        except user_model.DoesNotExist:
            return None
