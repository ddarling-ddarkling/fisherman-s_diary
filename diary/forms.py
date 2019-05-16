from django import forms
from .models import Diary


class DiaryForm(forms.ModelForm):

    class Meta:
        model = Diary
        fields = ('name', 'catch_date', 'description', 'feeding_type')