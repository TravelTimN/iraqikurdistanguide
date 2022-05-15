from django.db import models


class Province(models.Model):
    """
        Provinces/Governorates of Iraq, to be used as FKs
        for destinations, tours, gallery, etc.
    """
    name = models.CharField(max_length=25, null=False, blank=False)

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

    def __str__(self):
        return self.name
