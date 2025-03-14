from pydantic import BaseModel
from typing import Optional

class CarCreate(BaseModel):
    model: str
    license_plate: str
    is_rented: bool = False
    current_renter: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    speed: float = 0.0
    engine_on: bool = False
    headlights_on: bool = False
    windows_closed: bool = True
    doors_locked: bool = True
    trunk_closed: bool = True
    fuel_level: float = 100.0
    tire_pressure: float = 32.0
    alarm_active: bool = False

class CarUpdate(BaseModel):
    model: Optional[str]
    license_plate: Optional[str]
    is_rented: Optional[bool]
    current_renter: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    speed: Optional[float]
    engine_on: Optional[bool]
    headlights_on: Optional[bool]
    windows_closed: Optional[bool]
    doors_locked: Optional[bool]
    trunk_closed: Optional[bool]
    fuel_level: Optional[float]
    tire_pressure: Optional[float]
    alarm_active: Optional[bool]

class CarResponse(CarCreate):
    id: str

    class Config:
        from_attributes = True