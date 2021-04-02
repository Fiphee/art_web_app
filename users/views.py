from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import authenticate, login
from django.db import transaction
from .forms import RegisterForm
from .models import Profile, AuthUserModel, UserFollowing
from django.http import HttpResponseRedirect


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


def profile_view(request, username):
    context = {}
    if username == request.user.username:
        user = request.user
    else:
        user = get_object_or_404(AuthUserModel, username=username)

    context['visited_user'] = user
    try:
        context['user_artworks'] = [art for art in user.artwork_set.all()]
        likes = 0
        for art in context['user_artworks']:
            likes += art.likes.count()
        context['art_likes'] = likes       
    except AttributeError:
        context['user_artworks'] = None
        context['art_likes'] = None
        
    context['already_following'] = False
    if request.user.is_authenticated:
        test = user.followers.filter(user_followed_by=request.user).first()
        if test:
            context['already_following'] = True
    context['url_user'] = username
    
    return render(request, "users/profile.html", context)


def follow_view(request, artist_id):
    if request.user.is_authenticated:
        if artist_id != request.user.id:
            artist = AuthUserModel.objects.get(id=artist_id)
            followed = UserFollowing.objects.filter(user_id=artist, user_followed_by=request.user).first()
            if followed:
                followed.delete()
            else:
                UserFollowing(user_followed_by=request.user, user_id=artist).save()
        return HttpResponseRedirect(reverse('users:profile_view', args=(artist.username,)))
    return redirect('/login')
    