from django import forms
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
        # https://stackoverflow.com/a/72025478
        super().__init__(*args, **kwargs)
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
