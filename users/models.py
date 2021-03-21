from django.db import models
from art_web_app.models import CustomModel, AuthUserModel
from galleries.models import Gallery
from utils.constants import SWIPE_HOMEPAGE, GALLERY_HOMEPAGE, NEWEST_HOMEPAGE, POPULARS_HOMEPAGE


class Profile(CustomModel):
    user_id = models.OneToOneField(AuthUserModel, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, null=True)
    quote = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', default='media/avatars/default.png')

    class Types(models.IntegerChoices):
        SWIPE = SWIPE_HOMEPAGE
        GALLERY = GALLERY_HOMEPAGE 
        NEWEST = NEWEST_HOMEPAGE
        POPULARS = POPULARS_HOMEPAGE  

    homepage_type = models.SmallIntegerField(choices=Types.choices, default=SWIPE_HOMEPAGE)


class UserFollowing(CustomModel):
    user_id = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE, related_name="follows")
    user_followed_by = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE, related_name="followers")

