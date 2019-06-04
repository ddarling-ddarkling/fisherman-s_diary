from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = (
            'user_photo',
            'region',
            'bio',
            'birthday',
        )
        labels = {
            'user_photo': 'Ваша фотография:',
            'region': 'Регион:',
            'bio': 'О себе:',
            'birthday': 'День рождения:',
        }
        widgets = {
            'birthday': forms.DateInput(attrs={'class': 'datepicker'}),
        }
