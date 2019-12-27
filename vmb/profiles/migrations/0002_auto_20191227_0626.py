# Generated by Django 2.2.7 on 2019-12-27 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Name', max_length=255, unique=True)),
                ('code', models.CharField(db_index=True, help_text='Code', max_length=3, unique=True)),
                ('nationality', models.CharField(db_index=True, help_text='Nationality', max_length=255, unique=True)),
            ],
            options={
                'db_table': 'country',
            },
        ),
        migrations.AlterField(
            model_name='person',
            name='birth_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='birthCountry', to='profiles.Country'),
        ),
        migrations.AlterField(
            model_name='person',
            name='current_country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='currentCountry', to='profiles.Country'),
        ),
        migrations.CreateModel(
            name='Nationality',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('profiles.country',),
        ),
    ]
