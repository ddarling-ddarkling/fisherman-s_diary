from django import forms
from .models import Diary


class DiaryForm(forms.ModelForm):

    class Meta:
        model = Diary
        fields = ('name', 'catch_date', 'fishing_time', 'weather', 'description', 'feeding_type', 'tackle_type', 'catch_type')