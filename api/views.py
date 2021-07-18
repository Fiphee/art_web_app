from re import search
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework import viewsets, mixins
from rest_framework import filters
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer, 
    ArtworkSerializer, 
    ArtworkDetailSerializer,
    UploadArtworkSerializer, 
    CategorySerializer, 
    CommentSerializer
    
)
from rest_framework.permissions import IsAuthenticated
from artworks.models import Artwork, Category
from comments.models import Comment
from utils.categories import CategoryUtils


AuthUserModel = get_user_model()


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'List':'/api/users',
    }
    return Response(api_urls)


@api_view(['GET'])
def user_list_view(request):
    queryset = AuthUserModel.objects.all()
    serializer = UserSerializer(queryset, many=True, context={'request':request})
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def retreive_user_view(request, username):
    try:
        user = AuthUserModel.objects.get(username=username)
    except AuthUserModel.DoesNotExist:
        user = None
    serializer = UserSerializer(user, context={'request':request})
    return JsonResponse(serializer.data, safe=False)


class ArtworksView(viewsets.ModelViewSet):
    queryset = Artwork.objects.all()
    filter_backends = [filters.SearchFilter]    
    search_fields  = ['title', 'category__name']
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if hasattr(self, 'action'):
            if self.action == 'create':
                return UploadArtworkSerializer
            elif self.action == 'retrieve':
                return ArtworkDetailSerializer
        return ArtworkSerializer


    def perform_create(self, serializer):
        data = self.request.data
        categories = CategoryUtils.create_categories(data['categories'])
        obj = serializer.save(uploader=self.request.user)
        for category in categories:
            obj.category.add(category)


class UserView(viewsets.ModelViewSet):
    queryset = AuthUserModel.objects.all()
    serializer_class = UserSerializer


class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'head']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            category = Category.objects.get(name=request.data['name'])
            serializer = self.get_serializer(instance=category)
            return Response(serializer.data)
        except Exception as e:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, headers=headers)


class CommentView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
