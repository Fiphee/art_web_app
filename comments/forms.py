from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        fields = ['body']