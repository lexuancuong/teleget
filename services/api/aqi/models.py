from django.db import models


class AirInfo(models.Model):
    aqi = models.IntegerField(null=True)
    pm25 = models.FloatField(null=True)
    temperature = models.IntegerField(null=True)
    humidity = models.IntegerField(null=True)
    lat = models.FloatField()
    long = models.FloatField()

    class Meta:
        db_table = 'air_info'
        indexes = [
            models.Index(
                fields=['lat', 'long'],
                name='index_lat_long',
            ),
        ]
