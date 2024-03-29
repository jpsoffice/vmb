# Generated by Django 3.0.13 on 2022-09-04 07:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('matrimony', '0016_auto_20220827_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='category',
            field=models.CharField(blank=True, choices=[('USR', 'User'), ('STF', 'Staff'), ('SYS', 'Auto generated')], default='STF', max_length=3),
        ),
        migrations.AddField(
            model_name='match',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='match',
            name='is_mutual',
            field=models.NullBooleanField(help_text='Is it a mutual match based on expectations?'),
        ),
        migrations.AddField(
            model_name='match',
            name='is_visible',
            field=models.NullBooleanField(default=True, help_text='Is match visible to users?'),
        ),
        migrations.AddField(
            model_name='match',
            name='notification_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='notified',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='match',
            name='sender_gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Others')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='show_entire_profile',
            field=models.NullBooleanField(default=False, help_text='Show entire profile info'),
        ),
        migrations.AlterField(
            model_name='match',
            name='status',
            field=models.CharField(blank=True, choices=[('', ''), ('TSG', 'To suggest'), ('SUG', 'Suggested'), ('SNT', 'Sent'), ('ACP', 'Accepted'), ('REJ', 'Rejected'), ('NIM', 'Need info from matches'), ('CNV', 'In conversation'), ('MRC', 'Marriage cancelled'), ('MRF', 'Marriage finalized'), ('MRD', 'Married')], default='', max_length=3),
        ),
    ]
