from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Optional

class RentalBase(BaseModel):
    car_id: str
    user_id: str
    rent_date: datetime = datetime.now(timezone.utc)
    return_date: Optional[datetime] = None

class RentalCreate(RentalBase):
    duration_minutes: int

class Rental(RentalBase):
    id: str

    class Config:
        from_attributes = True