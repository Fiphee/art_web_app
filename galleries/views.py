from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect
from django.db import transaction
from artworks.models import Artwork
from .models import GalleryArtwork
from .forms import GalleryForm, Gallery
from utils.get_utils import get_next_position


def create_gallery_view(request):
    if request.method == 'POST':
        form = GalleryForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:user_gallery_view', args=(request.user.username,)))
    else:
        form = GalleryForm(user=request.user)

    context = {
        "form":form,
    }

    return render(request, 'galleries/create_gallery.html', context)


def add_artwork(request, art_id, gallery_id):
    if request.user.is_authenticated:
        gallery = Gallery.objects.get(id=gallery_id)
        if gallery.creator == request.user:
            artwork = Artwork.objects.get(id=art_id)
            try:
                GalleryArtwork.objects.get(gallery_id=gallery, art_id=artwork)
                raise Exception('Artwork in the gallery already')
            except GalleryArtwork.DoesNotExist:  # if artwork not in the gallery then add the connection.
                new_artwork_in_gallery = GalleryArtwork(gallery_id=gallery, art_id=artwork, position=get_next_position(gallery))
                new_artwork_in_gallery.save()
            return HttpResponseRedirect(reverse('users:profile_view', args=(artwork.uploader.username,)))
        return redirect('/')
    return redirect('/login')        