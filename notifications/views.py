from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from utils.notification import Notification, get_filter_argument
from utils.constants import ART_LIKE, FOLLOW, COMMENT, COMMENT_LIKE, GALLERY_LIKE, GALLERY_FOLLOW, REPLY, FILTER_BY_NOTIFICATION, FILTER_BY_ACTIVITY, FILTER_BY_CONTENT


@login_required
def categories_view(request):
    user = request.user

    Notification.clear_session(request.session)
    activities = [ART_LIKE, FOLLOW, COMMENT, COMMENT_LIKE, GALLERY_LIKE, GALLERY_FOLLOW, REPLY]
    notifications = {}
    for activity in activities:
        notification = user.notifications.filter(activity=activity, seen=False)
        notification_count = notification.count()
        if notification_count > 0:
            notifications[activity] = notification_count

    context = {
        'notifications':notifications,
        'filter':FILTER_BY_ACTIVITY
    }

    return render(request, 'notifications/categories.html', context)


@login_required
def activity_view(request, activity):
    user = request.user

    if activity == FOLLOW:
        return redirect(reverse('notifications:content', args=(activity, request.user.id)))
        
    notifications = user.notifications.filter(activity=activity, seen=False)
    contents = {}
    for notification in notifications:
        content_object = notification.content_object 
        if content_object in contents:
            contents[content_object][0] += 1 
        else:
            contents[content_object] = [1, notification.message, activity, content_object.id]

    context = {
        'notifications':contents,
        'filter':FILTER_BY_CONTENT
    }

    return render(request, 'notifications/activities.html', context)


@login_required
def content_view(request, activity, content_id):
    user = request.user
    notifications = user.notifications.filter(activity=activity, object_id=content_id, seen=False)
    context = {
        'notifications':notifications,
        'filter':FILTER_BY_NOTIFICATION
    }
    return render(request, 'notifications/content.html', context)


@login_required
def mark_as_seen(request, id_to_filter):
    filter_by = request.GET.get('filter_by')
    next_url = request.GET.get('next')
    user = request.user
    filter_argument = get_filter_argument(filter_by, id_to_filter)
    notifications = user.notifications.filter(**filter_argument, seen=False)
    notifications.update(seen=True)

    return redirect(next_url)


@login_required
def seen_view(request):
    user = request.user
    notifications = user.notifications.filter(seen=True)
    context = {
        'notifications':notifications,
        'seen':True
    }
    return render(request, 'notifications/seen.html', context)


@login_required
def all_unseen_view(request):
    user = request.user
    notifications = user.notifications.filter(seen=False)
    context = {
        'notifications':notifications,
        'all_unseen':True,
        'filter':FILTER_BY_NOTIFICATION
    }
    return render(request, 'notifications/all_unseen.html', context)