from django import forms
from bread.models import Leaven, FlourInLeaven


class FlourInLeavenForm(forms.ModelForm):
    class Meta:
        model = FlourInLeaven
        fields = ['grams', 'flour']


class LeavenForm(forms.ModelForm):
    class Meta:
        model = Leaven
        exclude = ['flour']