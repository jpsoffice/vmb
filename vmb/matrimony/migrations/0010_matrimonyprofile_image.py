# Generated by Django 2.2.7 on 2020-05-07 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photologue', '0011_auto_20190223_2138'),
        ('matrimony', '0009_auto_20200423_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='matrimonyprofile',
            name='image',
            field=models.ManyToManyField(blank=True, to='photologue.Photo'),
        ),
    ]
