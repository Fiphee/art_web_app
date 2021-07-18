from django.contrib.auth import get_user_model
from rest_framework import serializers
from artworks.models import Artwork, Category
from comments.models import Comment


AuthUserModel = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ArtworkSerializer(serializers.ModelSerializer):
    uploader = serializers.StringRelatedField()
    likes_count = serializers.SerializerMethodField()
    details = serializers.HyperlinkedIdentityField(
        view_name = 'api:artwork-details',
    )
    class Meta:
        model = Artwork
        fields = ['id', 'title', 'uploader', 'likes_count', 'created_at', 'details']
        

    def get_likes_count(self, obj):
        return obj.likes.count()


class ArtworkDetailSerializer(serializers.ModelSerializer):
    uploader = serializers.StringRelatedField()
    category = serializers.StringRelatedField(many=True)
    likes = serializers.StringRelatedField(many=True)
    colors = serializers.StringRelatedField(many=True)
    class Meta:
        model = Artwork
        fields = '__all__'


class UploadArtworkSerializer(serializers.ModelSerializer):
    categories = serializers.CharField(read_only=True)
    class Meta:
        model = Artwork
        fields = ['title', 'description', 'image', 'categories']


class UserSerializer(serializers.ModelSerializer):
    artworks = serializers.StringRelatedField(many=True, read_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = AuthUserModel
        exclude = ['is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions']

    def create(self, validated_data):
        user = super(UserSerializer,self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user