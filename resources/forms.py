from django import forms
from .models import Phrase


class PhraseForm(forms.ModelForm):
    """
        Form to allow admins to manage Phrases.
    """
    class Meta:
        model = Phrase
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].choices = [("", "Select Category"),] + list(self.fields["category"].choices)[1:]
        self.fields["english_phrase"].label = "English"
        self.fields["english_phrase"].widget.attrs["placeholder"] = "English Phrase"
        self.fields["sorani_script"].label = "کوردی (سۆرانی)"
        self.fields["sorani_script"].widget.attrs["placeholder"] = "Kurdish Sorani Script"
        self.fields["sorani_latin"].label = "Kurdi (Sorani)"
        self.fields["sorani_latin"].widget.attrs["placeholder"] = "Kurdish Sorani Letters"
        self.fields["arabic_script"].label = "عربي"
        self.fields["arabic_script"].widget.attrs["placeholder"] = "Arabic Script"
        self.fields["arabic_latin"].label = "earabiun"
        self.fields["arabic_latin"].widget.attrs["placeholder"] = "Arabic Letters"
