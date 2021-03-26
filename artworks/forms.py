from django import forms
from .models import Artwork, ArtCategory, Category


class ArtForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['title', 'description', 'image']

    category = forms.CharField(label='Categories')


    def clean_category(self):
        return self.cleaned_data['category']

