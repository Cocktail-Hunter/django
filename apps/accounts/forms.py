from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class UserCreationForm(forms.ModelForm):
    '''
    Handle data received from registration form
    '''
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        '''
        Meta data for the class
        '''
        model = User
        fields = ('username', 'email', 'is_admin', 'avatar')

    def clean_password2(self):
        '''
        Check that the two password entries match
        '''
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        '''
        Save the provided password in hashed format
        '''
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    '''
    Handle data received from form to edit user data
    '''
    password = ReadOnlyPasswordHashField(
        label='Password',
        help_text=(
            "Raw passwords are not stored, so there is no way to see "
            "this user's password, but you can change the password "
            "using <a href=\"../password/\">this form</a>."
        )
    )

    class Meta:
        '''
        Meta data for the class
        '''
        model = User
        fields = ('username', 'email', 'is_admin', 'avatar')

    def clean_password(self):
        '''
        Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the
        field does not have access to the initial value
        '''
        return self.initial["password"]
