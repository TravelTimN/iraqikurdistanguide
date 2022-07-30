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
        valid_types = (EmailInput, NumberInput, PasswordInput, TextInput, URLInput)
        for field in self.fields:
            this_widget = self.fields[field].widget
            if isinstance(this_widget, valid_types):
                this_widget.attrs["placeholder"] = field
            if field != "is_visible":
                if field == "sorani_script" or field == "arabic_script":
                    self.fields[field].widget.attrs["class"] = "form-control text-end"
                else:
                    self.fields[field].widget.attrs["class"] = "form-control"
