from django.db import models
from tinymce.models import HTMLField
from destinations.models import Destination


class Itinerary(models.Model):
    """
        Itinerary model.
    """
    title = models.CharField(max_length=255)
    is_visible = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Itineraries"

    def __str__(self):
        return self.title


class ItineraryDay(models.Model):
    """
        ItineraryDay model: each day for a specific itinerary.
    """
    itinerary = models.ForeignKey(
        Itinerary, related_name="days", on_delete=models.CASCADE)
    day_number = models.PositiveIntegerField(default=None, null=True)
    headline = models.CharField(max_length=255, null=False, blank=False)
    plan = HTMLField(null=False, blank=False)
    destinations = models.ManyToManyField(
        Destination, related_name="daily_destinations")
    overnight_city = models.ForeignKey(
        Destination, related_name="overnight", on_delete=models.CASCADE)
    hotel = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        ordering = ["itinerary", "day_number"]
        verbose_name = "Itinerary Day"
        verbose_name_plural = "Itinerary Days"

    def __str__(self):
        return self.headline

    def save(self, *args, **kwargs):
        if not self.day_number:
            last_day = ItineraryDay.objects.filter(itinerary=self.itinerary).order_by("-day_number").first()
            if last_day:
                self.day_number = last_day.day_number + 1
            else:
                self.day_number = 1

        super(ItineraryDay, self).save(*args, **kwargs)
