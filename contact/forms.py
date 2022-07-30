from django import forms
from django.forms.widgets import (
    EmailInput, NumberInput, PasswordInput, TextInput, URLInput
)
from .models import Contact
from destinations.models import Destination


class DateInput(forms.DateInput):
    input_type = "date"


class ContactForm(forms.ModelForm):
    """
        Form to allow users to submit a contact to site admins.
    """

    destinations = forms.ModelMultipleChoiceField(
        queryset = Destination.objects.filter(is_visible=True),
        widget = forms.CheckboxSelectMultiple(attrs={"class": "list-unstyled"}),
        required = True,
    )
    class Meta:
        model = Contact
        widgets = {
            "start_date": DateInput(),
        }
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """ Add placeholders to use floating-labels in Bootstrap5 """
        super().__init__(*args, **kwargs)

        # add placeholder for floating-label functionality
        # (email, number, password, search, tel, text, url)
        valid_types = (EmailInput, NumberInput, PasswordInput, TextInput, URLInput)
        for field in self.fields:
            this_widget = self.fields[field].widget
            # DateInput subclasses TextInput, so exclude them
            if isinstance(this_widget, valid_types) and not isinstance(this_widget, DateInput):  # noqa
                this_widget.attrs["placeholder"] = field
            if field != "destinations":
                this_widget.attrs["class"] = "form-control"
            if field == "num_days":
                self.fields[field].widget.attrs["min"] = 1
                self.fields[field].widget.attrs["max"] = 60
            if field == "num_guests":
                self.fields[field].widget.attrs["min"] = 1
                self.fields[field].widget.attrs["max"] = 21
