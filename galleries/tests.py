from django.test import TestCase
from django.shortcuts import reverse
from django.test.client import Client
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from .models import Gallery
from artworks.forms import ArtForm
from .forms import GalleryForm
from utils.constants import PUBLIC_MODE
import os
from django.test import override_settings
import shutil


ORIGINAL_ROOT = settings.MEDIA_ROOT
TEST_DIR = 'test_images'

class GelleryTestCase(TestCase):
    
    @classmethod
    def setUpTestData(self):
        self.UserModel = get_user_model()
        self.client = Client()
        self.username = 'test_user'
        self.pw = 'python123'

        self.user = self.UserModel(username=self.username, email='gallery@mail.com')
        self.user.set_password(self.pw)
        self.user.save()

        self.gallery_name = 'first gallery'
        self.gallery = Gallery(creator=self.user, name=self.gallery_name)
        self.gallery.save()

        
    def test_setup_gallery_created(self):
        results =  Gallery.objects.filter(creator=self.user, name=self.gallery_name)
        self.assertEqual(len(results), 1)


    def test_follow_gallery(self):
        second_user = self.UserModel(username='second user', email='follower@mail.com')
        second_user.set_password(self.pw)
        second_user.save()
        self.client.login(username=second_user.username, password=self.pw)

        # check if gallery has no followers
        gallery_follower_count = self.gallery.followers.count()
        self.assertEqual(gallery_follower_count, 0)

        # check if following a gallery updates correctly 
        self.client.get(reverse('galleries:follow', args=(self.gallery.id,)))       
        gallery_follower_count = self.gallery.followers.count()
        self.assertEqual(gallery_follower_count, 1)

        # check if unfollowing a gallery updates correctly 
        self.client.get(reverse('galleries:unfollow', args=(self.gallery.id,)))
        gallery_follower_count = self.gallery.followers.count()
        self.assertEqual(gallery_follower_count, 0)
        

    @override_settings(MEDIA_ROOT=(os.path.join(TEST_DIR, 'media')))
    def test_gallery_add_and_remove_artwork(self):
        self.client.login(username=self.username, password=self.pw)
        default_avatar_path = os.path.join(ORIGINAL_ROOT, 'users', 'avatars', 'default.png')
        data = {
            'title':'test_gallery_work',
            'description':'empty',
            'categories':'portrait',
        }
        with open(default_avatar_path, 'rb') as f:
            form = ArtForm(data=data, user=self.user, files={'image':SimpleUploadedFile('image.png', f.read())})
            artwork = form.save()

        gallery_art_count = self.gallery.artworks.count()
        self.assertEqual(gallery_art_count, 0)
    
        self.client.get(reverse('galleries:add_artwork', args=(artwork.id, self.gallery.id)))
        gallery_art_count = self.gallery.artworks.count()
        self.assertEqual(gallery_art_count, 1)

        self.client.get(reverse('galleries:remove_artwork', args=(artwork.id, self.gallery.id)))
        gallery_art_count = self.gallery.artworks.count()
        self.assertEqual(gallery_art_count, 0)


    def test_gallery_form_and_delete(self):
        self.client.login(username=self.username, password=self.pw)
        data = {'name':'Form gallery', 'status':PUBLIC_MODE}
        form = GalleryForm(data=data, user=self.user)
        valid = form.is_valid()
        self.assertTrue(valid)
        
        galleries_count = self.user.galleries.count()
        self.assertEqual(galleries_count, 1)
        
        # save gallery
        gallery = form.save()
        galleries_count = self.user.galleries.count()
        self.assertEqual(galleries_count, 2)

        # delete gallery
        response = self.client.get(reverse('galleries:delete', args=(gallery.id,)))
        galleries_count = self.user.galleries.count()
        self.assertEqual(galleries_count, 1)


    def tearDown(self):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass