from django.contrib import admin
from .models import Gallery, GalleryArtwork, UserSavedGallery


admin.site.register(Gallery)
admin.site.register(GalleryArtwork)
admin.site.register(UserSavedGallery)
