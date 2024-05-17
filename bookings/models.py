from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django_countries.fields import CountryField
from destinations.models import Destination


class Booking(models.Model):
    """
        Bookings model, for admin-only booking management.
    """
    GUIDES = [("haval", "Haval"), ("govand", "Govand"),]
    CURRENCY = [("usd", "$"), ("eur", "€"), ("iqd", "د.ع"),]
    STATUS = [("new", "New"), ("confirmed", "Confirmed"), ("cancelled", "Cancelled"), ("rejected", "Rejected")]

    guide = models.CharField(
        choices=GUIDES, default="Haval",
        max_length=10, null=False, blank=False)
    guest_name = models.CharField(max_length=100, null=False, blank=False)
    guest_email = models.EmailField(max_length=100, null=False, blank=False)
    guest_phone = models.CharField(max_length=50, null=False, blank=False)
    guest_country = CountryField(blank_label="Country", null=True, blank=True)
    total_guests = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(21)],
        null=False, blank=False)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    currency = models.CharField(
        choices=CURRENCY, max_length=3, null=False, blank=False)
    total_price = models.PositiveIntegerField(null=False, blank=False)
    amount_paid = models.PositiveIntegerField(
        default=0, null=False, blank=False)
    itinerary = models.ManyToManyField(
        Destination, blank=True, related_name="itinerary_destinations")
    notes = models.TextField(null=True, blank=True)
    status = models.CharField(choices=STATUS, default="New", max_length=25)

    class Meta:
        ordering = ["start_date", "guide"]

    def __str__(self):
        return self.guest_name
