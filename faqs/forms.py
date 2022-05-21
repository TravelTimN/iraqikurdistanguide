from django import forms
from .models import FAQ


class FAQForm(forms.ModelForm):
    """
        Form to allow admins to manage FAQs.
    """
    class Meta:
        model = FAQ
        fields = "__all__"
