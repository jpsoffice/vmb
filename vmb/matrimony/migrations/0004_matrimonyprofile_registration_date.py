# Generated by Django 2.2.7 on 2020-11-22 10:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0003_matrimonyprofile_is_tob_unknown'),
    ]

    operations = [
        migrations.AddField(
            model_name='matrimonyprofile',
            name='registration_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
