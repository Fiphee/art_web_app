from django.test import TestCase
from .models import Artwork, Color, Category
from django.contrib.auth import get_user_model
from .forms import ArtForm
from django.conf import settings
from django.test.client import Client
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from art_web_app.utils import get_non_swiped_artworks
from django.test import override_settings
import shutil


ORIGINAL_ROOT = settings.MEDIA_ROOT
TEST_DIR = 'test_images'

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


    @override_settings(MEDIA_ROOT=(os.path.join(TEST_DIR, 'media')))
    def test_artwork_upload(self):
        default_avatar_path = os.path.join(ORIGINAL_ROOT, 'users', 'avatars', 'default.png')
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



class SwipeTestCase(TestCase):
  
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
        self.art1 = self.upload(self)
        self.art2 = self.upload(self)

        self.second_user = self.UserModel(username='second user', email='second_user@gmail.com')
        self.second_user.set_password(self.valid_password)
        self.second_user.save()


    @override_settings(MEDIA_ROOT=(os.path.join(TEST_DIR, 'media')))
    def upload(self):
        default_avatar_path = os.path.join(ORIGINAL_ROOT, 'users', 'avatars', 'default.png')
        art_title = 'test_artwork'
        data = {
            'title':art_title,
            'description':'empty',
            'categories':'portrait',
        }

        with open(default_avatar_path, 'rb') as f:
            form = ArtForm(data=data, user=self.user, files={'image':SimpleUploadedFile('image.png', f.read())})
            valid = form.is_valid()
            artwork = form.save()
        return artwork


    def test_uploads(self):
        self.assertEqual(len(Artwork.objects.all()), 2)


    def test_likes_not_returned_on_swipe_page(self):
        # get_non_swiped_artworks function returns artworks which are:
        # - Not LIKED by the user given
        # - Not DISLIKED by the user given
        # - The user given is NOT the UPLOADER of the artwork

        # user is the uploader -> []
        artworks = get_non_swiped_artworks(self.user)
        self.assertEqual(len(artworks), 0)
        
        # not uploader, not liked, not disliked -> [art1, art2]
        artworks = get_non_swiped_artworks(self.second_user)
        self.assertEqual(len(artworks), 2)
        self.assertTrue(self.art1 in artworks)
        self.assertTrue(self.art2 in artworks)

        # not uploader, art1 LIKED, not disliked -> [art2]
        self.art1.likes.add(self.second_user)
        artworks = get_non_swiped_artworks(self.second_user)
        self.assertEqual(len(artworks), 1)
        self.assertTrue(self.art1 not in artworks)
        
        # not uploader, art1 LIKED, art2 DISLIKED -> []
        self.art2.dislikes.add(self.second_user)
        artworks = get_non_swiped_artworks(self.second_user)
        self.assertEqual(len(artworks), 0)      


    def tearDown(self):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass

