import requests

API_URL = "https://plant-recommendation-system-hptd.onrender.com/api/plants"

# ==========================================
# READ OPERATIONS (Allowed for 'user' and 'admin')
# ==========================================

def get_all_plants():
    """Fetches all plants from the external API."""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status() # Raise exception for bad status codes (4xx, 5xx)
        return response.json().get("plants", [])
    except Exception as e:
        print("Error fetching plants:", e)
        return {"error": "Failed to fetch plants."}

def get_plant_by_id(plant_id):
    """Fetches a single plant by its ID."""
    plants = get_all_plants()
    if isinstance(plants, dict) and "error" in plants:
        return plants # Pass the error up if get_all_plants failed
    
    return next((p for p in plants if p.get("plant_id") == plant_id), None)


# ==========================================
# WRITE OPERATIONS (Restricted to 'admin' ONLY)
# ==========================================

def create_plant(plant_data, account_type):
    """Creates a new plant via POST request. Admin only."""
    if account_type != 'admin':
        return {"error": "Unauthorized: Admin access required to create plants."}
    
    try:
        response = requests.post(API_URL, json=plant_data, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Error creating plant:", e)
        return {"error": "Failed to create plant."}

def update_plant(plant_id, plant_data, account_type):
    """Updates an existing plant via PUT request. Admin only."""
    if account_type != 'admin':
        return {"error": "Unauthorized: Admin access required to update plants."}
    
    try:
        response = requests.put(f"{API_URL}/{plant_id}", json=plant_data, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Error updating plant:", e)
        return {"error": "Failed to update plant."}

def delete_plant(plant_id, account_type):
    """Deletes a plant via DELETE request. Admin only."""
    if account_type != 'admin':
        return {"error": "Unauthorized: Admin access required to delete plants."}
    
    try:
        response = requests.delete(f"{API_URL}/{plant_id}", timeout=10)
        response.raise_for_status()
        return {"message": "Plant deleted successfully."}
    except Exception as e:
        print("Error deleting plant:", e)
        return {"error": "Failed to delete plant."}
