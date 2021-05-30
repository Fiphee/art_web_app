from django.test import TestCase
from django.test.client import Client
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import reverse
import os
from artworks.forms import ArtForm


class CommentTestCase(TestCase):

    @classmethod
    def setUpTestData(self):
        self.UserModel = get_user_model()
        self.client = Client()
        self.pw = 'python123'
        self.username = 'commenter'

        self.commenter =  self.UserModel(username=self.username, email='icomment@gmail.com')
        self.commenter.set_password(self.pw)
        self.commenter.save()
        
        default_avatar_path = os.path.join(settings.MEDIA_ROOT, 'users', 'avatars', 'default.png')
        data = {
            'title':'test_comments',
            'description':'empty',
            'categories':'portrait',
        }

        with open(default_avatar_path, 'rb') as f:
            form = ArtForm(data=data, user=self.commenter, files={'image':SimpleUploadedFile('image.png', f.read())})
            self.artwork = form.save()

        self.client.login(username=self.commenter.username, password=self.pw)
        url = reverse('artworks:view', args=(self.artwork.id,))
        data = {'body':'Comment on an artwork!'}
        self.client.post(url, data=data, follow=True)
        self.comment = self.artwork.comments.filter().first()


    def test_user_created(self):
        user_exists = self.UserModel.objects.filter(username=self.username).exists()
        self.assertTrue(user_exists)


    def test_make_comment(self):
        comment_exists = self.artwork.comments.filter().exists()
        self.assertTrue(comment_exists)
        

    def test_artwork_comment(self):
        self.client.login(username=self.commenter.username, password=self.pw)

        like_url = reverse('comments:like', args=(self.comment.id,)) + '?next=/'
        self.client.get(like_url)
        self.assertEqual(self.comment.likes.count(), 1)

        self.client.get(like_url)
        self.assertEqual(self.comment.likes.count(), 0)

        self.comment.delete()
        self.assertEqual(len(self.artwork.comments.all()), 0)
  