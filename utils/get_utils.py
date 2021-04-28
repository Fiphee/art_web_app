from artworks.models import Artwork, Category
from users.models import AuthUserModel


def get_next_position(model, **kwargs):
    try:
        next_position = model.objects.filter(**kwargs).order_by('-position').first().position + 1
    except AttributeError:
        next_position = 1
    
    return next_position


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
            if q.startswith('#'):
                category = Category.objects.get(name=q[1:])
                for art in category.artworks.all():
                    art_query_results.add(art)
                continue
            artworks = Artwork.objects.filter(title__icontains=q)
            users = AuthUserModel.objects.filter(username__icontains=q)
            for art in artworks:
                art_query_results.add(art)
            for user in users:
                user_query_results.add(user)
    return art_query_results, user_query_results
