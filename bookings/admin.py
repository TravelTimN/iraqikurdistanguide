from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "guest_name", "start_date", "end_date",
        "total_price", "amount_paid", "guide", "date_created")
    list_filter = ("guide", )
    search_fields = ["guest_name", "guest_email"]
