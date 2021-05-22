from django.contrib import admin
from .models import Gallery


def get_artwork_count(obj):
    return f'{obj.artworks.count()}'

get_artwork_count.short_description = 'Artwork count'


def get_creator(obj):
    return f'{obj.creator.username}'

get_creator.short_description = 'Creator'


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        get_creator,
        get_artwork_count, 
        )

    search_fields = ('creator__username', 'name')