from django.db import models
from tinymce.models import HTMLField


class FAQ(models.Model):
    """
        FAQs model, including categories.
    """
    CATEGORIES = [
        ("0", "General Information"), ("1", "Booking Information"),
        ("2", "Pre-Departure"), ("3", "Health & Safety"),
        ("4", "Accommodation"), ("5", "Food & Drink"),
    ]
    question = models.CharField(max_length=250, null=False, blank=False)
    answer = HTMLField(null=False, blank=False)
    category = models.CharField(
        choices=CATEGORIES, max_length=25, null=False, blank=False)
    is_visible = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "FAQs"
        ordering = ["category", "question"]

    def __str__(self):
        return self.question
