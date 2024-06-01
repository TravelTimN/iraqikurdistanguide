from django.contrib import admin
from .models import Itinerary, ItineraryDay


# ------------- ITINERARY
class ItineraryDayAdmin(admin.StackedInline):
    model = ItineraryDay

@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    inlines = [ItineraryDayAdmin]
    list_filter = ("is_visible",)
    list_display = ("title", "is_visible")


# ------------- ITINERARY DAY
@admin.register(ItineraryDay)
class ItineraryDayAdmin(admin.ModelAdmin):
    list_filter = ("itinerary", "overnight_city")
    list_display = ("itinerary", "day_number", "headline", "overnight_city")
