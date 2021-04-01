from django import forms
from .models import Artwork, ArtCategory, Category


class ArtForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['title', 'description', 'image']

    categories = forms.CharField(label='Categories')


    def save(self, commit=True):
        instance = super(ArtForm, self).save(commit=False)
        instance.uploader = self.user
        if commit:
            instance.save()
            tags = [tag.lower() for tag in self.cleaned_data['categories'].replace(' ', '').split(',')]
            for tag in tags:
                category = Category.objects.filter(name=tag)
                if category.exists():
                    instance.category.add(category[0])
                else:
                    category = Category.objects.create(name=tag)
                    category.save()
                    instance.category.add(category)
        return instance


    def set_user(self, user):
        self.user = user
