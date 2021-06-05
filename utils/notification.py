from django.shortcuts import reverse
import json
from .constants import FILTER_BY_NOTIFICATION, FILTER_BY_CONTENT, FILTER_BY_ACTIVITY, UPLOAD


class Notification:
    @staticmethod
    def clear_session(session):
        session['notification_count'] = 0


    @staticmethod
    def load_count(user, session):
        unseen_notifications = user.notifications.filter(seen=False)
        session['notification_count'] = unseen_notifications.count()


    @staticmethod
    def _get_content_url(content):
        artwork_model = 'Artwork'
        profile_model = 'Profile' 
        urls = {
            artwork_model:('artworks:view', content.id),
            profile_model:('users:profile', content),
        }

        for class_type in [artwork_model, profile_model]:
            if content.__class__.__name__ == class_type:
                url, args = urls[class_type]
                return reverse(url, args=(args,))


    @staticmethod
    def get_content_url(url=None, content=None):
        if not url:
            if content.__class__.__name__ != 'Comment':
                return Notification._get_content_url(content)
            return Notification.get_content_url(content=content.content_object)
        
        return reverse(url, args=(content,))


def get_filter_arguments(filter_key, filter_value, activity, content_type):
    if activity == str(UPLOAD):
        filter_arguments = {
            'user_id':filter_value,
            'content_type_id':content_type,
            'activity':activity
        }
        return filter_arguments

    arguments = {
        FILTER_BY_NOTIFICATION:'id',
        FILTER_BY_CONTENT:'object_id',
        FILTER_BY_ACTIVITY:'activity',
    }

    filter_arguments = {
        arguments[filter_key]:filter_value,
    }
    if activity:
        filter_arguments['activity'] = activity
    return filter_arguments
