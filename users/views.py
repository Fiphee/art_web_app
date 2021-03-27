from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.db import transaction
from .forms import RegisterForm
from .models import Profile, AuthUserModel


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
        user = get_object_or_404(AuthUserModel ,username=username)

    context['user'] = user
    try:
        context['user_artworks'] = [art for art in user.artwork_set.all()]
    except AttributeError:
        context['user_artworks'] = None
        
    return render(request, "users/profile.html", context)