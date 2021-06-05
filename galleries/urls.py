from django.urls import path
from .views import create_gallery_view, add_artwork, gallery_view, remove_artwork, delete_gallery, follow_gallery, unfollow_gallery


app_name = 'galleries'

urlpatterns = [
    path('create/', create_gallery_view, name='create'),
    path('add/<int:art_id>/to/<int:gallery_id>/', add_artwork, name='add_artwork'),
    path('<int:gallery_id>/', gallery_view, name='view'),
    path('delete/<int:art_id>/from/<int:gallery_id>/', remove_artwork, name='remove_artwork'),
    path('<int:gallery_id>/delete/', delete_gallery, name='delete'),
    path('<int:gallery_id>/follow/', follow_gallery, name='follow'),
    path('<int:gallery_id>/unfollow/', unfollow_gallery, name='unfollow'),
]   