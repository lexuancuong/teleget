from typing import Dict, List, Optional

from django.http.response import HttpResponse
from ninja import Router, Schema
from pydantic import root_validator

from .utils import get_multi_elevation, get_single_elevation

router = Router()


@router.get("/")
def get_elevation_api(request, lat: str, long: str):
    # Sample:
    # lat = 10.74474
    # lng = 106.70847
    error_msg_template = (
        f"Failed to get elevation from lat={lat}, long={long} because {{exc}}"
    )
    try:
        # Front-end need this support because they cannot convert to correct float format
        lat = lat.replace(',', '.')
        long = long.replace(',', '.')
        lat_float = float(lat)
        long_float = float(long)
        if (elevation := get_single_elevation(lat_float, long_float)) is None:
            return HttpResponse(
                error_msg_template.format(exc='elevation not found'),
                status=404,
            )
        return {
            'location': {'lat': lat_float, 'long': long_float},
            'elevation': elevation,
        }
    except Exception as exc:
        return HttpResponse(
            f"Failed to get elevation from {lat}, {long} because {exc}",
            status=400,
        )


class LocationRequest(Schema):
    lat: float
    long: float

    @root_validator(pre=True)
    def convert_lat_long_from_string(cls, values: Dict):
        # TODO DRY
        for key in ('lat', 'long'):
            value = values.get(key)
            if value:
                values[key] = float(str(value).replace(',', '.'))
        return values


class ElevationResponse(Schema):
    location: LocationRequest
    elevation: Optional[float]


@router.post("/", response=List[ElevationResponse])
def get_multi_elevation_api(request, locations: List[LocationRequest]):
    # Sample:
    # lat = 10.74474
    # lng = 106.70847
    try:
        res: list[ElevationResponse] = []
        lats = [location.lat for location in locations]
        longs = [location.long for location in locations]
        elevations = get_multi_elevation(lats, longs)
        for index in range(len(lats)):
            res.append(
                ElevationResponse(
                    location=LocationRequest(lat=lats[index], long=longs[index]),
                    elevation=elevations[index],
                )
            )
        return res
    except Exception as exc:
        return HttpResponse(
            f"Failed to get multiple elevations because {exc}",
            status=400,
        )
