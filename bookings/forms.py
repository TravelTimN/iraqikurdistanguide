from django import forms
from django.forms.widgets import (
    EmailInput, NumberInput, PasswordInput, TextInput, URLInput
)
from .models import Booking


class DateInput(forms.DateInput):
    input_type = "date"


class BookingForm(forms.ModelForm):
    """
        Form to allow admins to manage Bookings.
    """
    class Meta:
        model = Booking
        fields = "__all__"
        widgets = {
            "start_date": DateInput(),
            "end_date": DateInput(),
            "itinerary": forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # add placeholder for floating-label functionality
        # (email, number, password, search, tel, text, url)
        valid_types = (EmailInput, NumberInput, PasswordInput, TextInput, URLInput)
        for field in self.fields:
            this_widget = self.fields[field].widget
            # DateInput subclasses TextInput, so exclude them
            if isinstance(this_widget, valid_types) and not isinstance(this_widget, DateInput):  # noqa
                this_widget.attrs["placeholder"] = field
            if field != "is_visible" and field != "itinerary":
                this_widget.attrs["class"] = "form-control"
            if field == "total_guests":
                this_widget.attrs["min"] = 1
                this_widget.attrs["max"] = 21

        # generate list of available currencies
        self.fields["currency"].choices = [("", "Currency"),] + list(self.fields["currency"].choices)[1:]
