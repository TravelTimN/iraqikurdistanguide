from django import forms
from .models import Contact


class DateInput(forms.DateInput):
    input_type = "date"


class ContactForm(forms.ModelForm):
    """
        Form to allow users to submit a contact to site admins.
    """

    class Meta:
        model = Contact
        widgets = {
            "start_date": DateInput(),
        }
        fields = "__all__"
