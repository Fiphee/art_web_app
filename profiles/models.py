from django.db import models
from art_web_app.models import CustomModel
# Create your models here.
from django.contrib.auth.models import User
from galleries.models import Galleries
from utils.constants import SWIPE_HOMEPAGE, GALLERY_HOMEPAGE, NEWEST_HOMEPAGE, POPULARS_HOMEPAGE



class Profile(CustomModel):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, null=True)
    quote = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', default='media/avatars/default.png')

    class Types(models.IntegerChoices):
        SWIPE = SWIPE_HOMEPAGE
        GALLERY = GALLERY_HOMEPAGE 
        NEWEST = NEWEST_HOMEPAGE
        POPULARS = POPULARS_HOMEPAGE  

    homepage_type = models.SmallIntegerField(choices=Types.choices, null=False, default=SWIPE_HOMEPAGE)


class UserFollowing(CustomModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    user_followed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")


class UserSavedGalleries(CustomModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    galler_id = models.ForeignKey(Galleries, on_delete=models.CASCADE)
