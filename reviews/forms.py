from django import forms
from tinymce.widgets import TinyMCE
from .models import Review


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
            # setting 'format' causes UPDATE form to break date
            # "date": DateInput(attrs={"class": "datepicker"}, format="%d/%m/%Y"),
            "review": TinyMCE(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # only for ModelChoiceField
        self.fields["rating"].choices = [("", "Rating"),] + list(self.fields["rating"].choices)[1:]
        # for ChoiceFields
        self.fields["source"].empty_label = "Source"
