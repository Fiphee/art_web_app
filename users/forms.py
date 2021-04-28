from django.contrib.auth.forms import UserCreationForm
from .models import AuthUserModel, Profile
from django import forms


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = AuthUserModel
        fields = ['username', 'email', 'password1', 'password2']


class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['description', 'quote','avatar', 'homepage_type']	

        widgets = {
            'description': forms.Textarea(attrs={'class':'textarea'}),
            'quote':forms.TextInput(attrs={'class':'textinput'}),
            'avatar':forms.FileInput(attrs={'class':'upload'}),
            'homepage_type':forms.Select(attrs={'class':'select_choice'})
        }


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = AuthUserModel
        fields = ['first_name', 'last_name','email']	

        widgets = {
            'first_name': forms.TextInput(attrs={'class':'textinput'}),
            'last_name':forms.TextInput(attrs={'class':'textinput'}),
            'email':forms.TextInput(attrs={'class':'textinput'}),
        }