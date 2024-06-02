from django import forms
from django.forms.widgets import (
    DateInput, EmailInput, NumberInput, PasswordInput, TextInput, URLInput
)
from .models import Itinerary, ItineraryDay
from destinations.models import Province, Destination


class ItineraryForm(forms.ModelForm):
    """
        Form to allow admins to manage Itineraries.
    """
    class Meta:
        model = Itinerary
        fields = "__all__"

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
            if field != "is_visible":
                this_widget.attrs["class"] = "form-control"


class ItineraryDayForm(forms.ModelForm):
    """
        Form to allow admins to manage Itinerary Days.
    """
    class Meta:
        model = ItineraryDay
        fields = ("day_number", "headline", "plan", "destinations", "overnight_city", "hotel")  # noqa
        widgets = {
            "destinations": forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # add placeholder for floating-label functionality
        # (email, number, password, search, tel, text, url)
        valid_types = (EmailInput, NumberInput, PasswordInput, TextInput, URLInput)  # noqa
        for field in self.fields:
            this_widget = self.fields[field].widget
            # DateInput subclasses TextInput, so exclude them
            if isinstance(this_widget, valid_types) and not isinstance(this_widget, DateInput):  # noqa
                this_widget.attrs["placeholder"] = field
            if field == "plan":
                this_widget.attrs["placeholder"] = "Today's Agenda"
            if field != "destinations":
                this_widget.attrs["class"] = "form-control"
            if field == "day_number":
                this_widget.attrs["min"] = 1
                this_widget.attrs["readonly"] = True

        self.fields["overnight_city"].choices = self.get_overnight_city_choices()  # noqa

    def get_overnight_city_choices(self):
        # generate optgroups for overnight city destinations by region
        choices = {
            "Kurdistan": [],
            "Iraq": []
        }
        provinces = Province.objects.all()
        for province in provinces:
            region_name = province.get_region_display()
            destinations = Destination.objects.filter(province=province).order_by("name").values_list("id", "name")  # noqa
            if destinations:
                choices[region_name].extend([(dest_id, dest_name) for dest_id, dest_name in destinations])  # noqa
        
        # build the final choices list with optgroups
        final_choices = [("", "Overnight City")] + [
            ("Kurdistan", sorted(choices["Kurdistan"], key=lambda x: x[1])),
            ("Iraq", sorted(choices["Iraq"], key=lambda x: x[1]))
        ]
        return final_choices
