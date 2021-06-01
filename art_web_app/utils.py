from artworks.models import Artwork, Category, Color
from users.models import AuthUserModel
from galleries.models import Gallery


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
        
    
    # def get_query(query=None):
    #     queries = Query._split_queries(query)
    #     if 'rgb' in query:
    #         query_results = set()
    #         colors = Color.objects.filter(category__name=query)
    #         for color in colors:
    #             for art in color.artworks.all():
    #                 query_results.add(art)
    #         return query_results
    #     art_query_results = set()
    #     user_query_results = set()
    #     gallery_query_results = set()
    #     queries = _split_queries(query)
    #     if len(queries) > 0:
    #         for q in queries:
    #             if q.startswith('#'):
    #                 category = Category.objects.get(name=q[1:])
    #                 for art in category.artworks.all():
    #                     art_query_results.add(art)
    #                 continue
    #             artworks = Artwork.objects.filter(title__icontains=q)
    #             users = AuthUserModel.objects.filter(username__icontains=q)
    #             galleries = Gallery.objects.filter(name__icontains=q)
    #             for art in artworks:
    #                 art_query_results.add(art)
    #             for user in users:
    #                 user_query_results.add(user)
    #             for gallery in galleries:
    #                 gallery_query_results.add(gallery)
    #     return art_query_results, user_query_results, gallery_query_results
