from django.shortcuts import render, reverse
from django.core.paginator import Paginator
from ..utils import Search
from artworks.models import Artwork


def search_artworks_view(request):
    context = {}
    query = ''
    if request.method == 'GET':
        query = request.GET['search'].replace('#', '%23')

    artworks = list(Search.artworks(query))
    page_obj = Paginator(artworks, 12)
    page_number = request.GET.get('page', 1)
    page = page_obj.get_page(page_number)
    context = {
        'artworks':artworks,
        'query': str(query).replace('%23', '#'),
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
        query = request.GET.get('search')
    
    following = request.GET.get('following', None) 
    if following:
        users = list(Search.following(request.user, following))
        page_url = reverse('search:users')+f'?following={following}&page=' 
    else:
        users = list(Search.users(query))
        page_url = reverse('search:users')+f'?search={query}&page='
    
    page_obj = Paginator(users, 40)
    page_number = request.GET.get('page', 1)
    page = page_obj.get_page(page_number)
    context = {
        'users':users,
        'query': query,
        'page_obj':page_obj,
        'page':page,
        'page_url':page_url,
        'following':following,
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