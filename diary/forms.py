from django import forms
from .models import Diary, Comment


class DiaryForm(forms.ModelForm):

    class Meta:
        model = Diary
        fields = (
            'name',
            'catch_date',
            'fishing_time',
            'weather',
            'place',
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
            'place': 'Место:',
            'description': 'Описание:',
            'feeding_type': 'Тип прикорма:',
            'tackle_type': 'Тип снасти:',
            'catch_type': 'Тип улова:',
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = {
            'description',
        }
        labels = {
            'description': 'Текст комментария:',
        }
