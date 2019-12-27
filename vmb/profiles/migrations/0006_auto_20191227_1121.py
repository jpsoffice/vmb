# Generated by Django 2.2.7 on 2019-12-27 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20191227_0814'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='complexion',
            field=models.CharField(blank=True, choices=[('I', 'Light, Pale White'), ('II', 'White, Fair'), ('III', 'Medium, White to light brown'), ('IV', 'Olive, moderate brown'), ('V', 'Brown, dark brown'), ('VI', 'Very dark brown to black')], help_text='Enter your complexion', max_length=3),
        ),
        migrations.AlterField(
            model_name='person',
            name='current_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='currentCountry', to='profiles.Country', verbose_name='Country'),
        ),
    ]
