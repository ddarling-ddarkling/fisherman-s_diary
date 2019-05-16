from django import forms
from .models import Diary


class DiaryForm(forms.ModelForm):

    class Meta:
        model = Diary
        fields = ('name', 'description',)