from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django_countries.fields import CountryField
from destinations.models import Destination


class Contact(models.Model):
    """ Contact form fields """

    name = models.CharField(max_length=75, blank=False, null=False)
    email = models.EmailField(max_length=256, blank=False, null=False)
    phone_num = models.CharField(max_length=30, null=True)
    country = CountryField(blank_label="Your Country", null=False, blank=False)
    start_date = models.DateField(blank=False, null=False)
    num_days = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(60),
        ],
        blank=False,
        null=False
    )
    num_guests = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(21),
        ],
        blank=False,
        null=False
    )
    message = models.TextField(blank=False, null=False
    )
    destinations = models.ManyToManyField(
        Destination,
        blank=True,
        related_name="contact_destinations"
    )
    msg_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)

    def __str__(self):
        return self.email
