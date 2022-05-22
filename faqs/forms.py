from django import forms
from tinymce.widgets import TinyMCE
from .models import FAQ


class FAQForm(forms.ModelForm):
    """
        Form to allow admins to manage FAQs.
    """
    answer = forms.CharField(widget=TinyMCE(attrs={"cols": 30, "rows": 15}))

    class Meta:
        model = FAQ
        fields = "__all__"
