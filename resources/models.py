from django.db import models


class Phrase(models.Model):
    """
        Phrases can be single words, or full sentences.
        English, Sorani, and Arabic
    """
    PHRASE_CATEGORIES = [
        ("0", "Greetings"), ("1", "General"),
        ("2", "Directions"), ("3", "Accommodation"),
        ("4", "Food & Drink"), ("5", "Numbers"),
        ("6", "Colors"), ("7", "Emergency"),
    ]
    category = models.CharField(
        choices=PHRASE_CATEGORIES, max_length=50, null=False, blank=False)
    english_phrase = models.CharField(max_length=250, null=False, blank=False)
    sorani_script = models.CharField(max_length=250, null=False, blank=False)
    sorani_latin = models.CharField(max_length=250, null=False, blank=False)
    arabic_script = models.CharField(max_length=250, null=False, blank=False)
    arabic_latin = models.CharField(max_length=250, null=False, blank=False)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["category", "english_phrase"]

    def __str__(self):
        return self.english_phrase