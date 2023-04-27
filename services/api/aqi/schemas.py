from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, root_validator


class LocationSchema(BaseModel):
    lat: float
    long: float

    @root_validator(pre=True)
    def convert_lat_long_from_string(cls, values: Dict):
        for key in ('lat', 'long'):
            value = values.get(key)
            if value:
                value = float(str(value).replace(',', '.'))
        return values


class AirInfoSchema(BaseModel):
    aqi: Optional[int]
    pm25: Optional[float]
    temperature: Optional[int]
    humidity: Optional[int]
    location: Optional[LocationSchema]
    active: Optional[bool] = True
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
