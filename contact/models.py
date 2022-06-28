from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from destinations.models import Destination


class Contact(models.Model):
    """ Contact form fields """

    name = models.CharField(
        max_length=75,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=256,
        blank=False,
        null=False
    )
    destinations= models.ManyToManyField(
        Destination,
        blank=True,
        related_name="contact_destinations"
    )
    start_date = models.DateField(
        blank=False,
        null=False
    )
    num_days = models.IntegerField(
        validators=[
            MaxValueValidator(30),
            MinValueValidator(1)
        ],
        blank=False,
        null=False
    )
    message = models.TextField(
        blank=False,
        null=False
    )
    phone_num = models.CharField(
        max_length=30,
        null=True
    )
    msg_date = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        null=False
    )

    def __str__(self):
        return self.email
