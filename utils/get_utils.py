from django.db.models import Q
from artworks.models import Artwork
from users.models import AuthUserModel


def _split_queries(user_query):
    queries = []
    query = ''
    keep_spaces = False
    for char in user_query:
        if char == '"': 
            keep_spaces = True if keep_spaces == False else False
            continue
        if not keep_spaces and char == ' ' and query != '':
            queries.append(query)
            query = ''
            continue
        query += char
    queries.append(query)
    return queries


def get_query(query=None):
    art_query_results = set()
    user_query_results = set()
    queries = _split_queries(query)
    if len(queries) > 0:
        for q in queries:
            artworks = Artwork.objects.filter(
                Q(title__icontains=q),
            )
            users = AuthUserModel.objects.filter(
                Q(username__icontains=q),
            )
            for art in artworks:
                art_query_results.add(art)
            for user in users:
                user_query_results.add(user)
                
    return art_query_results, user_query_results