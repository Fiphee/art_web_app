from django.shortcuts import redirect, reverse, Http404
from .models import Comment
from utils.constants import COMMENT_LIKE, REPLY, COMMENT
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def like_view(request, comment_id):
    user = request.user
    try:
        next_url = request.GET.get('next')
    except KeyError:
        next_url = '/'
        
    if user.is_authenticated:
        comment = Comment.objects.get(id=comment_id)
        comment.notify = {'user':user, 'recipient':comment.author, 'activity':COMMENT_LIKE}
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
    try:
        content_object_user = getattr(comment.content_object, recipient)
    except AttributeError:
        # If recipient from the url is not matching then the comment is a reply on another comment
        content_object_user = getattr(comment.content_object, 'author')
    
    if user.is_authenticated:
        if user == content_object_user or user == comment.author:
            comment_content_type = ContentType.objects.get(app_label='comments', model='Comment')
            if isinstance(comment.content_object, Comment):
                activity = REPLY
            else:
                activity = COMMENT
            comment.notify = {'user':user, 'recipient':content_object_user, 'activity':activity}
            comment.delete()
        return redirect(next_url)
    return redirect('/login')


@login_required
def reply_view(request, comment_id):
    if request.method == 'POST':
        try:
            comment = Comment.objects.get(id=comment_id)
            user = request.user
            body = request.POST.get('body')
            reply = Comment(author=user, body=body, content_object=comment)
            reply.notify = {'user':user, 'recipient':comment.author, 'activity':REPLY}
            reply.save()
            print('*'*300, 'its here')
            print('*'*300, reply)
            return JsonResponse({})
        except Comment.DoesNotExist:
            return Http404('No comment found. Maybe it was just deleted.')