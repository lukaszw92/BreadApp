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
            'date': forms.DateInput(format=('%d-%m-%Y'),
            attrs={'firstDay': 1, 'pattern=': '\d{4}-\d{2}-\d{2}', 'lang': 'pl',
            'format': 'yyyy-mm-dd', 'type': 'date'}),
        }
