from django.urls import path
from .views import create_gallery_view

app_name = 'galleries'

urlpatterns = [
    path('create/', create_gallery_view, name='create_gallery_view'),
]