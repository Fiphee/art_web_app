from django.shortcuts import render, redirect
from django.db import transaction
from .forms import RegisterForm
from .models import Profile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    
    context = {
        "form":form
    }

    return render(request, "register.html", context)

