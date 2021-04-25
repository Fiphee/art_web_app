from django.shortcuts import redirect, reverse
from .models import Comment


def like_view(request, comment_id):
    user = request.user
    try:
        next_url = request.GET.get('next')
    except KeyError:
        next_url = '/'
        
    if user.is_authenticated:
        comment = Comment.objects.get(id=comment_id)
        if comment.likes.filter(id=user.id).exists():
            comment.likes.remove(user)
        else:
            comment.likes.add(user)
        return redirect(next_url)
    return redirect('/login')


def remove_view(request, comment_id):
    user = request.user
    try:
        next_url = request.GET.get('next')
    except KeyError:
        next_url = '/'
    try:
        recipient = request.GET.get('recipient')
    except KeyError:
        recipient=None

    comment = Comment.objects.get(id=comment_id)
    content_object_user = getattr(comment.content_object, recipient)
    if user.is_authenticated:
        if user == content_object_user or user == comment.author:
            comment.delete()
        return redirect(next_url)
    return redirect('/login')