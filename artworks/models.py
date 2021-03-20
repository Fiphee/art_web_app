from django.db import models
from art_web_app.models import CustomModel, AuthUserModel
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from utils.constants import THUMB_SIZE
import os


class Category(CustomModel):
    name = models.CharField(max_length=50, null=False)


    def __str__(self):
        return self.name


    def __repr__(self):
        return self.__str__()


class Artwork(CustomModel):
    uploader = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='artworks/original_images', null=False)
    thumbnail = models.ImageField(upload_to='artworks/thumbnails', default='default_thumb.jpg')
    category = models.ManyToManyField(Category, through='ArtCategory', related_name="artworks", blank=False)
    likes = models.ManyToManyField(AuthUserModel, through='ArtLike', related_name='artworks_liked')
    favourites = models.ManyToManyField(AuthUserModel, through='ArtFavourite', related_name='favourite_artworks')


    def save(self, *args, **kwargs):
        if not self.make_thumbnail():
            raise Exception('Could not create thumbnail - is the file type valid?')

        super(Artworks, self).save(*args, **kwargs)


    def make_thumbnail(self):
        img = Image.open(self.image)
        img.thumbnail(THUMB_SIZE, Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        img.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # Add the thumbnail to the thumbnail column
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True


    def delete(self, *args, **kwargs):
        self.image.storage.delete(self.image.name)
        self.thumbnail.storage.delete(self.thumbnail.name)
        super().delete(*args, **kwargs)


    def __str__(self):
        return self.title

    
    def __repr__(self):
        return self.__str__()


class ArtCategory(CustomModel):
    art_id = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)


class ArtLike(CustomModel):
    art_id = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    user_id = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE)


class ArtFavourite(CustomModel):
    art_id = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    user_id = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE)
