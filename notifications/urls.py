from django.urls import path
from .views import categories_view, activity_view, content_view, mark_as_seen, seen_view, all_unseen_view, clear_seen_view


app_name = 'notifications'


urlpatterns = [
    path('', categories_view, name='categories'),
    path('<int:activity>', activity_view, name='activities'),
    path('<int:activity>/<int:content_id>', content_view, name='content'),
    path('mark-as-seen/<int:id_to_filter>', mark_as_seen, name='mark_as_seen'),
    path('seen', seen_view, name='seen'),
    path('all_unseen', all_unseen_view, name='all_unseen'),
    path('clear_seen', clear_seen_view, name='clear_seen'),
]   