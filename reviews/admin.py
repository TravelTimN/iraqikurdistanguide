from django.contrib import admin
from .models import Source, Review


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ("name", "url")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "author", "date", "rating",
        "source", "country", "is_visible")
    list_filter = ("source", )
