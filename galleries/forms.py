from django import forms
from .models import Gallery


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['name', 'status']
        

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(GalleryForm, self).__init__(*args, **kwargs)
        

    def save(self, commit=True):
        instance = super(GalleryForm, self).save(commit=False)
        instance.creator = self.user
        if commit:
            instance.save()
        return instance