from django.contrib.auth.forms import UserCreationForm
from .models import AuthUserModel
from django import forms


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = AuthUserModel
        fields = ['username', 'email', 'password1', 'password2']
