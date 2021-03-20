from django.db import models
from django.contrib.auth.models import User
from art_web_app.models import CustomModel
from utils.constants import PUBLIC_MODE, PRIVATE_MODE
from artworks.models import Artworks
# Create your models here.


class Galleries(CustomModel):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_galleries')
    name = models.CharField(max_length=255, blank=False, null=False)

    class Types(models.IntegerChoices):
        PUBLIC = PUBLIC_MODE
        PRIVATE = PRIVATE_MODE

    status = models.SmallIntegerField(choices=Types.choices, null=False, default=PUBLIC_MODE)
    artworks = models.ManyToManyField(Artworks, through='GalleryArtworks', related_name='in_galleries')
    users = models.ManyToManyField(User, through='UserSavedGalleries', related_name='galleries')


class GalleryArtworks(CustomModel):
    art_id = models.ForeignKey(Artworks, on_delete=models.CASCADE)
    gallery_id = models.ForeignKey(Galleries, on_delete=models.CASCADE)


class UserSavedGalleries(CustomModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_galleries')
    gallery_id = models.ForeignKey(Galleries, on_delete=models.CASCADE, related_name='saved_by')