from datetime import timedelta
from math import atan2, cos, sin, sqrt
from typing import Dict

from django.db.models.query import QuerySet
from django.utils import timezone

from .models import AirInfo
from .schemas import LocationSchema

# Approximate radius of earth in km
R = 6373.0


def cal_distance_between_2_point(p1: LocationSchema, p2: LocationSchema) -> float:
    lat1, lon1 = p1.lat, p1.long
    lat2, lon2 = p2.lat, p2.long
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def get_current_aqi(location: LocationSchema) -> AirInfo:
    air_infos = AirInfo.objects.filter(active=True).order_by('-id')[:10]
    return get_aqi_from_air_infos(location, air_infos)


def get_aqi_from_air_infos(location: LocationSchema, air_infos: QuerySet) -> AirInfo:
    min_distance = 10000000000
    returned_air_info = None
    for air_info in air_infos:
        if (
            temp_distance := cal_distance_between_2_point(
                location, LocationSchema.parse_obj(air_info.location)
            )
        ) < min_distance:
            min_distance = temp_distance
            returned_air_info = air_info
    if not returned_air_info:
        raise Exception(f'Cannot get AQI from location={location.dict()}')
    return returned_air_info


def get_historical_aqi_data(
    location: LocationSchema, num_hours: int = 24
) -> Dict[int, AirInfo]:
    res = {}
    for num_hour in range(num_hours):
        air_infos = AirInfo.objects.filter(
            active=True,
            updated_at__lt=timezone.now() - timedelta(hours=num_hour),
            updated_at__gt=timezone.now() - timedelta(hours=num_hour + 1),
        ).order_by('-id')[:10]
        returned_air_info = None
        if air_infos:
            returned_air_info = get_aqi_from_air_infos(location, air_infos)
        res[num_hour] = returned_air_info
    return res
