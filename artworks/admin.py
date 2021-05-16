from django.contrib import admin
from .models import Artwork, Category, ArtCategory, ArtFavourite, ArtLike
from django.utils.html import format_html
from django.shortcuts import reverse


admin.site.register(Category)


def get_username(obj):
    url = reverse('users:profile', args=(obj.uploader,))
    return format_html(f'<a href={url}>{obj.uploader}</a>')

get_username.short_description = 'Artist'


def get_like_count(obj):
    return f'{obj.likes.count()}'

get_like_count.short_description = 'Likes'


def get_page(obj):
    url = reverse('artworks:view', args=(obj.id,))
    return format_html(f'<a href={url}>Visit</a>')

get_page.short_description = 'On site page'


def get_title(obj):
    url = reverse('admin:artworks_artwork_change', args=(obj.id,))
    return format_html(f'<a href={url}>{obj.title}</a>')

get_title.short_description = 'Title'


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    list_display = (
        lambda obj: format_html(f'<img src="{obj.thumbnail.url}" width="50px"/>'),
        get_title,
        get_username,
        get_like_count,
        get_page,
        )
    
    search_fields = ('uploader__username', 'title')