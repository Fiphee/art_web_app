from django.urls import path
from users.views import profile_view, follow_view, user_galleries_view, profile_settings_view


urlpatterns = [
    path('<str:username>/', profile_view, name='profile'),
    path('follow/<int:artist_id>/', follow_view, name='follow'),
    path('<str:username>/galleries/', user_galleries_view, name="galleries"),
    path('<int:user_id>/settings/', profile_settings_view, name="settings"),
]
