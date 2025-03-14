import uuid
from sqlalchemy import Column, String, Float, Boolean
from sqlalchemy.orm import relationship
from database.database import Base

class Car(Base):
    __tablename__ = "cars"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    model = Column(String, nullable=False)
    license_plate = Column(String, unique=True, nullable=False)

    is_rented = Column(Boolean, default=False)
    current_renter = Column(String, nullable=True)
    
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    speed = Column(Float, default=0.0)

    engine_on = Column(Boolean, default=False)
    headlights_on = Column(Boolean, default=False)
    windows_closed = Column(Boolean, default=True)
    doors_locked = Column(Boolean, default=True)
    trunk_closed = Column(Boolean, default=True)

    fuel_level = Column(Float, default=100.0)
    tire_pressure = Column(Float, default=32.0)
    
    alarm_active = Column(Boolean, default=False)

    rentals = relationship("Rent", back_populates="car")

    def is_ready_for_rent(self):
        return (not self.engine_on and
                self.doors_locked and
                self.trunk_closed and
                self.windows_closed and
                self.fuel_level > 10)
