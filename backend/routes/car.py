from fastapi import APIRouter, Depends, HTTPException, requests, status
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.car import Car
from schemas.car import CarCreate, CarUpdate, CarResponse
from typing import List

router = APIRouter(prefix="/cars", tags=["Cars"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", status_code=status.HTTP_201_CREATED, summary="Register a new car")
async def register_car(request: CarCreate, db: Session = Depends(get_db)):
    existing_car = db.query(Car).filter(Car.license_plate == request.license_plate).first()
    if existing_car:
        raise HTTPException(status_code=400, detail="Car with this license plate already exists")

    new_car = Car(
        model=request.model,
        license_plate=request.license_plate,
        latitude=request.latitude,
        longitude=request.longitude,
        is_rented=request.is_rented,
        current_renter=request.current_renter,
        engine_on=request.engine_on,
        headlights_on=request.headlights_on,
        windows_closed=request.windows_closed,
        doors_locked=request.doors_locked,
        trunk_closed=request.trunk_closed,
        fuel_level=request.fuel_level,
        tire_pressure=request.tire_pressure,
        alarm_active=request.alarm_active
    )
    db.add(new_car)
    db.commit()
    db.refresh(new_car)

    return {"message": "Car registered successfully", "car_id": new_car.id}

@router.get("/", response_model=List[CarResponse], summary="Get all cars")
async def get_all_cars(db: Session = Depends(get_db)):
    cars = db.query(Car).all()
    return cars

@router.get("/available", response_model=List[CarResponse], summary="Get available cars for rent")
async def get_available_cars(db: Session = Depends(get_db)):
    """
    Returnează lista mașinilor disponibile pentru închiriere (care nu sunt închiriate).
    """
    available_cars = db.query(Car).filter(Car.is_rented == False).all()
    return available_cars

@router.put("/{car_id}", summary="Update a car by ID")
async def update_car(car_id: str, car_update: CarUpdate, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()

    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    for key, value in car_update.dict().items():
        setattr(car, key, value)

    db.commit()
    db.refresh(car)

    return {"message": "Car updated successfully", "car": car}

@router.delete("/{car_id}", summary="Delete a car by ID")
async def delete_car(car_id: str, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()

    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    db.delete(car)
    db.commit()

    return {"message": "Car deleted successfully"}

@router.get("/can-stop/{car_id}", summary="Check if the car can be stopped")
async def can_stop_rental(car_id: str, db: Session = Depends(get_db)):
    response = requests.get(f"http://127.0.0.1:5000/telematics")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to get car telematics")

    car_telematics = response.json()
    
    if (car_telematics["speed"] == 0.0 and
        not car_telematics["engine_on"] and
        not car_telematics["headlights_on"] and
        car_telematics["windows_closed"] and
        car_telematics["doors_locked"] and
        car_telematics["trunk_closed"] and
        not car_telematics["alarm_active"]):

        # 1. Găsește mașina în baza de date
        car = db.query(Car).filter(Car.id == car_id).first()
        if not car:
            raise HTTPException(status_code=404, detail="Car not found")

        # 2. Actualizează datele manual
        car.latitude = car_telematics["latitude"]
        car.longitude = car_telematics["longitude"]
        car.engine_on = car_telematics["engine_on"]
        car.headlights_on = car_telematics["headlights_on"]
        car.windows_closed = car_telematics["windows_closed"]
        car.doors_locked = car_telematics["doors_locked"]
        car.trunk_closed = car_telematics["trunk_closed"]
        car.fuel_level = car_telematics["fuel_level"]
        car.tire_pressure = car_telematics["tire_pressure"]
        car.alarm_active = car_telematics["alarm_active"]

        # 3. Commit-ul este crucial
        db.commit()
        db.refresh(car)  # Asigură că schimbările sunt vizibile

        return {"can_stop": True, "updated_car": car}
    
    return {"can_stop": False}

