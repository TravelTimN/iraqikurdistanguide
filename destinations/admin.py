from django.contrib import admin
from .models import Province, Destination, Site


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("name", "region")


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("name", "province", "region", "is_visible")

    @admin.display()
    def region(self, response):
        return response.province.get_region_display()


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = (
        "name", "category", "destination", "province",
        "region", "is_visible", "primary_attraction")

    @admin.display()
    def province(self, response):
        return response.destination.province

    def region(self, response):
        return response.destination.province.get_region_display()
