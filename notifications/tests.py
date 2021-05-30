from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Notification
from users.models import UserFollowing
from django.shortcuts import reverse
from django.test.client import Client
from artworks.forms import ArtForm
from comments.forms import CommentForm
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from utils.constants import ART_LIKE, FOLLOW, COMMENT, COMMENT_LIKE, GALLERY_FOLLOW, REPLY, UPLOAD
import os


class FollowAndArtworkNotificationTestCase(TestCase):

    @classmethod
    def setUpTestData(self):
        self.UserModel = get_user_model()
        self.pw = 'python123'
        self.uploader = self.UserModel(username='mr_upload2', email='iupload@gmail.com')
        self.uploader.set_password(self.pw)
        self.uploader.save()

        self.follower = self.UserModel(username='mr_follow2', email='ifollow@gmail.com')
        self.follower.set_password(self.pw)
        self.follower.save()

        self.client = Client()
        self.client.login(username=self.follower.username, password=self.pw)
        self.client.get(reverse('users:follow', args=(self.uploader.id,)))

        default_avatar_path = os.path.join(settings.MEDIA_ROOT, 'users', 'avatars', 'default.png')
        data = {
            'title':'test_work',
            'description':'empty',
            'categories':'portrait',
        }
        with open(default_avatar_path, 'rb') as f:
            form = ArtForm(data=data, user=self.uploader, files={'image':SimpleUploadedFile('image.png', f.read())})
            self.artwork = form.save()

        self.gallery = self.uploader.galleries.create(name='gallery')


    def test_users_created_and_followed(self):
        user_count = len(self.UserModel.objects.all())
        self.assertEqual(user_count, 2)
        uploader_follower_count = self.uploader.followers.count()
        self.assertEqual(uploader_follower_count, 1)  


    def test_user_got_follow_notification(self):
        notification_exists = self.uploader.notifications.filter(user=self.follower, activity=FOLLOW).exists()
        self.assertTrue(notification_exists)


    def test_self_follow(self):
        self.client.get(reverse('users:follow', args=(self.follower.id,)))
        self.assertEqual(self.follower.followers.count(), 0)
        notification_exists = self.follower.notifications.filter(user=self.follower).exists()
        self.assertFalse(notification_exists)


    def test_upload_notification(self):
        notification_exists = self.follower.notifications.filter(user=self.uploader, activity=UPLOAD)
        self.assertTrue(notification_exists)


    def test_art_like_notification(self):
        self.client.login(username=self.follower.username, password=self.pw)
        response = self.client.get(reverse('artworks:like', args=(self.artwork.id,)))
        notification_exists = self.uploader.notifications.filter(user=self.follower, activity=ART_LIKE).exists()
        self.assertTrue(notification_exists)

    
    def test_gallery_follow_notification(self):
        self.client.login(username=self.follower.username, password=self.pw)
        self.client.get(reverse('galleries:follow', args=(self.gallery.id,)))
        notification_exists = self.uploader.notifications.filter(user=self.follower, activity=GALLERY_FOLLOW).exists()
        self.assertTrue(notification_exists)


    def test_comment_notifications(self):
        self.client.login(username=self.follower.username, password=self.pw)
        
        url = reverse('artworks:view', args=(self.artwork.id,))
        data = {'body':'This is a comment!'}
        self.client.post(url, data=data, follow=True)

        notification_exists = self.uploader.notifications.filter(user=self.follower, activity=COMMENT).exists()
        self.assertTrue(notification_exists)

        comment = self.artwork.comments.filter().first()

        # comment like
        self.client.login(username=self.uploader.username, password=self.pw)
        like_url = reverse('comments:like', args=(comment.id,)) + '?next=/'
        self.client.get(like_url)
        notification_exists = self.follower.notifications.filter(user=self.uploader, activity=COMMENT_LIKE).exists()
        self.assertTrue(notification_exists)
        
        # check if comment like notification gets deleted when the comment is unliked
        self.client.get(like_url)
        notification_exists = self.follower.notifications.filter(user=self.uploader, activity=COMMENT_LIKE).exists()
        self.assertFalse(notification_exists)

        # check if notification gets deleted when the comment is deleted      
        self.client.login(username=self.follower.username, password=self.pw)  
        remove_url = reverse('comments:remove', args=(comment.id,)) + "?recipient=uploader&next=/"
        self.client.get(remove_url)
        self.assertEqual(self.artwork.comments.count(), 0)
        notification_exists = self.uploader.notifications.filter(user=self.follower, activity=COMMENT).exists()
        self.assertFalse(notification_exists)

