from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.core.paginator import Paginator
from .forms import RegisterForm, ProfileSettingsForm, UserSettingsForm
from .models import Profile, AuthUserModel, UserFollowing
from utils.notification import Notification
from utils.constants import FOLLOW, COMMENT
from comments.forms import CommentForm
from comments.models import Comment
from utils.comment import CommentUtils
from notifications.models import Notification as NotificationModel
from django.http import JsonResponse


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

    return render(request, "users/register.html", context)


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
                    return redirect(reverse('users:profile', args=(user.username,)))
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
    if username == request.user.username:
        user = request.user
    else:
        user = get_object_or_404(AuthUserModel, username=username)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                comment = Comment(author=request.user, body=form.cleaned_data['body'], content_object=user.profile)
                comment.notify = {'user':request.user, 'recipient':user, 'activity':COMMENT}
                comment.save()
                return redirect(reverse('users:profile', args=(user,)))
            return redirect(reverse('users:login'))
    else:
        form = CommentForm()
        artworks = []
        total_likes = 0
        try:
            for art in user.artworks.all():
                artworks.append(art)
                total_likes += art.likes.count()
        except AttributeError:
            print("User has no artworks")

        page_obj = Paginator(artworks, 8)
        page_number = request.GET.get('page', 1)
        page = page_obj.get_page(page_number)
        context = {
            'visited_user':user,
            'page_obj':page_obj,
            'page':page,
            'page_url':reverse('users:profile', args=(username,))+'?page=',
            'total_art_likes':total_likes,
            'already_following':False,
            'url_user':username,
            'comments': user.profile.comments.all(),
            'form':form,
            'comment_util': CommentUtils('user', reverse('users:profile', args=(user,)), request.user == user)
        }

        if request.user.is_authenticated:
            already_following = user.followers.filter(user_followed_by=request.user).first()
            if already_following:
                context['already_following'] = True
        

    return render(request, "users/profile.html", context)


def follow_view(request, artist_id):
    user = request.user
    if user.is_authenticated:
        if artist_id != request.user.id:
            artist = AuthUserModel.objects.get(id=artist_id)
            followed = UserFollowing.objects.filter(user=artist, user_followed_by=user).first()
            if followed:
                followed.delete()
                follow = False
                try:
                    notification = artist.notifications.filter(user=user, activity=FOLLOW, seen=False)
                    notification.delete()
                except:
                    print('Notification already seen by user')
            else:
                UserFollowing(user_followed_by=user, user=artist).save()
                artist.notifications.create(user=user, content_object=artist, activity=FOLLOW).save()
                follow = True
        return JsonResponse({"followed":follow, "followers_nr":artist.followers.count()})
    return JsonResponse({"redirect_url": reverse('users:login')})


def user_galleries_view(request, username):
    if username == request.user.username:
        user = request.user
    else:
        user = get_object_or_404(AuthUserModel, username=username)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                comment = Comment(author=request.user, body=form.cleaned_data['body'], content_object=user.profile)
                comment.notify = {'user':request.user, 'recipient':user, 'activity':COMMENT}
                comment.save()
                return redirect(reverse('users:galleries', args=(user,)))
            return redirect(reverse('users:login'))

    else:
        form = CommentForm()
        galleries = []
        total_artworks_in_gallery = 0
        try:
            for gallery in user.galleries.all():
                galleries.append(gallery)
                total_artworks_in_gallery += gallery.artworks.count()
        except AttributeError:
            print("User has no galleries")

        page_obj = Paginator(galleries, 8)
        page_number = request.GET.get('page', 1)
        page = page_obj.get_page(page_number)

        context = {
            'visited_user':user,
            'page_obj':page_obj,
            'page':page,
            'page_url':reverse('users:galleries', args=(username,)),
            'comments': user.profile.comments.all(),
            'form':form,
            'comment_util': CommentUtils('user', reverse('users:galleries', args=(user,)), request.user == user)
        }
        if request.user.is_authenticated:
            already_following = user.followers.filter(user_followed_by=request.user).first()
            context['already_following'] = already_following


        return render(request, "users/galleries.html", context)
