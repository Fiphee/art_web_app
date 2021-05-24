from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view, search_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('', include('users.urls')),
    path('', include('django.contrib.auth.urls')),
    path('search/', search_view, name="search_view"),
    path('artworks/', include('artworks.urls')),
    path('galleries/', include('galleries.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)