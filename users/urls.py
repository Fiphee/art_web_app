from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view


app_name = 'users'

urlpatterns = [
    path('register/', register_view, name='register'),
]
