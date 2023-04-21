from typing import List

from ninja import Router, Schema

from .models import AirInfo
from .schemas import AirInfoSchema

router = Router()


@router.post("/", response=AirInfoSchema)
def save_air_info(request, air_info: AirInfoSchema):
    return AirInfoSchema.from_orm(AirInfo.objects.create(**air_info.dict()))


@router.get("/", response=AirInfoSchema)
def get_air_information_from_single_lat_long(request, lat: float, long: float):
    return AirInfoSchema(aqi=10, pm25=10, temperature=37, humidity=50, lat=10, long=100)


class LocationRequest(Schema):
    lat: float
    long: float


@router.post("/get_batch_aqi", response=List[AirInfoSchema])
def get_batch_air_information_from_multiple_lat_long(request, locations: List[LocationRequest]):
    return [
        AirInfoSchema(aqi=10, pm25=10, temperature=37, humidity=50, lat=10, long=100)
        for _ in range(len(locations))
    ]
