from django import forms
from django.forms.widgets import (
    EmailInput, NumberInput, PasswordInput, TextInput, URLInput
)
from .models import Province, Destination, Sight, Tour
from gallery.models import Photo


class DestinationForm(forms.ModelForm):
    """
        Form to allow admins to manage Destinations.
    """
    class Meta:
        model = Destination
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        # https://stackoverflow.com/a/72025478
        super().__init__(*args, **kwargs)

        # hide lat/lng by default (auto-generated from map selection)
        self.fields["latitude"].widget = forms.HiddenInput()
        self.fields["longitude"].widget = forms.HiddenInput()

        # add placeholder for floating-label functionality
        # (email, number, password, search, tel, text, url)
        valid_types = (EmailInput, NumberInput, PasswordInput, TextInput, URLInput)
        for field in self.fields:
            this_widget = self.fields[field].widget
            if isinstance(this_widget, valid_types):
                this_widget.attrs["placeholder"] = field
            if field != "is_visible":
                this_widget.attrs["class"] = "form-control"

        # generate list of provinces using optgroups
        self.fields["province"].choices = [["", "Select Province"]]
        regions = Province.REGION
        for k, v in regions:
            provinces = [
                f"{v}",
                [[p.id, p.name]
                    for p in Province.objects.filter(region=k)
                ]
            ]
            self.fields["province"].choices.append(provinces)


class SightForm(forms.ModelForm):
    """
        Form to allow admins to manage Sights.
    """
    class Meta:
        model = Sight
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        # https://stackoverflow.com/a/72025478
        super().__init__(*args, **kwargs)

        # hide lat/lng by default (auto-generated from map selection)
        self.fields["latitude"].widget = forms.HiddenInput()
        self.fields["longitude"].widget = forms.HiddenInput()

        # add placeholder for floating-label functionality
        for field in self.fields:
            if field != "is_visible" and field != "primary_attraction":
                self.fields[field].widget.attrs["class"] = "form-control"
            self.fields[field].widget.attrs["placeholder"] = field

        # generate list of categories
        self.fields["category"].choices = [["", "Select Category"]]
        categories = Sight.MARKER_TYPE
        for category in categories:
            self.fields["category"].choices.append(category)


class TourForm(forms.ModelForm):
    """
        Form to allow admins to manage Tours.
    """
    class Meta:
        model = Tour
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        # https://stackoverflow.com/a/72025478
        super().__init__(*args, **kwargs)

        # add placeholder for floating-label functionality
        for field in self.fields:
            if field != "is_visible":
                self.fields[field].widget.attrs["class"] = "form-control"
            self.fields[field].widget.attrs["placeholder"] = field

        # generate list of available photos, by destination
        self.fields["photo"].choices = [["", "Select Photo"]]
        destinations = Destination.objects.all()
        for destination in destinations:
            photos = [
                f"{destination.name}",
                [[p.id, p.image.url]
                    for p in Photo.objects.filter(sight__destination=destination)
                ]
            ]
            self.fields["photo"].choices.append(photos)
