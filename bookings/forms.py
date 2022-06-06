from django import forms
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
        # only for ModelChoiceField
        self.fields["currency"].choices = [("", "Currency"),] + list(self.fields["currency"].choices)[1:]
