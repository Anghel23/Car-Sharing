import fastapi
from fastapi.middleware.cors import CORSMiddleware
from routes import user, car, rental
from database.database import Base, engine, SessionLocal
from models.user import User
from models.car import Car
from models.rental import Rent
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager

app = fastapi.FastAPI(
    title="User & Car Management API",
    description="API for managing users and cars, including registration, authentication, updates, and deletions.",
    version="1.0.0"
)

# CORS pentru a permite conexiuni de la frontend (Angular)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Adaugă frontend-ul Angular
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crearea automată a tabelelor în baza de date
Base.metadata.create_all(bind=engine)

# Adăugarea rutelor API
app.include_router(user.router)
app.include_router(car.router)
app.include_router(rental.router)

# Funcție pentru a verifica și șterge închirierile expirate
def delete_expired_rentals():
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        expired_rentals = db.query(Rent).filter(Rent.return_date <= now).all()
        for rental in expired_rentals:
            # Update car status
            car = db.query(Car).filter(Car.id == rental.car_id).first()
            if car:
                car.is_rented = False
                car.current_renter = None

            db.delete(rental)
            print(f"Rental with ID {rental.id} has been deleted at {now}.")
        db.commit()
    finally:
        db.close()

# Configurarea scheduler-ului pentru a rula funcția la fiecare minut
scheduler = BackgroundScheduler()
scheduler.add_job(delete_expired_rentals, 'interval', minutes=1)

# Gestionarii de evenimente de durată de viață
@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()

app.router.lifespan_context = lifespan