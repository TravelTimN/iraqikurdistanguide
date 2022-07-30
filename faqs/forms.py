from django import forms
from django.forms.widgets import (
    EmailInput, NumberInput, PasswordInput, TextInput, URLInput
)
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

    def __init__(self, *args, **kwargs):
        # https://stackoverflow.com/a/72025478
        super().__init__(*args, **kwargs)

        # add placeholder for floating-label functionality
        # (email, number, password, search, tel, text, url)
        valid_types = (EmailInput, NumberInput, PasswordInput, TextInput, URLInput)
        for field in self.fields:
            this_widget = self.fields[field].widget
            if isinstance(this_widget, valid_types):
                this_widget.attrs["placeholder"] = field
            if field == "answer":
                this_widget.attrs["placeholder"] = "FAQ Answer"
            if field != "is_visible":
                this_widget.attrs["class"] = "form-control"

        # generate list of available FAQ categories
        self.fields["category"].choices = [["", "Select Category"]]
        categories = FAQ.CATEGORIES
        for category in categories:
            self.fields["category"].choices.append(category)
