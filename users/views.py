from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.db import transaction
from .forms import RegisterForm, ProfileSettingsForm, UserSettingsForm
from .models import Profile, AuthUserModel, UserFollowing


def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    
    context = {
        "form":form
    }

    return render(request, "register.html", context)


def profile_settings_view(request, user_id):
    user = request.user
    if user_id == request.user.id:
        if request.method == "POST":
            form = ProfileSettingsForm(request.POST, request.FILES, instance=user.profile)
            user_form = UserSettingsForm(request.POST, instance=user)
            with transaction.atomic():
                if form.is_valid() and user_form.is_valid():
                    user_form.save()
                    form.save()
                    return redirect('/')
        else:
            form = ProfileSettingsForm(instance=user.profile)
            user_form = UserSettingsForm(instance=user)
        
        context = {
            "form":form,
            "user_form":user_form,
        }
        return render(request, 'users/profile_settings.html', context)
    return redirect('/')


def profile_view(request, username):
    context = {}
    if username == request.user.username:
        user = request.user
    else:
        user = get_object_or_404(AuthUserModel, username=username)
    
    artworks = []
    total_likes = 0
    context['visited_user'] = user
    try:
        for art in user.artworks.all():
            artworks.append(art)
            total_likes += art.likes.count()
    except AttributeError:
        print("User has no artworks")

    context['user_artworks'] = artworks
    context['total_art_likes'] = total_likes
    context['already_following'] = False

    if request.user.is_authenticated:
        already_following = user.followers.filter(user_followed_by=request.user).first()
        if already_following:
            context['already_following'] = True
    context['url_user'] = username
    
    return render(request, "users/profile.html", context)


def follow_view(request, artist_id):
    if request.user.is_authenticated:
        if artist_id != request.user.id:
            artist = AuthUserModel.objects.get(id=artist_id)
            followed = UserFollowing.objects.filter(user=artist, user_followed_by=request.user).first()
            if followed:
                followed.delete()
            else:
                UserFollowing(user_followed_by=request.user, user=artist).save()
        return redirect(reverse('users:profile', args=(artist.username,)))
    return redirect('/login')


def user_galleries_view(request, username):
    context = {}
    if username == request.user.username:
        user = request.user
    else:
        user = get_object_or_404(AuthUserModel, username=username)
    
    galleries = []
    total_artworks_in_gallery = 0
    context['visited_user'] = user
    try:
        for gallery in user.galleries.all():
            galleries.append(gallery)
            total_artworks_in_gallery += gallery.artworks.count()
    except AttributeError:
        print("User has no galleries")

    context['user_galleries'] = galleries
    context['url_user'] = username
    if request.user.is_authenticated:
        already_following = user.followers.filter(user_followed_by=request.user).first()
        context['already_following'] = already_following


    return render(request, "users/galleries.html", context)

    
