from django.contrib import admin
from .models import Artwork, Category, ArtCategory, ArtFavourite, ArtLike

admin.site.register(Artwork)
admin.site.register(Category)
admin.site.register(ArtCategory)
admin.site.register(ArtLike)
admin.site.register(ArtFavourite)

