# Generated by Django 3.0.13 on 2023-10-25 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0021_auto_20231025_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='matrimonyprofile',
            name='actual_dob',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
