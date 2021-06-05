from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from utils.notification import Notification, get_filter_arguments
from utils.constants import ART_LIKE, FOLLOW, COMMENT, COMMENT_LIKE, GALLERY_LIKE, GALLERY_FOLLOW, REPLY, UPLOAD, FILTER_BY_NOTIFICATION, FILTER_BY_ACTIVITY, FILTER_BY_CONTENT
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType


@login_required
def categories_view(request):
    user = request.user

    Notification.clear_session(request.session)
    activities = [ART_LIKE, FOLLOW, COMMENT, COMMENT_LIKE, GALLERY_LIKE, GALLERY_FOLLOW, REPLY, UPLOAD]
    notifications = {}
    for activity in activities:
        notification = user.notifications.filter(activity=activity, seen=False)
        notification_count = notification.count()
        if notification_count > 0:
            notifications[activity] = notification_count

    context = {
        'notifications':notifications,
        'filter':FILTER_BY_ACTIVITY,
        'mark_all':'unseen',
        'seen_argument':0,
    }

    return render(request, 'notifications/categories.html', context)


@login_required
def activity_view(request, activity):
    user = request.user

    if activity == FOLLOW:
        return redirect(reverse('notifications:content', args=(activity, request.user.id)))

    notifications = user.notifications.filter(activity=activity, seen=False)
    contents = {}
    if activity == UPLOAD:
        for notification in notifications:
            uploader = notification.user
            if uploader in contents:
                contents[uploader][0] += 1
            else:
                message = f'new upload by {notification.user}'
                contents[uploader] = [1, message, activity, uploader.id, notification.content_type.id]
    else:                
        for notification in notifications:
            content_object = notification.content_object 
            if content_object in contents:
                contents[content_object][0] += 1 
            else:
                message = notification.message  
                content_type_id = notification.content_type.id
                for comment_activity in [COMMENT, REPLY]:
                    if activity == comment_activity:
                        content_type_id = ContentType.objects.get(app_label='comments', model='Comment').id
                        

                contents[content_object] = [1, message, activity, content_object.id, content_type_id]

    page_obj = Paginator(list(contents.values()), 50)
    page_number = request.GET.get('page', 1)
    page = page_obj.get_page(page_number)

    context = {
        'notifications':contents,
        'filter':FILTER_BY_CONTENT,
        'mark_all':FILTER_BY_ACTIVITY,
        'seen_argument':activity,
        'page_url':reverse('notifications:activities', args=(activity,)),
        'page_obj':page_obj,
        'page':page,
    }
    return render(request, 'notifications/activities.html', context)


@login_required
def content_view(request, activity, content_id):
    user = request.user
    if activity == UPLOAD:
        notifications = user.notifications.filter(activity=activity, user=content_id, seen=False)
    else:
        notifications = user.notifications.filter(activity=activity, object_id=content_id, seen=False)
    page_obj = Paginator(notifications, 50)
    page_number = request.GET.get('page', 1)
    page = page_obj.get_page(page_number)
    context = {
        'notifications':notifications,
        'filter':FILTER_BY_NOTIFICATION,
        'mark_all':FILTER_BY_CONTENT,
        'seen_argument':content_id,
        'page_url':reverse('notifications:content', args=(activity, content_id)),
        'page_obj':page_obj,
        'page':page,
    }
    return render(request, 'notifications/content.html', context)


@login_required
def mark_as_seen(request, id_to_filter):
    filter_by = request.GET.get('filter_by')
    next_url = request.GET.get('next')
    content_type = request.GET.get('content_type')
    activity = request.GET.get('activity')
    user = request.user
    if id_to_filter == 0:
        notifications = user.notifications.filter(seen=False)
    else:
        filter_argument = get_filter_arguments(filter_by, id_to_filter, activity, content_type)
        notifications = user.notifications.filter(**filter_argument, seen=False)
    notifications.update(seen=True)

    return redirect(next_url)


@login_required
def seen_view(request):
    user = request.user
    notifications = user.notifications.filter(seen=True)
    page_obj = Paginator(notifications, 50)
    page_number = request.GET.get('page', 1)
    page = page_obj.get_page(page_number)
    context = {
        'notifications':notifications,
        'seen':True,
        'page_url':reverse('notifications:seen'),
        'page_obj':page_obj,
        'page':page,
    }
    return render(request, 'notifications/seen.html', context)


@login_required
def all_unseen_view(request):
    user = request.user
    notifications = user.notifications.filter(seen=False)
    page_obj = Paginator(notifications, 50)
    page_number = request.GET.get('page', 1)
    page = page_obj.get_page(page_number)
    context = {
        'notifications':notifications,
        'all_unseen':True,
        'filter':FILTER_BY_NOTIFICATION,
        'mark_all':'unseen',
        'seen_argument':0,
        'page_url':reverse('notifications:all_unseen'),
        'page_obj':page_obj,
        'page':page,
    }
    return render(request, 'notifications/all_unseen.html', context)


@login_required
def clear_seen_view(request):
    next_url = request.GET.get('next')
    user = request.user
    notifications = user.notifications.filter(seen=True).delete()
    return redirect(next_url)