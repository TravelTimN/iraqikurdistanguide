from django import forms
from django.forms.widgets import (
    EmailInput, NumberInput, PasswordInput, TextInput, URLInput
)
from .models import Phrase


class PhraseForm(forms.ModelForm):
    """
        Form to allow admins to manage Phrases.
    """
    class Meta:
        model = Phrase
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].choices = [("", "Select Category"),] + list(self.fields["category"].choices)[1:]  # noqa

        # add placeholder for floating-label functionality
        # (email, number, password, search, tel, text, url)
        for field in self.fields:
            if isinstance(self.fields[field].widget, (EmailInput, NumberInput, PasswordInput, TextInput, URLInput)):  # noqa
                self.fields[field].widget.attrs["placeholder"] = field
            if field != "is_visible":
                if field == "sorani_script" or field == "arabic_script":
                    self.fields[field].widget.attrs["class"] = "form-control text-end"
                else:
                    self.fields[field].widget.attrs["class"] = "form-control"
