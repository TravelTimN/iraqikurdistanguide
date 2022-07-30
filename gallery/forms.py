from django import forms
from django.forms.widgets import (
    EmailInput, NumberInput, PasswordInput, TextInput, URLInput
)
from .models import Photo
from destinations.models import Destination, Sight


class PhotoForm(forms.ModelForm):
    """
        Form to allow admins to manage Photos.
    """

    image = forms.ImageField(required=True)
    class Meta:
        model = Photo
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # add placeholder for floating-label functionality
        # (email, number, password, search, tel, text, url)
        for field in self.fields:
            if isinstance(self.fields[field].widget, (EmailInput, NumberInput, PasswordInput, TextInput, URLInput)):  # noqa
                self.fields[field].widget.attrs["placeholder"] = field
            if field != "is_visible":
                self.fields[field].widget.attrs["class"] = "form-control"

        # generate list of destinations using optgroups
        self.fields["sight"].choices = [["", "Select Sight"]]
        destinations = Destination.objects.all()
        for destination in destinations:
            sights = [
                f"{destination}",
                [[sight.id, sight.name]
                    for sight in Sight.objects.filter(destination=destination)
                ]
            ]
            self.fields["sight"].choices.append(sights)
