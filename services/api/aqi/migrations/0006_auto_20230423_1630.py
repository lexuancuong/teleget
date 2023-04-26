# Generated by Django 3.2.14 on 2023-04-23 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aqi', '0005_airinfo_index_active'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='airinfo',
            name='index_active',
        ),
        migrations.AddIndex(
            model_name='airinfo',
            index=models.Index(fields=['active', 'updated_at'], name='index_active_n_updated_at'),
        ),
    ]