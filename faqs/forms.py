from django import forms
from tinymce.widgets import TinyMCE
from .models import FAQ


class FAQForm(forms.ModelForm):
    """
        Form to allow admins to manage FAQs.
    """
    answer = forms.CharField(widget=TinyMCE(attrs={"cols": 30, "rows": 15}))

    class Meta:
        model = FAQ
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        # https://stackoverflow.com/a/72025478
        super().__init__(*args, **kwargs)

        # add placeholder for floating-label functionality
        for field in self.fields:
            if field != "is_visible":
                self.fields[field].widget.attrs["class"] = "form-control"
            if field == "answer":
                self.fields[field].widget.attrs["placeholder"] = "FAQ Answer"
            else:
                self.fields[field].widget.attrs["placeholder"] = field

        # generate list of available FAQ categories
        self.fields["category"].choices = [["", "Select Category"]]
        categories = FAQ.CATEGORIES
        for category in categories:
            self.fields["category"].choices.append(category)
