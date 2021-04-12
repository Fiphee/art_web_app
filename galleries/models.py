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
    users = models.ManyToManyField(AuthUserModel, through='UserSavedGallery', related_name='favourite_galleries')


    def __str__(self):
        return self.name


    def __repr__(self):
        return self.__str__()


class GalleryArtwork(CustomModel):
    art_id = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    gallery_id = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    position = models.IntegerField()

    class Meta:
        ordering = ['position']


class UserSavedGallery(CustomModel):
    user_id = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE, related_name='saved_galleries')
    gallery_id = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='saved_by')
    position = models.IntegerField()
    