from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LocationSchema(BaseModel):
    lat: float
    long: float


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
