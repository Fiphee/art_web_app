from django.shortcuts import render, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Count
from artworks.models import Artwork, ArtLike, ArtDislike
import random
from .search import search_artworks_view, search_colors_view, search_galleries_view, search_users_view
from ..utils import get_homepage_date_filters, get_non_swiped_artworks, get_random_artwork
from utils.constants import THIS_MONTH, TODAY, ALL_TIME
from datetime import datetime, timedelta
import time


def home_view(request):
    user = request.user
    art = None
    try:
        last_artwork_id = Artwork.objects.latest('id').id
    except ObjectDoesNotExist as e:
        return render(request, "home.html", {})
    
    if request.user.is_authenticated:
        non_swiped_artworks = get_non_swiped_artworks(request.user)
        if non_swiped_artworks:
            random_index = random.randint(0, len(non_swiped_artworks)-1)
            art = non_swiped_artworks[random_index]

    if not art:
        art = get_random_artwork()


    context = {
        'art':art,
    }
    return render(request, "home.html", context)


def list_view(request):
    list_type = request.GET.get('artworks')
    filter_by = request.GET.get('filter', THIS_MONTH)
    date_filters = get_homepage_date_filters(filter_by)

    if list_type == 'followed':
        artworks = Artwork.objects.filter(uploader__followers__user_followed_by=request.user.id, **date_filters).order_by('-created_at')
        extra_options = True
    elif list_type == 'oldest':
        artworks = Artwork.objects.filter(**date_filters).order_by('created_at')
        extra_options = True
    elif list_type == 'newest':
        artworks = Artwork.objects.filter(**date_filters).order_by('-created_at')
        extra_options = False
    elif list_type == 'popular':
        artworks = Artwork.objects.annotate(likes_count=Count('likes')).filter(**date_filters).order_by('-likes_count')
        extra_options = True


    page_obj = Paginator(artworks, 12)
    page_number = request.GET.get('page', 1)
    page = page_obj.get_page(page_number)

    context = {
        'page_obj':page_obj,
        'page':page,
        'page_url': reverse('list') + f'?artworks={list_type}&filter={filter_by}&page=',
        'extra_options':extra_options
    }
    return render(request, 'home.html', context)

    