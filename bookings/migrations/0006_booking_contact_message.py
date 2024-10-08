# Generated by Django 4.2.16 on 2024-09-11 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0006_contact_country'),
        ('bookings', '0005_booking_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='contact_message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contact.contact'),
        ),
    ]
