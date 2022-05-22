from django import forms
from .models import Photo


class PhotoForm(forms.ModelForm):
    """
        Form to allow admins to manage Photos.
    """
    class Meta:
        model = Photo
        fields = "__all__"
