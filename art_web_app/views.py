from django.shortcuts import render
from artworks.models import Artwork, ArtCategory, Category
from utils.get_utils import get_random_index
from django.core.exceptions import ObjectDoesNotExist

def home_view(request):
    invalid_ids = set()
    
    try:
        nr_of_artworks = Artwork.objects.latest('id').id
    except ObjectDoesNotExist as e:
        art = None

    while True:
        art_query_index = get_random_index(nr_of_artworks)
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