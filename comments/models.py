from django.db import models
from art_web_app.models import CustomModel, AuthUserModel
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Comment(CustomModel):
    author = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE)
    likes = models.ManyToManyField(AuthUserModel, through='CommentLikes', related_name='comments')
    body = models.TextField(blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    replies = GenericRelation('Comment')

    def __str__(self):
        return f'comment on "{self.content_object}"'


    def __repr__(self):
        return self.__str__()


class CommentLikes(CustomModel):
    user = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)