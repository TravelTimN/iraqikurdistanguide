from django.contrib import admin
from .models import Phrase


@admin.register(Phrase)
class PhraseAdmin(admin.ModelAdmin):
    list_display = ("english_phrase", "category", "is_visible")
    list_filter = ("category", )
