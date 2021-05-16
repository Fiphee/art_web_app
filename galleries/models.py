from django.db import models
from art_web_app.models import CustomModel, AuthUserModel
from utils.constants import PUBLIC_MODE, PRIVATE_MODE
from artworks.models import Artwork


class Gallery(CustomModel):
    creator = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE, related_name='galleries')
    name = models.CharField(max_length=255)

    class Types(models.IntegerChoices):
        PUBLIC = PUBLIC_MODE
        PRIVATE = PRIVATE_MODE

    status = models.SmallIntegerField(choices=Types.choices, default=PUBLIC_MODE)
    artworks = models.ManyToManyField(Artwork, through='GalleryArtwork', related_name='galleries')
    followers = models.ManyToManyField(AuthUserModel, through='UserFollowedGallery', related_name='followed_galleries')
    position = models.IntegerField(default=0)

    class Meta:
        ordering = ['position']
        verbose_name_plural = 'Galleries'


    def __str__(self):
        return self.name


    def __repr__(self):
        return self.__str__()


class GalleryArtwork(CustomModel):
    art = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)

    class Meta:
        ordering = ['position']


class UserFollowedGallery(CustomModel):
    user = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['position']