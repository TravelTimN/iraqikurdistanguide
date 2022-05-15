from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


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
    destinations= models.JSONField(
        blank=False,
        null=False
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

    class Meta:
        verbose_name = ("Contact")
        verbose_name_plural = ("Contacts")

    def __str__(self):
        return (
            f"Contact from {self.email} on "
            f"{self.msg_date.strftime('%d%b%y').upper()} @ "
            f"{self.msg_date.strftime('%H:%M')}"
        )
