from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from artworks.models import Artwork, ArtLike
from notifications.models import Notification


@receiver(m2m_changed, sender=ArtLike)
def liked_signal(instance, action, *args, **kwargs):
    if hasattr(instance, 'notify'):
        recipient = instance.notify.get('recipient')
        activity = instance.notify.get('activity')
        user = instance.notify.get('user')
        if action == 'post_remove':
            print('#'*200, 'disliking')
            try:
                notification = instance.uploader.notifications.get(user=user, recipient=recipient, activity=activity, seen=False)
                notification.delete()
            except Notification.DoesNotExist:
                print('Notification was already seen')

        elif action == 'post_add':
            print('*'*200, 'liking')
            Notification(user=user, recipient=recipient, content_object=instance, activity=activity).save()
        