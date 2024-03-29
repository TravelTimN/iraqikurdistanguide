from django.db import models
import gallery.models


class Province(models.Model):
    """
        Provinces/Governorates of Iraq, to be used as FKs
        for destinations, tours, gallery, etc.
    """
    REGION = [
        ("kur", "Kurdistan"),
        ("irq", "Iraq"),
    ]
    name = models.CharField(max_length=25, null=False, blank=False)
    region = models.CharField(
        choices=REGION, max_length=10, null=False, blank=False)

    class Meta:
        ordering = ["-region", "name"]

    def __str__(self):
        return self.name


class Destination(models.Model):
    """
        Various destinations, can be used with tours,
        gallery, maps, contact form, etc.
    """
    name = models.CharField(max_length=50, null=False, blank=False)
    province = models.ForeignKey(
        Province, on_delete=models.CASCADE, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=False, blank=False)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=False, blank=False)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["-province__region", "name"]

    def __str__(self):
        return self.name


class Sight(models.Model):
    """
        Various POIs / sights, can be used with tours,
        gallery, maps, contact form, etc.
        These extend the Destination model.
    """
    MARKER_TYPE = [
        ("accommodation", "Accommodation"), ("airport", "Airport"),
        ("archaeology", "Archaeology"), ("historic", "Historic"),
        ("memorial", "Memorial"), ("museum", "Museum"),
        ("nature", "Nature"), ("recreation", "Recreation"),
        ("religious", "Religious"), ("restaurant", "Restaurant"),
        ("shopping", "Shopping"), ("tea_shop", "Tea Shop"),
    ]
    name = models.CharField(max_length=150, null=False, blank=False)
    destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE, null=False, blank=False)
    category = models.CharField(
        choices=MARKER_TYPE, max_length=30, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=False, blank=False)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=False, blank=False)
    is_visible = models.BooleanField(default=True)
    primary_attraction = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tour(models.Model):
    """
        Various types of tours available.
        Can be applied to 'Sights' as pill badges.
    """
    category = models.CharField(max_length=30, null=False, blank=False)
    photo = models.ForeignKey(
        "gallery.Photo", on_delete=models.CASCADE, null=False, blank=False)
    description = models.CharField(max_length=100, null=False, blank=False)
    is_visible = models.BooleanField(default=True)

    def image_preview(self):
        from django.utils.html import format_html
        return format_html(f"<img src='{self.photo.image.url}' height='150'>")

    class Meta:
        ordering = ["category"]

    def __str__(self):
        return self.category
