# Generated by Django 2.2.7 on 2020-12-07 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0002_auto_20201018_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='female',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='male_matches', to='matrimony.Female'),
        ),
        migrations.AlterField(
            model_name='match',
            name='male',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='female_matches', to='matrimony.Male'),
        ),
    ]
