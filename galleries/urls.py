from django.urls import path
from .views import create_gallery_view, add_artwork

app_name = 'galleries'

urlpatterns = [
    path('create/', create_gallery_view, name='create_gallery_view'),
    path('<int:art_id>/to/<int:gallery_id>', add_artwork, name='add_artwork'),

]