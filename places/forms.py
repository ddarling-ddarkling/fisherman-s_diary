from django import forms
from .models import Place


class PlaceForm(forms.ModelForm):

    class Meta:
        model = Place
        fields = {
            'name',
            'visibility',
            'latitude',
            'longitude',
            'description',
        }
        labels = {
            'name': 'Название:',
            'visibility': 'Кому видно место:',
            'latitude': 'Широта:',
            'longitude': 'Долгота:',
            'description': 'Описание:',
        }
