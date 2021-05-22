from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .forms import ArtForm
from django.db import transaction
from .models import Category, Artwork, ArtLike
from django.contrib.auth import authenticate
from notifications.models import Notification
from utils.constants import ART_LIKE, COMMENT
from comments.forms import CommentForm
from utils.comment import CommentUtils
from comments.models import Comment
from django.http import JsonResponse

@login_required
def upload_view(request):
    if request.method == "POST":
        form = ArtForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            with transaction.atomic():
                form.save()
            return redirect('/')
    else:
        form = ArtForm(user=request.user)
    context = {
        "form":form,
    }
    return render(request, 'artworks/upload.html', context)


def like_view(request, art_id):
    user = request.user
    # next_url = request.GET.get('next')

    if user.is_authenticated:
        artwork = Artwork.objects.get(pk=art_id)
        artwork.notify = {'activity':ART_LIKE, 'user':user, 'recipient':artwork.uploader}
        liked = False
        if artwork.likes.filter(id=user.id).exists():
            artwork.likes.remove(user)
        else:
            artwork.likes.add(user)
            liked = True

        return JsonResponse({"liked":liked, "art_likes":artwork.likes.count()})
    return redirect('/login')


def swipe_like_view(request, art_id):
    user = request.user
    if user.is_authenticated:
        artwork = Artwork.objects.get(pk=art_id)
        artwork.notify = {'activity':ART_LIKE, 'user':user, 'recipient':artwork.uploader}
        artwork.likes.add(user)
    return redirect('/')


def art_view(request, art_id):
    user = request.user
    artwork = Artwork.objects.get(pk=art_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if user.is_authenticated:
                comment = Comment(author=user, body=form.cleaned_data['body'], content_object=artwork)
                comment.notify = {'user':user, 'recipient':artwork.uploader, 'activity':COMMENT}
                comment.save()
                return redirect(reverse('artworks:view', args=(art_id,)))
            return redirect('/login')
    else: 
        form = CommentForm()
        liked = artwork.likes.filter(id=user.id).exists()
        categories = artwork.category.all()
        comments = artwork.comments.all()
        
        context = {
            "artwork":artwork,
            "artist": artwork.uploader,
            "liked":liked,
            "categories":categories,
            "comments":comments,
            "form": form,
            'comment_util': CommentUtils('uploader', reverse('artworks:view', args=(art_id,)), user == artwork.uploader)
        }
        return render(request, 'artworks/view.html', context)

