from django.shortcuts import render
from artworks.models import Artwork, ArtCategory, Category
from utils.get_utils import get_random_index


def home_view(request):
    invalid_ids = set()
    nr_of_artworks = Artwork.objects.latest('id').id
    while True:
        art_query_index = get_random_index(nr_of_artworks)
        try:
            if art_query_index in invalid_ids:
                continue
            artwork = Artwork.objects.get(id=art_query_index)
            break
        except:
            invalid_ids.add(art_query_index) 
            continue

    test = Category.artworks


    context = {
        'user':request.user,
        'art':artwork,
        'test':test
    }
    return render(request, "home.html", context)