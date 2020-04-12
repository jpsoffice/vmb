# Generated by Django 2.2.7 on 2020-04-12 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matrimony', '0006_auto_20200412_1305'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('male_response', models.CharField(blank=True, choices=[('', ''), ('ACP', 'Accepted'), ('REJ', 'Rejected')], default='', max_length=3)),
                ('male_response_updated_at', models.DateTimeField(auto_now=True)),
                ('female_response', models.CharField(blank=True, choices=[('', ''), ('ACP', 'Accepted'), ('REJ', 'Rejected')], default='', max_length=3)),
                ('female_response_updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(blank=True, choices=[('', ''), ('SUG', 'Suggested'), ('FOL', 'Follow up'), ('PRD', 'Parties discussing'), ('MRC', 'Marriage cancelled'), ('MRF', 'Marriage finalized'), ('MRD', 'Married')], default='', max_length=3)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('female', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='male_matches', to='matrimony.MatrimonyProfile')),
                ('male', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='female_matches', to='matrimony.MatrimonyProfile')),
            ],
            options={
                'db_table': 'matrimony_matches',
            },
        ),
        migrations.AddField(
            model_name='matrimonyprofile',
            name='matches',
            field=models.ManyToManyField(blank=True, through='matrimony.Match', to='matrimony.MatrimonyProfile'),
        ),
    ]
