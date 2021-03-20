from django.db import models
from django.contrib.auth import get_user_model


AuthUserModel = get_user_model()


class CustomModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)