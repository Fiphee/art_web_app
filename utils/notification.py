import json
from notifications.models import Notification as NotificationModel
from .constants import FILTER_BY_NOTIFICATION, FILTER_BY_CONTENT, FILTER_BY_ACTIVITY


class Notification:
    @staticmethod
    def clear_session(session):
        session['notification_count'] = 0


    @staticmethod
    def load_count(user, session):
        unseen_notifications = user.notifications.filter(seen=False)
        session['notification_count'] = unseen_notifications.count()


def get_filter_argument(filter_key, filter_value):
    arguments = {
        FILTER_BY_NOTIFICATION:'id',
        FILTER_BY_CONTENT:'object_id',
        FILTER_BY_ACTIVITY:'activity',
    }

    filter_argument = {
        arguments[filter_key]:filter_value,
    }
    return filter_argument
