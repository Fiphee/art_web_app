from django.urls import path 
from art_web_app.views import home_view, search_artworks_view, search_colors_view, search_users_view, search_galleries_view


app_name = 'search'

urlpatterns = [
    path('', search_artworks_view, name="artworks"),
    path('colors/', search_colors_view, name="colors"),
    path('users/', search_users_view, name="users"),
    path('galleries/', search_galleries_view, name='galleries'),
]
