from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.db import transaction
from artworks.models import Artwork
from .models import GalleryArtwork, Gallery, UserSavedGallery
from .forms import GalleryForm
from utils.get_utils import get_next_position


def create_gallery_view(request):
    if request.method == 'POST':
        form = GalleryForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('users:user_galleries_view', args=(request.user.username,)))
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
                position = get_next_position(GalleryArtwork, gallery_id=gallery.id)
                new_artwork_in_gallery = GalleryArtwork(gallery_id=gallery, art_id=artwork, position=position)
                new_artwork_in_gallery.save()
            return redirect(reverse('users:profile_view', args=(artwork.uploader.username,)))
        return redirect('/')
    return redirect('/login')


def gallery_view(request, gallery_id):
    context = {}
    user = request.user
    gallery = get_object_or_404(Gallery, id=gallery_id)
    if gallery.status == 0:
        status = 'Public'
    else:
        status = 'Private'

    context['gallery'] = gallery
    context['status'] = status
    if gallery.creator == user:
        if request.method == 'POST':
            form = GalleryForm(request.POST, user=user, instance=gallery)
            if form.is_valid():
                form.save()
                return redirect(reverse('galleries:gallery_view', args=(gallery_id,)))
        else:
            form = GalleryForm(user=user, instance=gallery)

        context['form'] = form
    context['saved_by_user'] = UserSavedGallery.objects.filter(user_id=user, gallery_id=gallery).exists()
    
    return render(request, 'galleries/gallery_view.html', context)


def remove_artwork(request, art_id, gallery_id):
    gallery = get_object_or_404(Gallery, id=gallery_id)
    if request.user.is_authenticated:
        if gallery.creator == request.user:
            artwork = Artwork.objects.get(id=art_id)
            if artwork in gallery.artworks.all():
                gallery.artworks.remove(artwork)
                return redirect(reverse('galleries:gallery_view', args=(gallery_id,)))   
        return redirect('/')
    return redirect('/login')


def delete_gallery(request, gallery_id):
    gallery = get_object_or_404(Gallery, id=gallery_id)
    if gallery.creator == request.user:
        gallery.delete()
        return redirect(reverse('users:user_galleries_view', args=(request.user,)))
    return redirect('/')


def save_gallery(request, gallery_id):
    user = request.user
    if user.is_authenticated:
        gallery = get_object_or_404(Gallery, id=gallery_id)
        if not UserSavedGallery.objects.filter(gallery_id=gallery, user_id=user).exists():
            position = get_next_position(UserSavedGallery, user_id=user.id)
            new_saved_gallery = UserSavedGallery(user_id=user, gallery_id=gallery, position=position)
            new_saved_gallery.save()
        return redirect(reverse('galleries:gallery_view', args=(gallery_id,)))
    return redirect('/login')


def remove_saved_gallery(request, gallery_id):
    user = request.user
    if user.is_authenticated:
        gallery = get_object_or_404(Gallery, id=gallery_id)
        gallery_relationship = UserSavedGallery.objects.filter(gallery_id=gallery, user_id=user)
        if gallery_relationship.exists():
            gallery_relationship.first().delete()
        return redirect(reverse('galleries:gallery_view', args=(gallery_id,)))
    return redirect('/login')