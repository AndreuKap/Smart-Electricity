# Generated by Django 5.0.6 on 2024-05-09 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Counters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.IntegerField()),
                ('power', models.FloatField()),
                ('datetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
