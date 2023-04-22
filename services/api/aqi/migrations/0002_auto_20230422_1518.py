# Generated by Django 3.2.14 on 2023-04-22 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aqi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='airinfo',
            name='index_lat_long',
        ),
        migrations.RemoveField(
            model_name='airinfo',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='airinfo',
            name='long',
        ),
        migrations.AddField(
            model_name='airinfo',
            name='location',
            field=models.JSONField(null=True),
        ),
    ]