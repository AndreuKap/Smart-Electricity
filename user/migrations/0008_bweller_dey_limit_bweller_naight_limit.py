# Generated by Django 5.0.6 on 2024-05-11 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_bweller_time_identifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='bweller',
            name='dey_limit',
            field=models.FloatField(blank=True, default=32, verbose_name='dey limit'),
        ),
        migrations.AddField(
            model_name='bweller',
            name='naight_limit',
            field=models.FloatField(blank=True, default=11, verbose_name='night limit'),
        ),
    ]
