from artworks.models import Artwork, Category, Color
from users.models import AuthUserModel
from galleries.models import Gallery
from utils.constants import GALLERY_HOMEPAGE, NEWEST_HOMEPAGE, POPULARS_HOMEPAGE, FOLLOWED_HOMEPAGE, OLDEST_HOMEPAGE, THIS_MONTH, TODAY, ALL_TIME
from datetime import datetime, timedelta, date

class Search:
    @staticmethod
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

    @staticmethod
    def artworks(query=None):
        queries = Search._split_queries(query)
        art_query_results = set()
        if len(queries) > 0:
            for q in queries:
                if q.startswith('#'):
                    category = Category.objects.get(name=q[1:])
                    for art in category.artworks.all():
                        art_query_results.add(art)
                    continue
                artworks = Artwork.objects.filter(title__icontains=q)
                for art in artworks:
                    art_query_results.add(art)
        return art_query_results

    @staticmethod
    def galleries(query=None):
        queries = Search._split_queries(query)
        gallery_query_results = set()
        if len(queries) > 0:
            for q in queries:
                galleries = Gallery.objects.filter(name__icontains=q)
                for gallery in galleries:
                    gallery_query_results.add(gallery)
        return gallery_query_results

    @staticmethod
    def users(query=None):
        queries = Search._split_queries(query)
        user_query_results = set()
        if len(queries) > 0:
            for q in queries:
                users = AuthUserModel.objects.filter(username__icontains=q)
                for user in users:
                    user_query_results.add(user)
        return user_query_results

    @staticmethod
    def colors(query=None):
        query_results = set()
        colors = Color.objects.filter(category__name=query)
        for color in colors:
            for art in color.artworks.all():
                query_results.add(art)
        return query_results
        

def get_homepage_date_filters(max_time_ago):
    if max_time_ago == TODAY:
        now = datetime.now()
        day_start = now.replace(hour=0)
        return {'created_at__gte':day_start}
    
    elif max_time_ago == THIS_MONTH:
        now = datetime.now()
        month_start = now.replace(day=1)
        return {'created_at__gte':month_start}

    elif max_time_ago == ALL_TIME:
        return {}

