from django import forms
from bread.models import Leaven, FlourInLeaven


class FlourInLeavenForm(forms.ModelForm):
    class Meta:
        model = FlourInLeaven
        fields = ['flour', 'grams']


class LeavenForm(forms.ModelForm):
    class Meta:
        model = Leaven
        exclude = ['flour']