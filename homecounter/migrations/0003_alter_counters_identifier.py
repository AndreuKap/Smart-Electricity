# Generated by Django 5.0.6 on 2024-05-10 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homecounter', '0002_languages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counters',
            name='identifier',
            field=models.CharField(max_length=64),
        ),
    ]