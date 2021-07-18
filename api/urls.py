from django.urls import path, include
from rest_framework import routers
from .views import api_overview, user_list_view, retreive_user_view, UserView, ArtworksView, CategoryView, CommentView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = 'api'

router = routers.DefaultRouter()
router.register('users', UserView)
router.register('categories', CategoryView)
router.register('comments', CommentView)


urlpatterns = [
    path('', include(router.urls)),
    path('artworks/', ArtworksView.as_view({'get':'list'}), name='artwork-list'),
    path('artworks/<int:pk>/', ArtworksView.as_view({'get':'retrieve'}), name='artwork-details'),
    path('artworks/create/', ArtworksView.as_view({'post':'create'}), name='artwork-create'),
    path('users/<str:username>/', retreive_user_view, name='get_user_view'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

