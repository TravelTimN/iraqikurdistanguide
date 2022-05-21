from django import forms
from .models import Destination, Site, Province


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


class SiteForm(forms.ModelForm):
    """
        Form to allow admins to manage Sites.
    """
    class Meta:
        model = Site
        widgets = {"destination": forms.HiddenInput(),}
        fields = "__all__"
