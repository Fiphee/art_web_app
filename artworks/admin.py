from django.contrib import admin
from .models import Artworks, Categories, ArtCategories, ArtFavourites, ArtLikes
# Register your models here.


admin.site.register(Artworks)
admin.site.register(Categories)
admin.site.register(ArtCategories)
admin.site.register(ArtLikes)
admin.site.register(ArtFavourites)

