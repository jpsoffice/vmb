# Generated by Django 2.2.7 on 2020-06-20 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0034_matrimonyprofile_profile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matrimonyprofile',
            name='profile_id',
            field=models.CharField(blank=True, max_length=15, unique=True),
        ),
    ]
