from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, profile_view, follow_view, user_galleries_view


app_name = 'users'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('users/<str:username>', profile_view, name='profile_view'),
    path('follow/<int:artist_id>', follow_view, name='follow_view'),
    path('users/<str:username>/galleries', user_galleries_view, name="user_galleries_view"),
]
