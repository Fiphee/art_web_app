from django.urls import path
from .views import like_view, remove_view


app_name = 'comments'

urlpatterns = [
    path('<int:comment_id>/like/', like_view, name='like'),
    path('<int:comment_id>/delete/', remove_view, name='remove'),
]