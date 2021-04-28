from django import forms
from .models import Notification


class MarkSeenForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['seen']


    def save(self, commit=True):
        self.instance 
        self.instance.seen = True
        if commit:
            self.instance.save()
        return self.instance