# Generated by Django 4.2.16 on 2024-09-11 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itineraries', '0003_itinerary_is_visible'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itinerary',
            options={'verbose_name_plural': 'Itineraries'},
        ),
        migrations.AlterModelOptions(
            name='itineraryday',
            options={'ordering': ['itinerary', 'day_number'], 'verbose_name': 'Itinerary Day', 'verbose_name_plural': 'Itinerary Days'},
        ),
    ]
