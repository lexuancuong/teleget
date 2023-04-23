from django.db import models


class AirInfo(models.Model):
    aqi = models.IntegerField(null=True)
    pm25 = models.FloatField(null=True)
    temperature = models.IntegerField(null=True)
    humidity = models.IntegerField(null=True)
    location = models.JSONField(null=True)
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'air_info'
        indexes = [
            models.Index(
                fields=['active', 'updated_at'],
                name='index_active_n_updated_at',
            ),
        ]
