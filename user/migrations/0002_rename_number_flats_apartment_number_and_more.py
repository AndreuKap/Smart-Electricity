# Generated by Django 5.0.6 on 2024-05-09 16:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flats',
            old_name='number',
            new_name='apartment_number',
        ),
        migrations.AddField(
            model_name='bweller',
            name='date_register',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='bweller',
            name='apartment_number',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='number', serialize=False, to='user.flats'),
        ),
        migrations.AlterField(
            model_name='bweller',
            name='login',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='flats',
            name='bweller',
            field=models.IntegerField(),
        ),
    ]