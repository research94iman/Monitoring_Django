# forms.py
from django import forms
from .models import TempData

class tempDataForm(forms.ModelForm):
    class Meta:
        model = TempData
        fields = ['name', 'value', 'date']