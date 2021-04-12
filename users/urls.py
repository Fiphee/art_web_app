from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, profile_settings_view


app_name = 'users'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('users/<int:user_id>/settings', profile_settings_view, name="profile_settings"),
]
