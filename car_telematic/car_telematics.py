import uuid
import requests
from flask import Flask, jsonify, request
import threading
import atexit
import signal
import os

app = Flask(__name__)

car_telematics = {
    "id": str(uuid.uuid4()),
    "model": "Tesla Model S",
    "license_plate": "ABC123",
    "is_rented": False,
    "current_renter": None,
    "latitude": 47.155392,
    "longitude": 27.635950,
    "speed": 0.0,
    "engine_on": False,
    "headlights_on": False,
    "windows_closed": True,
    "doors_locked": True,
    "trunk_closed": True,
    "fuel_level": 100.0,
    "tire_pressure": 32.0,
    "alarm_active": False
}

BACKEND_URL = "http://127.0.0.1:8000"

@app.route('/telematics', methods=['GET'])
def get_telematics():
    return jsonify(car_telematics)

@app.route('/telematics', methods=['POST'])
def update_telematics():
    data = request.json
    for key, value in data.items():
        if key in car_telematics:
            car_telematics[key] = value
    return jsonify(car_telematics)

def run_server():
    app.run(debug=False, port=5000)

def register_car():
    response = requests.post(f"{BACKEND_URL}/cars", json=car_telematics)
    if response.status_code == 201:
        car_telematics["id"] = response.json()["car_id"]
        print("Car registered successfully.")
    else:
        print("Failed to register car:", response.json())

def delete_car():
    response = requests.delete(f"{BACKEND_URL}/cars/{car_telematics['id']}")
    if response.status_code == 200:
        print("Car deleted successfully.")
    else:
        print("Failed to delete car:", response.json())

def stop_server():
    os.kill(os.getpid(), signal.SIGINT)

def main():
    register_car()

    atexit.register(delete_car)

    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    while True:
        print("\nTelematics Menu:")
        print("1. View telematics data")
        print("2. Update telematics data")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("\nCurrent Telematics Data:")
            for key, value in car_telematics.items():
                print(f"{key}: {value}")

        elif choice == "2":
            print("\nSelect the telematics value to update:")
            keys = list(car_telematics.keys())
            for i, key in enumerate(keys):
                if key != "id":
                    print(f"{i}. {key}")
            selected_key_index = int(input("Enter the number of the telematics value: ").strip())
            selected_key = keys[selected_key_index]
            new_value = input(f"Enter new value for {selected_key}: ").strip()
            if new_value.lower() in ["true", "false"]:
                car_telematics[selected_key] = new_value.lower() == "true"
            elif new_value.replace('.', '', 1).isdigit():
                car_telematics[selected_key] = float(new_value) if '.' in new_value else int(new_value)
            else:
                car_telematics[selected_key] = new_value
            print(f"{selected_key} updated to {car_telematics[selected_key]}")

        elif choice == "3":
            print("Exiting program.")
            delete_car()
            stop_server()
            server_thread.join()
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()