# Generated by Django 2.2.7 on 2020-08-26 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony', '0056_auto_20200826_1453'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['content_type', 'object_id'], name='comments_content_cd20f6_idx'),
        ),
        migrations.AddIndex(
            model_name='emailmessage',
            index=models.Index(fields=['profile'], name='matrimony_e_profile_2f6251_idx'),
        ),
        migrations.AddIndex(
            model_name='image',
            index=models.Index(fields=['profile'], name='matrimony_i_profile_a2f0c8_idx'),
        ),
        migrations.AddIndex(
            model_name='match',
            index=models.Index(fields=['male'], name='matrimony_m_male_id_d0a9ed_idx'),
        ),
        migrations.AddIndex(
            model_name='match',
            index=models.Index(fields=['female'], name='matrimony_m_female__e3b12e_idx'),
        ),
    ]
