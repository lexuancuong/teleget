from django.http.response import HttpResponse
from ninja import NinjaAPI

from .elevation import get_single_elevation

api = NinjaAPI(title='Teleget API')


@api.get("/elevation")
def get_elevation_api(request, lat: float, long: float):
    # Sample:
    # lat = 10.74474
    # lng = 106.70847
    error_msg_template = (
        f"Failed to get elevation from {lat}, {long} because {{exc}}",
    )
    try:
        if not (elevation := get_single_elevation(lat, long)):
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
