from django.db import models
from art_web_app.models import CustomModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Comment(CustomModel):
    author = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE)
    likes = models.ManyToManyField(AuthUserModel, through='CommentLikes', related_name='comments')
    body = models.TextField(blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class CommentLikes(CustomModel):
    user = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)