import uuid
from database.database import Base
from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    verified_payment = Column(Boolean, default=False)
    verified_driving_license = Column(Boolean, default=False)
    is_renting = Column(Boolean, default=False)
    renting_car_id = Column(String, nullable=True)

    rental_history = relationship("Rent", back_populates="user")
