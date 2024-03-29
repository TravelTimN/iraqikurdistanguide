# Generated by Django 3.2.13 on 2022-07-16 21:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0003_auto_20220531_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='num_guests',
            field=models.IntegerField(default=2, validators=[django.core.validators.MaxValueValidator(21), django.core.validators.MinValueValidator(1)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contact',
            name='num_days',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(60), django.core.validators.MinValueValidator(1)]),
        ),
    ]
