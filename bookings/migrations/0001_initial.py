# Generated by Django 3.2.13 on 2022-05-31 22:02

import django.core.validators
from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('destinations', '0006_rename_site_sight'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guide', models.CharField(choices=[('haval', 'Haval'), ('govand', 'Govand')], default='Haval', max_length=10)),
                ('guest_name', models.CharField(max_length=100)),
                ('guest_email', models.EmailField(max_length=100)),
                ('guest_phone', models.CharField(max_length=50)),
                ('guest_country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('total_guests', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)])),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('currency', models.CharField(choices=[('usd', '$'), ('eur', '€'), ('iqd', 'د.ع')], max_length=3)),
                ('total_price', models.PositiveIntegerField()),
                ('amount_paid', models.PositiveIntegerField(default=0)),
                ('notes', models.TextField(blank=True, null=True)),
                ('itinerary', models.ManyToManyField(blank=True, related_name='itinerary_destinations', to='destinations.Destination')),
            ],
            options={
                'ordering': ['start_date', 'guide'],
            },
        ),
    ]
