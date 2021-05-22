from django.contrib import admin
from django.shortcuts import reverse
from .models import Profile
from django.utils.html import format_html
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


def get_full_name(obj):
    return f'{obj.user.first_name} {obj.user.last_name}'

get_full_name.short_description = 'Full name'


def get_artwork_count(obj):
    return f'{obj.user.artworks.count()}'

get_artwork_count.short_description = 'Nr. of Artworks'


def get_follower_count(obj):
    return f'{obj.user.followers.count()}'

get_follower_count.short_description = 'Followers'


def get_username(obj):
    url = reverse('admin:users_profile_change', args=(obj.id,))
    return format_html(f'<a href={url}>{obj.user}</a>')

get_username.short_description = 'Username'


def get_page(obj):
    url = reverse('users:profile', args=(obj.user,))
    return format_html(f'<a href={url}>Visit</a>')

get_page.short_description = 'Profile Page'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    ordering = ('user__username',)
    list_display = (
        lambda obj: format_html(f'<img src="{obj.avatar.url}" width="50px"/>'),
        get_username,
        get_full_name,
        get_artwork_count,
        get_follower_count,
        get_page,
        )
    search_fields = ('user__username', 'user__first_name','user__last_name')
    fieldsets = (
        ('Personal info', {'fields': ('user','description','quote','avatar','homepage_type')}),
    )
