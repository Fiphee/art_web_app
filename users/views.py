from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.db import transaction
from .forms import RegisterForm, ProfileSettingsForm, UserSettingsForm
from .models import Profile


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