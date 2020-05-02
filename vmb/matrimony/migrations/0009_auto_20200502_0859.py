# Generated by Django 2.2.7 on 2020-05-02 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0008_auto_20200412_1439'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='match',
            options={'verbose_name': 'Matche', 'verbose_name_plural': 'Matches'},
        ),
        migrations.AlterField(
            model_name='match',
            name='status',
            field=models.CharField(blank=True, choices=[('', ''), ('SUG', 'Suggested'), ('TON', 'To notify'), ('NTF', 'Notified'), ('FOL', 'Follow up'), ('PRD', 'Parties discussing'), ('MRC', 'Marriage cancelled'), ('MRF', 'Marriage finalized'), ('MRD', 'Married')], default='', max_length=3),
        ),
        migrations.AlterField(
            model_name='matrimonyprofile',
            name='dob',
            field=models.DateField(help_text='Enter birth date as YYYY-MM-DD', null=True, verbose_name='date of birth'),
        ),
        migrations.AlterField(
            model_name='matrimonyprofile',
            name='rounds_chanting',
            field=models.IntegerField(default=0, help_text='How many rounds are you chanting?', verbose_name='Rounds'),
        ),
    ]
