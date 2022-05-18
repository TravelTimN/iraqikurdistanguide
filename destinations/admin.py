from django.contrib import admin
from .models import Province, Destination, Site


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "region")


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "province", "region")

    @admin.display()
    def region(self, response):
        return response.province.get_region_display()


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "province", "region")

    @admin.display()
    def province(self, response):
        return response.destination.province

    def region(self, response):
        return response.destination.province.get_region_display()
