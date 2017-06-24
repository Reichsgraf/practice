from django import forms
from .models import *

class CityForm(forms.ModelForm):
    city = forms.CharField(required=True)

    class Meta:
        model = City
        fields = [
            "city",
        ]
