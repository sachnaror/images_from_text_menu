# app1/forms.py

from django import forms
from .models import MenuImage  # Import the model where menu images are stored

class MenuImageForm(forms.ModelForm):
    """
    Form for uploading menu images. This uses the MenuImage model
    to save the uploaded image.
    """

    class Meta:
        model = MenuImage  # Specify the model to use
        fields = ['menu_image']  # Include only the `menu_image` field in the form

    def clean_menu_image(self):
        """
        Custom validation for the `menu_image` field.
        """
        menu_image = self.cleaned_data.get('menu_image')

        # Restrict image size to 5MB
        if menu_image and menu_image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("The image file is too large. Max size is 5MB.")

        # Restrict allowed file types
        if menu_image and not menu_image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise forms.ValidationError("Only PNG, JPG, or JPEG files are allowed.")

        return menu_image
