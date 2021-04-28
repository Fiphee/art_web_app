from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.db import transaction
from artworks.models import Artwork
from .models import GalleryArtwork, Gallery, UserFollowedGallery
from .forms import GalleryForm
from .utils import get_next_position


def create_gallery_view(request):
    if request.method == 'POST':
        form = GalleryForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('users:galleries', args=(request.user.username,)))
    else:
        form = GalleryForm(user=request.user)

    context = {
        "form":form,
    }

    return render(request, 'galleries/create.html', context)


def add_artwork(request, art_id, gallery_id):
    if request.user.is_authenticated:
        gallery = Gallery.objects.get(id=gallery_id)
        if gallery.creator == request.user:
            artwork = Artwork.objects.get(id=art_id)
            try:
                GalleryArtwork.objects.get(gallery=gallery, art=artwork)
            except GalleryArtwork.DoesNotExist:  # if artwork not in the gallery then add the connection.
                position = get_next_position(GalleryArtwork, gallery=gallery.id)
                gallery.artworks.add(artwork, through_defaults={'position':position})
            return redirect(reverse('users:profile', args=(artwork.uploader.username,)))
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
                return redirect(reverse('galleries:view', args=(gallery_id,)))
        else:
            form = GalleryForm(user=user, instance=gallery)

        context['form'] = form
    context['saved_by_user'] = UserFollowedGallery.objects.filter(user=user, gallery=gallery).exists()
    
    return render(request, 'galleries/view.html', context)


def remove_artwork(request, art_id, gallery_id):
    gallery = get_object_or_404(Gallery, id=gallery_id)
    if request.user.is_authenticated:
        if gallery.creator == request.user:
            artwork = Artwork.objects.get(id=art_id)
            if artwork in gallery.artworks.all():
                gallery.artworks.remove(artwork)
                return redirect(reverse('galleries:view', args=(gallery_id,)))   
        return redirect('/')
    return redirect('/login')


def delete_gallery(request, gallery_id):
    gallery = get_object_or_404(Gallery, id=gallery_id)
    if gallery.creator == request.user:
        gallery.delete()
        return redirect(reverse('users:galleries', args=(request.user,)))
    return redirect('/')


def follow_gallery(request, gallery_id):
    user = request.user
    if user.is_authenticated:
        gallery = get_object_or_404(Gallery, id=gallery_id)
        if not UserFollowedGallery.objects.filter(gallery=gallery, user=user).exists():
            position = get_next_position(UserFollowedGallery, user=user.id)
            user.followed_galleries.add(gallery, through_defaults={'position':position})
        return redirect(reverse('galleries:view', args=(gallery_id,)))
    return redirect('/login')


def unfollow_gallery(request, gallery_id):
    user = request.user
    if user.is_authenticated:
        gallery = get_object_or_404(Gallery, id=gallery_id)
        gallery_relationship = UserFollowedGallery.objects.filter(gallery=gallery, user=user)
        if gallery_relationship.exists():
            gallery_relationship.first().delete()
        return redirect(reverse('galleries:view', args=(gallery_id,)))
    return redirect('/login')