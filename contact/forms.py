from django import forms
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
        for field in self.fields:
            if field != "destinations":
                self.fields[field].widget.attrs["class"] = "form-control"
            self.fields[field].widget.attrs["placeholder"] = field
            if field == "num_days":
                self.fields[field].widget.attrs["min"] = 1
                self.fields[field].widget.attrs["max"] = 60
            if field == "num_guests":
                self.fields[field].widget.attrs["min"] = 1
                self.fields[field].widget.attrs["max"] = 21
