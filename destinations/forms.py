from django import forms
from .models import Destination


class DestinationForm(forms.ModelForm):
    """
        Form to allow admins to manage Destinations.
    """
    class Meta:
        model = Destination
        fields = "__all__"
