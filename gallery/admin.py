from django.contrib import admin
from .models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    readonly_fields = ("image_preview", )
    list_display = ("sight", "destination", "image_preview", "image", "is_visible")

    @admin.display()
    def destination(self, response):
        return response.sight.destination

