# Generated by Django 2.2.7 on 2020-09-19 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200918_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_matrimony_registration_complete',
            field=models.BooleanField(blank=True, default=False, verbose_name='Is matrimony registration complete?'),
        ),
    ]
