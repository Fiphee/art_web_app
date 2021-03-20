from django.contrib import admin
from .models import Galleries, GalleryArtworks, UserSavedGalleries
# Register your models here.


admin.site.register(Galleries)
admin.site.register(GalleryArtworks)
admin.site.register(UserSavedGalleries)
