# Generated by Django 3.2.13 on 2022-05-29 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Phrase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('0', 'Greetings'), ('1', 'General'), ('2', 'Directions'), ('3', 'Accommodation'), ('4', 'Food & Drink'), ('5', 'Numbers'), ('6', 'Colors'), ('7', 'Emergency')], max_length=50)),
                ('english_phrase', models.CharField(max_length=250)),
                ('sorani_script', models.CharField(max_length=250)),
                ('sorani_latin', models.CharField(max_length=250)),
                ('arabic_script', models.CharField(max_length=250)),
                ('arabic_latin', models.CharField(max_length=250)),
                ('is_visible', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['category', 'english_phrase'],
            },
        ),
    ]
