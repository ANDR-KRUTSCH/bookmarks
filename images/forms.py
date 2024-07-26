import requests

from django import forms
from django.utils.text import slugify
from django.core.files.base import ContentFile

from .models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
        }

    def clean_url(self) -> str:
        url: str = self.cleaned_data.get('url')
        extension = url.split('.')[-1]
        if extension.lower() not in ['jpg', 'jpeg', 'png']:
            raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url
    
    def save(self, commit: bool = True) -> Image:
        image: Image = super().save(commit=False)
        image_url: str = self.cleaned_data.get('url')
        name = slugify(value=image.title)
        extension = image_url.split('.')[-1]
        image_name = f'{name}.{extension.lower()}'
        response = requests.get(url=image_url)
        print(response.status_code)
        image.image.save(name=image_name, content=ContentFile(response.content), save=False)
        if commit:
            image.save()
        return image