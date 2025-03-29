# CarSharing

This project is a full car-sharing application, developed as part of the **ISSA (Automotive-Specific Software Engineering)** course offered by the Continental team at the Faculty of Computer Science in Iași. The application allows users to register, add payment methods and documents, rent cars, and manage the rental process.

## Technologies Used

The project is built using a modern technology stack, including:

### Frontend
- **Angular**: A framework for building web applications.
- **TypeScript**: A typed programming language for frontend development.
- **Leaflet**: A library for displaying interactive maps.
- **HTML5 & CSS3**: For structuring and styling the user interface.

### Backend
- **FastAPI**: A fast framework for developing RESTful APIs.
- **SQLAlchemy**: An ORM for database management.
- **SQLite**: The database used to store application data.
- **APScheduler**: A scheduler for managing recurring tasks (e.g., removing expired rentals).

### Others
- **JWT (JSON Web Tokens)**: Used for user authentication.
- **bcrypt**: For securing user passwords.
- **Flask**: Used to handle car telematics.

## Features

1. **User Registration and Authentication**
   - Users can register and log in using email and password.
   - JWT tokens are used for authentication.

2. **Adding Payment Methods and Documents**
   - Users can add payment methods and documents required for renting cars.

3. **Interactive Map**
   - Users can view available cars on an interactive map and select one for rental.

4. **Car Rental and Return**
   - Users can rent cars for a specific period.
   - The system manages the car status and checks if they can be returned.

5. **Telematics Management**
   - Telematics data from cars (e.g., location, fuel level, engine status) is handled through a Flask server.

6. **Scheduler for Expired Rentals**
   - Expired rentals are automatically deleted, and the car status is updated.

## Project Structure

The project is organized into the following modules:

- **`backend/`** – Contains the API implementation using FastAPI, handling authentication, the database, and business logic.
- **`frontend/`** – Angular web application for the user interface, including the interactive map and rental management.
- **`car-telematic/`** – Module responsible for simulating car telematics, developed in Python using Flask to manage vehicle data.
- **`uml/`** – UML and flow diagrams describing the system’s architecture and functionality.
