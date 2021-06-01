from django.shortcuts import render, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from .utils import Search
from artworks.models import Artwork, ArtCategory, Category
import random


def home_view(request):
    invalid_ids = set()
    
    try:
        last_artwork_id = Artwork.objects.latest('id').id
    except ObjectDoesNotExist as e:
        art = None
        return render(request, "home.html", {})

    while True:
        art_query_index = random.randint(1, last_artwork_id)
        try:
            if art_query_index in invalid_ids:
                continue
            art = Artwork.objects.get(id=art_query_index)
            break
        except ObjectDoesNotExist as e:
            invalid_ids.add(art_query_index) 
            continue

    context = {
        'art':art,
    }
    return render(request, "home.html", context)


def search_artworks_view(request):
    context = {}
    query = ''
    if request.method == 'GET':
        query = request.GET['search']

    artworks = list(Search.artworks(query))
    page_obj = Paginator(artworks, 12)
    page_number = request.GET.get('page', 1)
    page = page_obj.get_page(page_number)
    context = {
        'artworks':artworks,
        'query': str(query),
        'page_obj':page_obj,
        'page':page,
        'page_url':reverse('search:artworks')+f'?search={query}&page=',
    }
    return render(request, 'search/artworks.html', context)



def search_colors_view(request):
    context = {}
    query = ''
    if request.method == 'GET':
        query = request.GET['search']

    artworks = list(Search.colors(query))
    page_obj = Paginator(artworks, 12)
    page_number = request.GET.get('page', 1)
    page = page_obj.get_page(page_number)
    context = {
        'artworks':artworks,
        'query': str(query),
        'page_obj':page_obj,
        'page':page,
        'page_url':reverse('search:colors')+f'?search={query}&page=',
    }
    return render(request, 'search/colors.html', context)


def search_users_view(request):
    context = {}
    query = ''
    if request.method == 'GET':
        query = request.GET['search']

    users = list(Search.users(query))
    page_obj = Paginator(users, 40)
    page_number = request.GET.get('page', 1)
    page = page_obj.get_page(page_number)
    context = {
        'users':users,
        'query': str(query),
        'page_obj':page_obj,
        'page':page,
        'page_url':reverse('search:users')+f'?search={query}&page=',
    }
    return render(request, 'search/users.html', context)

    
def search_galleries_view(request):
    context = {}
    query = ''
    if request.method == 'GET':
        query = request.GET['search']

    galleries = list(Search.galleries(query))
    page_obj = Paginator(galleries, 20)
    page_number = request.GET.get('page', 1)
    page = page_obj.get_page(page_number)
    context = {
        'galleries':galleries,
        'query': str(query),
        'page_obj':page_obj,
        'page':page,
        'page_url':reverse('search:galleries')+f'?search={query}&page=',
    }
    return render(request, 'search/galleries.html', context)