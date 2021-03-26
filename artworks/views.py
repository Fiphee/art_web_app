from django.shortcuts import render, redirect, reverse
from .forms import ArtForm
from django.db import transaction
from .models import Category, Artwork, ArtLike
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate


def upload_view(request):
    if request.method == "POST":
        form = ArtForm(request.POST, request.FILES)
        if form.is_valid():
            with transaction.atomic():
                form_save = form.save(commit=False)
                tags = [tag.lower() for tag in form.cleaned_data['category'].replace(' ', '').split(',')]
                form_save.uploader = request.user
                form_save.save()
                for tag in tags:
                    category = Category.objects.create(name=tag)
                    category.save()
                    form_save.category.add(category)
            return redirect('/')
    else:
        form = ArtForm()
    context = {
        "form":form,
    }
    return render(request, 'artworks/upload_art.html', context)


def like_view(request, art_id):
    if request.user.is_authenticated:
        artwork = Artwork.objects.get(pk=art_id)
        if artwork.likes.filter(id=request.user.id).exists():
            artwork.likes.remove(request.user)
        else:
            artwork.likes.add(request.user)
        return HttpResponseRedirect('/')
    return redirect('/login')


def swipe_like_view(request, art_id):
    if request.user.is_authenticated:
        artwork = Artwork.objects.get(pk=art_id)
        artwork.likes.add(request.user)
    return HttpResponseRedirect('/')


def art_view(request, art_id):
    artwork = Artwork.objects.get(pk=art_id)
    liked = artwork.likes.filter(id=request.user.id).exists()
    context = {
        "artwork":artwork,
        "artist": artwork.uploader,
        "liked":liked,
    }
    return render(request, 'artworks/art_view.html', context)

