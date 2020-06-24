# Generated by Django 2.2.7 on 2020-06-20 10:45

from django.db import migrations, models
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0032_merge_20200620_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expectation',
            name='annual_income_from',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default_currency='INR', max_digits=10, null=True, verbose_name='From annual income'),
        ),
        migrations.AlterField(
            model_name='expectation',
            name='annual_income_to',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default_currency='INR', max_digits=10, null=True, verbose_name='To annual income'),
        ),
        migrations.AlterField(
            model_name='expectation',
            name='four_reg_principles',
            field=models.BooleanField(blank=True, null=True, verbose_name='Does the spouse have to follow four regulative principles?'),
        ),
        migrations.AlterField(
            model_name='matrimonyprofile',
            name='employed_in',
            field=models.CharField(blank=True, choices=[('PSU', 'Government/PSU'), ('PVT', 'Private'), ('BUS', 'Business'), ('DEF', 'Defence'), ('SE', 'Self Employed'), ('NW', 'Not Working')], max_length=3, null=True),
        ),
    ]
