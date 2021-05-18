from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from art_web_app.models import AuthUserModel
from .models import Profile, UserFollowing
from notifications.models import Notification


@receiver(post_save, sender=AuthUserModel)
def create_profile_signal(instance, created, **kwargs):
    if created:
        Profile(user=instance).save()