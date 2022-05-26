from django.db import models
from django_countries.fields import CountryField
from tinymce.models import HTMLField


class Source(models.Model):
    """
        Sources used for Reviews
    """
    name = models.CharField(max_length=50, null=False, blank=False)
    url = models.URLField(null=False, blank=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Review(models.Model):
    """
        Reviews from previous tours, sourced manually online
    """
    RATINGS = [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ]

    author = models.CharField(max_length=75, null=False, blank=False)
    headline = models.CharField(max_length=120, null=False, blank=False)
    review = HTMLField(null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    country = CountryField(blank_label="Country", null=True, blank=True)
    rating = models.CharField(
        choices=RATINGS, max_length=1, null=False, blank=False)
    source = models.ForeignKey(
        Source, on_delete=models.CASCADE, null=False, blank=False)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["date", "rating"]

    def __str__(self):
        return self.author
