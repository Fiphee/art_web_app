from django.test import TestCase
from .models import Artwork, Color, Category
from django.contrib.auth import get_user_model
from .forms import ArtForm
from django.conf import settings
from django.test.client import Client
import os
from django.core.files.uploadedfile import SimpleUploadedFile


class ArtworkTestCase(TestCase):

    @classmethod
    def setUpTestData(self):
        self.valid_username = 'testart'
        self.valid_email = 'testordog@hotmail.com'
        self.valid_password = 'python123'
        self.UserModel = get_user_model()
        self.user = self.UserModel(username=self.valid_username, email=self.valid_email)
        self.user.set_password(self.valid_password)
        self.user.save()
        self.client = Client()
        self.client.login(username=self.valid_username, password=self.valid_password)


    def test_artwork_upload(self):
        default_avatar_path = os.path.join(settings.MEDIA_ROOT, 'users', 'avatars', 'default.png')
        art_title = 'test_artwork'
        data = {
            'title':art_title,
            'description':'empty',
            'categories':'portrait',
        }

        with open(default_avatar_path, 'rb') as f:
            form = ArtForm(data=data, user=self.user, files={'image':SimpleUploadedFile('image.png', f.read())})
            valid = form.is_valid()
            self.assertTrue(valid)
            form.save()
            art = Artwork.objects.get(title=art_title, uploader=self.user)
            
            # check if categories and m2m connection was created properly
            art_category_count = art.category.count()
            self.assertEqual(art_category_count, 1) 
            
            # check if colors and m2m connection was created properly
            art_colors_count = art.colors.count()
            self.assertEqual(art_colors_count, 6)            
