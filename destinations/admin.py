from django.contrib import admin
from .models import Province, Destination, Sight, Tour


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "region")


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "province", "region", "is_visible")

    @admin.display()
    def region(self, response):
        return response.province.get_region_display()


@admin.register(Sight)
class SightAdmin(admin.ModelAdmin):
    list_display = (
        "name", "id", "category", "destination", "province",
        "region", "is_visible", "primary_attraction")
    list_filter = (
        "category", "destination", "destination__province__region",
        "is_visible", "primary_attraction",
    )

    @admin.display()
    def province(self, response):
        return response.destination.province

    def region(self, response):
        return response.destination.province.get_region_display()


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    readonly_fields = ("image_preview", )
    list_display = ("category", "id", "image_preview", "description", "is_visible")
