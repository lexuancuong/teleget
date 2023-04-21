from typing import Optional

from pydantic import BaseModel


class AirInfoSchema(BaseModel):
    aqi: Optional[int]
    pm25: Optional[float]
    temperature: Optional[int]
    humidity: Optional[int]
    lat: Optional[float]
    long: Optional[float]

    class Config:
        orm_mode = True
