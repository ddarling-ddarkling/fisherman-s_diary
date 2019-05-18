from django import forms
from .models import Diary


class DiaryForm(forms.ModelForm):

    class Meta:
        model = Diary
        fields = (
            'name',
            'catch_date',
            'fishing_time',
            'weather',
            'description',
            'feeding_type',
            'tackle_type',
            'catch_type',
        )
        labels = {
            'name': 'Название:',
            'catch_date': 'Дата рыбалки:',
            'fishing_time': 'Время суток:',
            'weather': 'Погода:',
            'description': 'Описание:',
            'feeding_type': 'Тип прикорма:',
            'tackle_type': 'Тип снасти:',
            'catch_type': 'Тип улова:',
        }
