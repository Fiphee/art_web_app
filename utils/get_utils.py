from django.db.models import Q
from artworks.models import Artwork

def get_query(query=None):
    queryset = set()
    queries = query.split(' ')
    if len(queries) > 0:
        for q in queries:
            artworks = Artwork.objects.filter(
                Q(title__icontains=q),
            )
            for art in artworks:
                queryset.add(art)
    return queryset