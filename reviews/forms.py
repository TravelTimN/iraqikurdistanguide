from django import forms
from django.forms.widgets import (
    EmailInput, NumberInput, PasswordInput, TextInput, URLInput
)
from tinymce.widgets import TinyMCE
from .models import Review, Source


class DateInput(forms.DateInput):
    input_type = "date"


class ReviewForm(forms.ModelForm):
    """
        Form to allow admins to manage Reviews.
    """
    class Meta:
        model = Review
        fields = "__all__"
        widgets = {
            "date": DateInput(),
            "review": TinyMCE(),
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
            if field != "is_visible":
                this_widget.attrs["class"] = "form-control"

        # ratings selection
        self.fields["rating"].choices = [("", "Rating"),] + list(self.fields["rating"].choices)[1:]

        # generate list of available sources
        self.fields["source"].choices = [["", "Source"]]
        sources = Source.objects.all()
        for source in sources:
            self.fields["source"].choices.append((source.id, source.name))
