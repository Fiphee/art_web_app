from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from utils.notification import Notification


@receiver(user_logged_in)
def add_user_notifications_to_session(*args, **kwargs):
    user = kwargs.get('user')
    request = kwargs.get('request')
    Notification.load_count(user, request.session)
