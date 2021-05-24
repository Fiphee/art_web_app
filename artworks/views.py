from django.shortcuts import render, redirect, reverse
from .forms import ArtForm
from django.db import transaction
from .models import Category, Artwork, ArtLike
from django.contrib.auth import authenticate


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
    next_url = request.GET.get('next')

    if user.is_authenticated:
        artwork = Artwork.objects.get(pk=art_id)
        if artwork.likes.filter(id=user.id).exists():
            artwork.likes.remove(user)
        else:
            artwork.likes.add(user)
        if next_url:
            return redirect(next_url)
        return HttpResponseRedirect(reverse('artworks:view', args=(art_id,)))
    return redirect('/login')


def swipe_like_view(request, art_id):
    if request.user.is_authenticated:
        artwork = Artwork.objects.get(pk=art_id)
        artwork.likes.add(request.user)
    return redirect('/')


def art_view(request, art_id):
    artwork = Artwork.objects.get(pk=art_id)
    liked = artwork.likes.filter(id=request.user.id).exists()
    categories = artwork.category.all()
    context = {
        "artwork":artwork,
        "artist": artwork.uploader,
        "liked":liked,
        "categories":categories,
    }
    return render(request, 'artworks/view.html', context)

