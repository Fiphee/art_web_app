from django.db import models
from art_web_app.models import CustomModel, AuthUserModel
from utils.constants import SWIPE_HOMEPAGE, GALLERY_HOMEPAGE, NEWEST_HOMEPAGE, POPULARS_HOMEPAGE
from django.contrib.contenttypes.fields import GenericRelation
from notifications.models import Notification

from comments.models import Comment


class Profile(CustomModel):
    user = models.OneToOneField(AuthUserModel, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, null=True)
    quote = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='users/avatars/', default='/users/avatars/default.png')
    comments = GenericRelation(Comment)

    class Types(models.IntegerChoices):
        SWIPE = SWIPE_HOMEPAGE
        GALLERY = GALLERY_HOMEPAGE 
        NEWEST = NEWEST_HOMEPAGE
        POPULARS = POPULARS_HOMEPAGE  

    homepage_type = models.SmallIntegerField(choices=Types.choices, default=SWIPE_HOMEPAGE)
    notifications = GenericRelation(Notification)


    def __str__(self):
        return self.user.username


    def __repr__(self):
        return __str__()


class UserFollowing(CustomModel):
    user = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE, related_name="followers")
    user_followed_by = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE, related_name="follows")

