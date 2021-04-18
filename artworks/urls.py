from django.urls import path
from .views import upload_view, like_view, art_view, swipe_like_view


app_name = 'artworks'

urlpatterns = [
    path('upload/', upload_view, name='upload'),
    path('like/<int:art_id>', like_view, name='like'),
    path('swipe-like/<int:art_id>', swipe_like_view, name='swipe_like'),
    path('<int:art_id>', art_view, name='view')
]