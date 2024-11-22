# app1/forms.py
from django import forms
from .models import MenuImage  # Import the correct model

class MenuImageForm(forms.ModelForm):
    class Meta:
        model = MenuImage  # Your model name
        fields = ['menu_image']  # Field(s) for the form
