from django import forms
from bread.models import Leaven, FlourInLeaven, Bread, FlourInBread


class FlourInLeavenForm(forms.ModelForm):
    class Meta:
        model = FlourInLeaven
        fields = ['flour', 'grams']


class LeavenForm(forms.ModelForm):
    class Meta:
        model = Leaven
        exclude = ['flour']


class FlourInBreadForm(forms.ModelForm):
    class Meta:
        model = FlourInBread
        fields = ['flour', 'grams']


class BreadForm(forms.ModelForm):
    class Meta:
        model = Bread
        exclude = ['flour_mix', 'user']
        widgets = {
            'date': forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date'}),
        }
