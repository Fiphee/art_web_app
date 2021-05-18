from django.contrib import admin
from .models import Gallery, GalleryArtwork, UserFollowedGallery


admin.site.register(Gallery)
admin.site.register(GalleryArtwork)
admin.site.register(UserFollowedGallery)
