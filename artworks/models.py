from django.db import models
from art_web_app.models import CustomModel
# Create your models here.
from django.contrib.auth.models import User
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile


class Categories(CustomModel):
    category = models.CharField(max_length=50, null=False)


class Artworks(CustomModel):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='artworks/original_image', null=False)
    thumbnail = models.ImageField(upload_to='artworks/thumbnails', default='artworks/thumbnails/default_thumb.jpg')
    category = models.ManyToManyField(Categories, through='ArtCategories', related_name="artworks", blank=False)
    likes = models.ManyToManyField(User, through='ArtLikes', related_name='artworks_liked')
    favourites = models.ManyToManyField(User, through='ArtFavourites', related_name='favourite_artworks')
    # galleries = models.ManyToManyField(Galleries, through='GalleryArtworks')

    def save(self, *args, **kwargs):
        if not self.make_thumbnail():
            raise Exception('Could not create thumbnail - is the file type valid?')

        super(Artworks, self).save(*args, **kwargs)


    def make_thumbnail(self):
        image = Image.open(self.image)
        image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)

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
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # Add the thumbnail to the thumbnail column
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True


class ArtCategories(CustomModel):
    art_id = models.ForeignKey(Artworks, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE)


class ArtLikes(CustomModel):
    art_id = models.ForeignKey(Artworks, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class ArtFavourites(CustomModel):
    art_id = models.ForeignKey(Artworks, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
