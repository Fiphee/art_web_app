from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from art_web_app.views import home_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('', include('users.urls')),
    path('', include('django.contrib.auth.urls')),
    path('search/', include('art_web_app.urls.search')),
    path('artworks/', include('artworks.urls')),
    path('galleries/', include('galleries.urls')),
    path('notifications/', include('notifications.urls')),
    path('comments/', include('comments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)