from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save
from artworks.models import Artwork, ArtLike
from notifications.models import Notification
from utils.constants import UPLOAD


@receiver(m2m_changed, sender=ArtLike)
def liked_signal(instance, action, *args, **kwargs):
    if hasattr(instance, 'notify'):
        recipient = instance.notify.get('recipient')
        activity = instance.notify.get('activity')
        user = instance.notify.get('user')
        if action == 'post_remove':
            try:
                notification = instance.uploader.notifications.get(user=user, recipient=recipient, activity=activity, seen=False)
                notification.delete()
            except Notification.DoesNotExist:
                print('Notification was already seen')

        elif action == 'post_add':
            Notification(user=user, recipient=recipient, content_object=instance, activity=activity).save()


@receiver(post_save, sender=Artwork)
def artwork_uploaded_signal(instance, created, *args, **kwargs):
    uploader = instance.uploader
    for user_follow in uploader.followers.all():
        Notification(user=uploader, recipient=user_follow.user_followed_by, content_object=instance, activity=UPLOAD).save()
