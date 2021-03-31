from django.shortcuts import render
from utils.get_utils import get_query
from artworks.models import Artwork

def home_view(request):
    return render(request, "home.html", {})


def search_view(request):
    context = {}
    query = ''
    if request.method == 'GET':
        query = request.GET['q']
        context['query'] = str(query)
    try:
        artworks, users = get_query(query)
    except:
        artworks = ''
        users = ''
        
    context['artworks'] = artworks
    context['users'] = users
    return render(request, 'search.html', context)