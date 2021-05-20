from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save, post_delete
from comments.models import CommentLikes, Comment
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType


@receiver(m2m_changed, sender=CommentLikes)
def comment_liked_signal(instance, action, *args, **kwargs):
    if hasattr(instance, 'notify'):
        # Notify consists of user, recipient and activity defined in the comments like view
        if action == 'post_remove':
            try:
                notification = instance.author.notifications.get(**instance.notify, seen=False)
                notification.delete()
            except Notification.DoesNotExist:
                print('Notification was already seen')

        elif action == 'post_add':
            Notification(**instance.notify, content_object=instance).save()
        

@receiver(post_save, sender=Comment)
def comment_created_signal(instance, created, *args, **kwargs):
    if hasattr(instance, 'notify') and created:
        Notification(**instance.notify, content_object=instance).save()


@receiver(post_delete, sender=Comment)
def comment_deleted_signal(instance, *args, **kwargs):
    if hasattr(instance, 'notify'):
        try:
            comment_content_type = ContentType.objects.get(app_label='comments', model='Comment')
            notification = Notification.objects.get(**instance.notify, object_id=instance.id, content_type=comment_content_type)
            notification.delete()
        except Notification.DoesNotExist:
            print("Notification does not exist")