from django.test import TestCase, Client
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from django.shortcuts import reverse
from http import HTTPStatus
from .forms import RegisterForm

class UserTestCase(TestCase):
    UserModel = get_user_model()

    def setUp(self):
        self.valid_username = 'test'
        self.valid_password = 'python123'
        valid_user = self.UserModel(username=self.valid_username, is_staff=0, is_superuser=0, email="mymail@gmail.com")
        valid_user.set_password(self.valid_password)
        valid_user.save() 
        self.validators = settings.AUTH_PASSWORD_VALIDATORS
        
    def test_valid_user_created(self):
        user = self.UserModel.objects.filter(username="test")
        self.assertTrue(user.exists())


    def test_duplicate_username(self):
        try:
            invalid_user_username = self.UserModel(username="test", password="python123", is_staff=0, is_superuser=0, email='duplicateuser@mail.com').save()
            can_create_user = True
        except:
            can_create_user = False
        self.assertFalse(can_create_user)


    def test_password_length_validator(self):
        has_validator = False
        for validator in self.validators:
            if validator['NAME'] == 'django.contrib.auth.password_validation.MinimumLengthValidator':
                has_validator = True
                break
        self.assertTrue(has_validator)


    def test_user_login(self):
        response = self.client.login(username=self.valid_username, password=self.valid_password)
        self.assertTrue(response)
        response = self.client.login(username='non-existent', password=self.valid_password)
        self.assertFalse(response)
        response = self.client.login(username=self.valid_username, password='wrong-password')
        self.assertFalse(response)


    def test_register_form(self):
        register_url = reverse('users:register')
        data = {
            'username':'registeraccount',
            'email':'ey@mail.com',
            'password1':self.valid_password,
            'password2':self.valid_password
        }

        valid_form = RegisterForm(data=data)
        self.assertTrue(valid_form.is_valid())

        invalid_email_data = {key:value for key,value in data.items()}
        invalid_email_data['email'] = 'bad email'
        invalid_email_form = RegisterForm(data=invalid_email_data)
        self.assertFalse(invalid_email_form.is_valid())

        existing_username_data = {key:value for key,value in data.items()}
        existing_username_data['username'] = self.valid_username
        existing_username_form = RegisterForm(data=existing_username_data)
        self.assertFalse(existing_username_form.is_valid())

        not_matching_pw_data = {key:value for key,value in data.items()}
        not_matching_pw_data['password2'] = 'not matching'
        not_matching_pw_form = RegisterForm(data=not_matching_pw_data)
        self.assertFalse(not_matching_pw_form.is_valid())
