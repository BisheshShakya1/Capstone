# CRUD.py
import requests

API_URL = "https://plant-recommendation-system-hptd.onrender.com/api/plants"

def get_all_plants():
    """Fetches all plants from the external API."""
    try:
        response = requests.get(API_URL, timeout=10)
        return response.json().get("plants", [])
    except Exception as e:
        print("Error fetching plants:", e)
        return []

def get_plant_by_id(plant_id):
    """Fetches a single plant by its ID."""
    plants = get_all_plants()
    return next((p for p in plants if p.get("plant_id") == plant_id), None)

def create_plant(plant_data):
    """Creates a new plant via POST request."""
    try:
        return requests.post(API_URL, json=plant_data, timeout=10)
    except Exception as e:
        print("Error creating plant:", e)
        return None

def update_plant(plant_id, plant_data):
    """Updates an existing plant via PUT request."""
    try:
        return requests.put(f"{API_URL}/{plant_id}", json=plant_data, timeout=10)
    except Exception as e:
        print("Error updating plant:", e)
        return None

def delete_plant(plant_id):
    """Deletes a plant via DELETE request."""
    try:
        return requests.delete(f"{API_URL}/{plant_id}", timeout=10)
    except Exception as e:
        print("Error deleting plant:", e)
        return None
