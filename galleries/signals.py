from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from galleries.models import UserFollowedGallery
from notifications.models import Notification


@receiver(m2m_changed, sender=UserFollowedGallery)
def gallery_follow_signal(instance, action, *args, **kwargs):
    if hasattr(instance, 'notify'):
        # Notify consists of user, recipient and activity defined in the follow view
        if action == 'post_remove':
            try:
                notification = instance.creator.notifications.get(**instance.notify, seen=False)
                notification.delete()
            except Notification.DoesNotExist:
                print('Notification was already seen')

        elif action == 'post_add':
            Notification(**instance.notify, content_object=instance).save()
        