from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.db import transaction
from .forms import GalleryForm


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