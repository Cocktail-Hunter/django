from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import _user_has_perm, _user_has_module_perms


class UserManager(BaseUserManager):
    '''
    Class containing methods for working with data from user model
    '''

    def create_user(self, username: str, email: str, password: str, **extra_fields):
        '''
        Creates and saves a user with the given username, password, email, created_at
        birth and password.
        '''
        if not username:
            raise ValueError('User must contain a username')
        if not email:
            raise ValueError('User must contain an email')

        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username: str, email: str, password: str, **extra_fields):
        '''
        Creates and saves a user with admin permissions
        '''
        user = self.create_user(username, email, password, **extra_fields)
        user.is_admin = True
        user.is_verified = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        '''
        Override Django's default case-sensitive username check
        This makes the username case-insensitve so only one user
        can have a specific username regardless of its letter casing
        '''
        case_insensitive_username_field = f'{self.model.USERNAME_FIELD}__iexact'
        return self.get(**{case_insensitive_username_field: username})


class User(AbstractBaseUser):
    '''
    Data that the user table will contain
    '''
    slug = models.SlugField(max_length=255)
    username = models.CharField(
        verbose_name='Username',
        max_length=255,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Email Address',
        max_length=255,
        unique=True
    )
    created_at = models.DateTimeField(
        verbose_name="Created Date",
        auto_now_add=True
    )
    avatar = models.ImageField(upload_to='users/avatars', blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    inventory = models.ManyToManyField(
        'ingredients.Ingredient',
        related_name='users',
        related_query_name='user'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def is_staff(self):
        '''
        Property that checks whether the user is an admin or not and thus a staff
        Needed for Django to function properly.
        '''
        return self.is_admin

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        '''
        Checks if the user has a specific permission
        '''
        # Active admins have all permissions
        if self.is_active and self.is_admin:
            return True

        # Otherwise we need to check the backends
        return _user_has_perm(self, perm, obj)

    def has_module_perms(self, app_label):
        '''
        Checks if the user has permissions to view the app `app_label`
        '''
        # Active admins have all permissions
        if self.is_active and self.is_admin:
            return True

        return _user_has_module_perms(self, app_label)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.username)
