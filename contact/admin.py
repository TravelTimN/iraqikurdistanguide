from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("msg_date", "name", "email", "country", "start_date", "num_days")
    list_filter = ("email", )
    search_fields = ["email", "name"]

    formfield_overrides = {
        models.ManyToManyField: {
            "widget": CheckboxSelectMultiple,
        }
    }
