from django.db import models
from art_web_app.models import CustomModel, AuthUserModel
from utils.constants import ART_LIKE, COMMENT, COMMENT_LIKE, GALLERY_FOLLOW, GALLERY_LIKE, FOLLOW, REPLY, UPLOAD
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.shortcuts import reverse
from artworks.models import Artwork
from utils.notification import Notification as NotificationUtils


class Notification(CustomModel):
    user = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE)
    recipient = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE, related_name="notifications")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Types(models.IntegerChoices):
        gallery_like = GALLERY_LIKE
        gallery_follow = GALLERY_FOLLOW
        art_like = ART_LIKE
        follow = FOLLOW
        reply = REPLY
        comment = COMMENT
        comment_like = COMMENT_LIKE
        upload = UPLOAD

    activity = models.SmallIntegerField(choices=Types.choices)
    seen = models.BooleanField(default=False)


    class Meta:
        ordering = ['-id']


    def save(self, *args, **kwargs):
        if self.user != self.recipient:
            notification = Notification.objects.filter(user=self.user, recipient=self.recipient, activity=self.activity, object_id=self.object_id, content_type=self.content_type)
            if not notification.exists() or notification.exists() and self.activity in [COMMENT, REPLY]:
                super(Notification, self).save(*args, **kwargs)


    def __str__(self):
        return self._activity_text()


    def _activity_text(self):
        texts = {
            ART_LIKE: f' {self.content_object} liked by {self.user}',
            FOLLOW: f'{self.content_object} followed by {self.user}',
            COMMENT: f'{self.content_object} commented on by {self.user}',
            COMMENT_LIKE: f'{self.content_object} comment liked by {self.user}',
            GALLERY_LIKE: f'{self.content_object} gallery liked by {self.user}',
            GALLERY_FOLLOW: f'{self.content_object} gallery followed by {self.user}',
            REPLY: f'{self.content_object} reply by {self.user}',
            UPLOAD: f'{self.content_object} uploaded by {self.user}'
        }
        return texts[self.activity]


    @property
    def message(self):
        texts = {
            ART_LIKE: f'liked your artwork "{self.content_object}"!',
            FOLLOW: f'followed you!',
            COMMENT: f'commented on "{self.content_object}"!',
            COMMENT_LIKE: f'liked your {self.content_object}!',
            GALLERY_LIKE: f'liked your gallery "{self.content_object}"!',
            GALLERY_FOLLOW: f'followed your gallery "{self.content_object}"!',
            REPLY: f'replied to you with "{getattr(self.content_object, "body", "")[0:25] + "..."}"',
            UPLOAD: f'uploaded art "{self.content_object}"',
        }
        return texts[self.activity]

    @property
    def activity_url(self):
        texts = {
            ART_LIKE: ('artworks:view', self.content_object.id),
            FOLLOW: ('users:profile', self.user),
            COMMENT: (None, self.content_object),
            COMMENT_LIKE: (None, self.content_object),
            GALLERY_LIKE: ('galleries:view', self.content_object.id),
            GALLERY_FOLLOW: ('galleries:view', self.content_object.id),
            REPLY: (None, self.content_object),
            UPLOAD: ('artworks:view', self.content_object.id),
        }

        url, args = texts[self.activity]      
        return NotificationUtils.get_content_url(url, args)

