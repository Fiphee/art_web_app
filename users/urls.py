from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, profile_settings_view
from .views import register_view, profile_view, follow_view


app_name = 'users'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('users/<int:user_id>/settings', profile_settings_view, name="profile_settings"),
    path('users/<str:username>', profile_view, name='profile_view'),
    path('follow/<int:artist_id>', follow_view, name='follow_view'),
]
