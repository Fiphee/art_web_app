from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save
from artworks.models import Artwork, ArtLike, Color, Category
from notifications.models import Notification
from utils.constants import UPLOAD, COLOR_THRESHOLD
from utils.colors import get_colors, get_best_category
from math import sqrt


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
    if created:
        uploader = instance.uploader
        for user_follow in uploader.followers.all():
            Notification(user=uploader, recipient=user_follow.user_followed_by, content_object=instance, activity=UPLOAD).save()

        color_palette = get_colors(instance.thumbnail.path) 
        
        create_category = lambda r,g,b: Category.objects.create(name=f'rgb({r}, {g}, {b})')
        
        for color in color_palette:
            r,g,b = color
            threshold = COLOR_THRESHOLD
            find_similar_args = {
                'r__lte':r+threshold,
                'r__gte':r-threshold,
                'g__lte':g+threshold,
                'g__gte':g-threshold,
                'b__lte':b+threshold,
                'b__gte':b-threshold,
            }
            
            try:  
                color_obj = Color.objects.get(r=r,g=g,b=b)
                instance.colors.add(color_obj)
            except Color.DoesNotExist:
                similar_colors = Color.objects.filter(**find_similar_args)
                if similar_colors.exists():  # check if similar colors have fitting categories
                    category = get_best_category(color, similar_colors)
                    if not category:
                        category = create_category(r,g,b)

                    current_color = Color.objects.create(r=r,g=g,b=b, category=category)
                else: 
                    category = create_category(r,g,b)
                    current_color = Color.objects.create(r=r,g=g,b=b, category=category)

                instance.colors.add(current_color)
        
