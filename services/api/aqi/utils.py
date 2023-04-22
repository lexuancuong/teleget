from math import atan2, cos, sin, sqrt

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


def get_aqi_from_location(location: LocationSchema) -> AirInfo:
    air_infos = AirInfo.objects.filter(active=True).reverse()[:10]
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
