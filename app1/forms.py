from django import forms

class MenuUploadForm(forms.Form):
    menu_image = forms.ImageField()
