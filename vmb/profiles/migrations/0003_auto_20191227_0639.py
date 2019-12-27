# Generated by Django 2.2.7 on 2019-12-27 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20191227_0626'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='languages_known',
        ),
        migrations.AddField(
            model_name='person',
            name='languages_known',
            field=models.ManyToManyField(to='profiles.Language'),
        ),
    ]
