from django.test import TestCase
from django.shortcuts import reverse
from .models import Artwork, Color
from django.contrib.auth import get_user_model
from .forms import ArtForm
from django.conf import settings
import os
from PIL import Image
from django.test.client import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from os import unlink
from tempfile import NamedTemporaryFile

class ArtworkTestCase(TestCase):

    def setUp(self):
        self.valid_username = 'testart'
        self.valid_email = 'testordog@hotmail.com'
        self.valid_password = 'python123'
        self.UserModel = get_user_model()
        self.user = self.UserModel(username=self.valid_username, email=self.valid_email)
        self.user.set_password(self.valid_password)
        self.user.save()
        self.client.login(username=self.valid_username, password=self.valid_password)


    def test_upload_form(self):
        # default_avatar_path = os.path.join(settings.MEDIA_ROOT, 'users', 'avatars', 'default.png')
        image = Image.new('RGB', (100, 100))
        image_file = NamedTemporaryFile(suffix='.jpg')
        image.save(image_file)
        data = {
            'title':'test_artwork',
            'description':'empty',
            'categories':'portrait',
            'image':image_file
        }
        form = ArtForm(data=data, user=self.user)
        valid = form.is_valid()
        print(valid)
        print(form.errors)
        self.assertTrue(valid)
