# Generated by Django 2.2.7 on 2020-09-10 15:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0062_auto_20200910_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matrimonyprofile',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
