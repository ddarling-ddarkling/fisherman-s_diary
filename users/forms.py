from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'region',
            'bio',
            'birthday',
        )
        labels = {
            'region': 'Регион:',
            'bio': 'О себе:',
            'birthday': 'День рождения:',
        }
        widgets = {
            'birthday': forms.DateInput(attrs={'class': 'datepicker'}),
        }
