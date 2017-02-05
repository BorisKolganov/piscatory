from django import forms
from adverts.models import Advert


class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = ['header', 'text', 'city', 'address', 'price', 'type', 'photo']

    photo = forms.ImageField(required=False)