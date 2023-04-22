import logging
from datetime import datetime
from typing import List, Optional

from ninja import Router
from pydantic import BaseModel

from .models import AirInfo
from .schemas import AirInfoSchema, LocationSchema
from .utils import get_aqi_from_location

router = Router()


class AirInfoSchemaResponse(BaseModel):
    aqi: Optional[int]
    pm25: Optional[float]
    temperature: Optional[int]
    humidity: Optional[int]
    location: Optional[LocationSchema]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


@router.post("/", response=AirInfoSchema)
def save_air_info(request, air_info: AirInfoSchema):
    return AirInfo.objects.create(**air_info.dict())


@router.get("/", response=AirInfoSchemaResponse)
def get_air_information_from_single_lat_long(request, lat: float, long: float):
    requested_location = LocationSchema(lat=lat, long=long)
    try:
        return get_aqi_from_location(requested_location)
    except Exception as exc:
        logging.exception(f"Failed to return AQI because {exc}")


@router.post("/get_batch_aqi", response=List[AirInfoSchemaResponse])
def get_batch_air_information_from_multiple_lat_long(
    request, locations: List[LocationSchema]
):
    res = []
    for location in locations:
        try:
            res.append(get_aqi_from_location(location))
        except Exception as exc:
            logging.exception(f"Failed to return AQI because {exc}")
    return res
