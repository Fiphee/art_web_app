from django.db.models.signals import post_save
from django.dispatch import receiver
from art_web_app.models import AuthUserModel
from .models import Profile


@receiver(post_save, sender=AuthUserModel)
def update_profile_signal(instance, created, **kwargs):
    if created:
        instance.profile.save()