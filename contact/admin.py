from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("msg_date", "name", "email", "start_date", "num_days")
    list_filter = ("email", )
    search_fields = ["email", "name"]
