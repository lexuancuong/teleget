from typing import List, Optional

from django.http.response import HttpResponse
from ninja import Router, Schema

from .utils import get_multi_elevation, get_single_elevation

router = Router()


@router.get("/")
def get_elevation_api(request, lat: float, long: float):
    # Sample:
    # lat = 10.74474
    # lng = 106.70847
    error_msg_template = (
        f"Failed to get elevation from lat={lat}, long={long} because {{exc}}"
    )
    try:
        if (elevation := get_single_elevation(lat, long)) is None:
            return HttpResponse(
                error_msg_template.format(exc='elevation not found'),
                status=404,
            )
        return {
            'location': {'lat': lat, 'long': long},
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