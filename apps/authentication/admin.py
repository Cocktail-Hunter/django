from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    '''
    Organise fields and data in Django admin for user model
    '''
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'username', 'email', 'is_admin', 'is_active', 'is_verified'
    )
    list_filter = ('created_at',)

    fieldsets = (
        (None, {'fields': (
            'email', 'password', 'is_admin', 'is_active', 'is_verified'
        )}),
        ('Profile', {'fields': ('username', 'avatar')})
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'is_admin', 'password1', 'password2')}),
        ('Profile', {'fields': ('username', 'avatar')})
    )

    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)  # No longer need the built in Django group system
