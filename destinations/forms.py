from django import forms
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
        widgets = {"destination": forms.HiddenInput(),}
        fields = "__all__"


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
