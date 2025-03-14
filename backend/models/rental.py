import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime, timedelta

class Rent(Base):
    __tablename__ = "rentals"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    car_id = Column(String, ForeignKey("cars.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=False)

    car = relationship("Car", back_populates="rentals")
    user = relationship("User", back_populates="rental_history")