# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import Dict
# import uvicorn

# app = FastAPI(
#     title="Car Sharing API",
#     description="API for renting and returning cars in a car-sharing service.",
#     version="1.0.0"
# )

# # In-memory databases (simulated)
# cars = {
#     "Ferrari": {
#         "status": "available",
#         "location": "Strada A",
#         "rented_by": ""
#     }
# }

# users = {
#     "ana": {
#         "password": "1234",
#         "license_photo": "license.png",
#         "card_details": "1234-5678-9999-9999"
#     }
# }

# class RentRequest(BaseModel):
#     """Request model for renting or returning a car"""
#     car_id: str
#     user_id: str 

# class RegisterRequest(BaseModel):
#     """Request model for registering a car"""
#     car_id: str
#     location: str

# class RegisterUserRequest(BaseModel):
#     user_id: str
#     password: str
#     license_photo: str
#     card_details: str

# class LoginRequest(BaseModel):
#     user_id: str
#     password: str


# @app.get("/cars", summary="List all cars", tags=["Cars"])
# async def get_cars():
#     """
#     Fetches the list of all available and rented cars.
#     - **status**: "available" or "rented"
#     - **location**: Car's location
#     - **rented_by**: Who has the car right now
#     """
#     return cars

# @app.get("/available-cars", summary="List available cars", tags=["Cars"])
# async def get_available_cars():
#     """
#     Fetches the list of all available cars.
#     """
#     available_cars = {car_id: details for car_id, details in cars.items() if details["status"] == "available"}
#     return available_cars

# @app.post("/register", summary="Register a car", tags=["Cars"])
# async def register_car(request: RegisterRequest):
#     """
#     Register a car by providing the car ID and location.
#     """
#     car_id = request.car_id
#     if car_id not in cars:
#         cars[car_id] = {"status": "available", "location": request.location}
#         return {"message": f"{car_id} registered successfully!"}
#     raise HTTPException(status_code=400, detail="Car already registered")


# @app.post("/user/register", summary="Register a new user", tags=["Users"])
# async def register_user(request: RegisterUserRequest):
#     """
#     Registers a new user with user_id, password, license photo, and card details.
#     """
#     if request.user_id in users:
#         raise HTTPException(status_code=400, detail="User already registered")

#     users[request.user_id] = {
#         "password": request.password,
#         "license_photo": request.license_photo,
#         "card_details": request.card_details
#     }

#     return {"message": f"User {request.user_id} registered successfully!"}


# @app.post("/rent", summary="Rent a car", tags=["Rental"])
# async def rent_car(request: RentRequest):
#     """
#     Rent a car by providing the car ID and user ID.
#     - If the car is available and the user is registered, the car will be rented.
#     - If the car is already rented or the user is not registered, an error will be returned.
#     """
#     car_id = request.car_id
#     user_id = request.user_id

#     # Check if the user is registered
#     if user_id not in users:
#         raise HTTPException(status_code=400, detail="User not registered")

#     # Check if the car is available
#     if car_id in cars and cars[car_id]["status"] == "available":
#         cars[car_id]["status"] = "rented"
#         cars[car_id]["rented_by"] = user_id
#         return {"message": f"{car_id} unlocked and rented successfully by {user_id}!"}
#     raise HTTPException(status_code=400, detail="Car not available")

# @app.post("/return", summary="Return a car", tags=["Rental"])
# async def return_car(request: RentRequest):
#     """
#     Return a rented car by providing the car ID and user ID.
#     - If the car is rented, it will be marked as available.
#     - If the car is not rented, an error will be returned.
#     """
#     car_id = request.car_id
#     user_id = request.user_id

#     # Check if the user is registered
#     if user_id not in users:
#         raise HTTPException(status_code=400, detail="User not registered")

#     # Check if the car is rented
#     if car_id in cars and cars[car_id]["status"] == "rented":
#         cars[car_id]["status"] = "available"
#         cars[car_id]["rented_by"] =""
#         return {"message": f"{car_id} returned successfully! The car will lock soon..."}
#     raise HTTPException(status_code=400, detail="Car not rented or registered")

# @app.get("/user/{user_id}", summary="Get user details", tags=["Users"])
# async def get_user(user_id: str):
#     """
#     Fetches user details by user_id.
#     If the user exists, returns the user details.
#     If the user does not exist, raises an error.
#     """
#     if user_id in users:
#         return {"user_id": user_id, "password": users[user_id]["password"], "card_details":users[user_id]["card_details"]}
#     raise HTTPException(status_code=404, detail="User not found")


# @app.post("/user/login", summary="Login an existing user", tags=["Users"])
# async def login_user(request: LoginRequest):
#     """
#     Logs in an existing user by checking user_id and password.
#     """
#     user = users.get(request.user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     if user["password"] != request.password:
#         raise HTTPException(status_code=401, detail="Incorrect password")

#     return {"message": f"User {request.user_id} logged in successfully!"}


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)
