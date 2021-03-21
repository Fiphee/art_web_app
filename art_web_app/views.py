from django.shortcuts import render


def home_view(request):
    context = {
        'user':request.user,
    }
    return render(request, "home.html", context)