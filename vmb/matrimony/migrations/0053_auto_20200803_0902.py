# Generated by Django 2.2.7 on 2020-08-03 09:02

from django.db import migrations
import places.fields


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0052_auto_20200727_0646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matrimonyprofile',
            name='current_place',
            field=places.fields.PlacesField(blank=True, max_length=255, null=True),
        ),
    ]
