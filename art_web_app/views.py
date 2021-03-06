from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from utils import get_query
from artworks.models import Artwork, ArtCategory, Category
import random


def home_view(request):
    invalid_ids = set()
    
    try:
        last_artwork_id = Artwork.objects.latest('id').id
    except ObjectDoesNotExist as e:
        art = None

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


def search_view(request):
    context = {}
    query = ''
    if request.method == 'GET':
        query = request.GET['search']
        context['query'] = str(query)
    try:
        artworks, users = get_query(query)
    except:
        artworks = ''
        users = ''
        
    context['artworks'] = artworks
    context['users'] = users
    return render(request, 'search.html', context)



