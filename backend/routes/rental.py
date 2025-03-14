from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.car import Car
from models.user import User
from models.rental import Rent
from schemas.rental import RentalCreate, Rental
from datetime import datetime, timedelta
import requests

router = APIRouter(prefix="/rent", tags=["Rent"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Rental, summary="Rent a car")
async def rent_car(request: RentalCreate, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == request.car_id).first()
    user = db.query(User).filter(User.id == request.user_id).first()

    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if car.is_rented:
        raise HTTPException(status_code=400, detail="Car is already rented")
    if not car.is_ready_for_rent():
        raise HTTPException(status_code=400, detail="Car is not in a rentable condition")

    # Create rental
    rental_duration = timedelta(minutes=request.duration_minutes)
    rent_date = datetime.utcnow()
    return_date = rent_date + rental_duration
    rental = Rent(car_id=request.car_id, user_id=request.user_id, start_time=rent_date, return_date=return_date)
    db.add(rental)

    # Update car status
    car.is_rented = True
    car.current_renter = user.id
    db.commit()
    db.refresh(rental)

    print(f"New rental added at {rental.start_time}. It will be deleted at {rental.return_date}.")

    return rental

@router.get("/can-stop/{car_id}", summary="Check if the car can be stopped")
async def can_stop_rental(car_id: str):
    response = requests.get(f"http://127.0.0.1:5000/telematics")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to get car telematics")

    car_telematics = response.json()
    reasons = []
    if car_telematics["speed"] != 0.0:
        reasons.append("Mașina este în mișcare.")
    if car_telematics["engine_on"]:
        reasons.append("Motorul este pornit.")
    if car_telematics["headlights_on"]:
        reasons.append("Farurile sunt aprinse.")
    if not car_telematics["windows_closed"]:
        reasons.append("Geamurile sunt deschise.")
    if not car_telematics["doors_locked"]:
        reasons.append("Ușile sunt deblocate.")
    if not car_telematics["trunk_closed"]:
        reasons.append("Portbagajul este deschis.")
    if car_telematics["alarm_active"]:
        reasons.append("Alarma este activată.")

    can_stop = len(reasons) == 0
    return {"can_stop": can_stop, "reasons": reasons}

@router.post("/return/{car_id}/{user_id}", summary="Return a rented car")
async def return_car(car_id: str, user_id: str, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()

    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    if not car.is_rented:
        raise HTTPException(status_code=400, detail="Car is not currently rented")
    if car.current_renter != user_id:
        raise HTTPException(status_code=403, detail="You are not the renter of this car")

    # Get current telematics data
    response = requests.get(f"http://127.0.0.1:5000/telematics")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to get car telematics")

    car_telematics = response.json()

    # Update car status
    car_update = {
        "is_rented": False,
        "current_renter": None,
        "latitude": car_telematics["latitude"],
        "longitude": car_telematics["longitude"],
        "speed": car_telematics["speed"],
        "engine_on": car_telematics["engine_on"],
        "headlights_on": car_telematics["headlights_on"],
        "windows_closed": car_telematics["windows_closed"],
        "doors_locked": car_telematics["doors_locked"],
        "trunk_closed": car_telematics["trunk_closed"],
        "fuel_level": car_telematics["fuel_level"],
        "tire_pressure": car_telematics["tire_pressure"],
        "alarm_active": car_telematics["alarm_active"]
    }

    update_response = requests.put(f"http://127.0.0.1:8000/cars/{car_id}", json=car_update)
    if update_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to update car status")

    return {"message": f"Car {car.model} ({car.license_plate}) returned successfully"}

@router.delete("/{rental_id}", summary="Delete a rental by ID")
async def delete_rental(rental_id: str, db: Session = Depends(get_db)):
    rental = db.query(Rent).filter(Rent.id == rental_id).first()

    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")

    # Update car status
    car = db.query(Car).filter(Car.id == rental.car_id).first()
    if car:
        car.is_rented = False
        car.current_renter = None

    db.delete(rental)
    db.commit()

    print(f"Rental with ID {rental_id} has been deleted.")

    return {"message": "Rental deleted successfully"}