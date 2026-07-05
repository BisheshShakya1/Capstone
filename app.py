# app.py
from flask import Flask, render_template_string, request, redirect, url_for, jsonify
from flask_cors import CORS
import math

# Import your custom modules
import CRUD
import alg

def create_app():
    app = Flask(__name__)
    CORS(app)

    # ==================================================
    # HTML TEMPLATES
    # ==================================================
    BASE_STYLE = """
        body { font-family: Arial, sans-serif; background: #f0f4f0; margin: 0; padding: 20px; }
        h1 { text-align: center; color: #2e7d32; margin-bottom: 25px; }
        .container { max-width: 1200px; margin: auto; }
        .search-box { text-align: center; margin-bottom: 30px; }
        input[type=text], input[type=number] { width: 300px; padding: 12px; border: 1px solid #ccc; border-radius: 8px; }
        button, .btn { padding: 12px 18px; border: none; background: #2e7d32; color: white; border-radius: 8px; cursor: pointer; text-decoration: none; display: inline-block; font-size: 16px; }
        button:hover, .btn:hover { background: #1b5e20; }
        .btn-orange { background: #f57c00; } .btn-orange:hover { background: #e65100; }
        .btn-red { background: #d32f2f; } .btn-red:hover { background: #b71c1c; }
        .cards { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; }
        .card { background: white; width: 320px; padding: 20px; border-radius: 12px; box-shadow: 0px 2px 8px rgba(0,0,0,0.1); transition: 0.3s; }
        .card:hover { transform: translateY(-5px); }
        .plant-name { color: #1b5e20; margin-bottom: 10px; }
        .info { margin-bottom: 10px; color: #444; }
        .details-link { margin-top: 15px; }
        .pagination { text-align: center; margin-top: 30px; }
        .pagination a { display: inline-block; margin: 5px; padding: 10px 15px; background: white; color: #2e7d32; text-decoration: none; border-radius: 8px; box-shadow: 0px 2px 5px rgba(0,0,0,0.1); }
        .pagination a:hover { background: #1b5e20; color: white; }
        .active { background: #2e7d32 !important; color: white !important; }
        .empty { text-align: center; color: red; font-size: 20px; margin-top: 40px; }
        .actions { margin-top: 20px; display: flex; gap: 10px; }
        .form-container { max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0px 2px 10px rgba(0,0,0,0.1); }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; color: #1b5e20; }
        .form-control { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 8px; box-sizing: border-box; }
    """

    HOME_HTML = """<!DOCTYPE html><html><head><title>Plant System</title><style>""" + BASE_STYLE + """</style></head><body><div class="container"><h1>🌱 Plant Recommendation System</h1><div style="text-align: right; margin-bottom: 20px;"><a href="/add" class="btn">+ Add New Plant</a></div><div class="search-box"><form method="GET"><input type="text" name="search" placeholder="Search plant or category..." value="{{ search }}"><button type="submit">Search</button></form></div>{% if plants %}<div class="cards">{% for plant in plants %}<div class="card"><h2 class="plant-name">{{ plant.plant_name }}</h2><div class="info"><strong>Category:</strong> {{ plant.category_name }}</div><div class="info"><strong>Light:</strong> {{ plant.light_requirement }}</div><div class="info"><strong>Watering:</strong> {{ plant.watering_frequency }}</div><a class="btn details-link" href="/plant/{{ plant.plant_id }}">View Details</a></div>{% endfor %}</div><div class="pagination">{% if current_page > 1 %}<a href="/?page={{ current_page - 1 }}&search={{ search }}">← Prev</a>{% endif %}{% for p in range(1, total_pages + 1) %}<a href="/?page={{ p }}&search={{ search }}" class="{% if p == current_page %}active{% endif %}">{{ p }}</a>{% endfor %}{% if current_page < total_pages %}<a href="/?page={{ current_page + 1 }}&search={{ search }}">Next →</a>{% endif %}</div>{% else %}<div class="empty">No plants found.</div>{% endif %}</div></body></html>"""

    DETAILS_HTML = """<!DOCTYPE html><html><head><title>{{ plant.plant_name }}</title><style>""" + BASE_STYLE + """ .detail-card { max-width: 700px; margin: auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0px 2px 10px rgba(0,0,0,0.1); } .detail-card h1 { text-align: left; }</style></head><body><div class="detail-card"><h1>{{ plant.plant_name }}</h1><div class="info"><strong>Plant ID:</strong> {{ plant.plant_id }}</div><div class="info"><strong>Category:</strong> {{ plant.category_name }}</div><div class="info"><strong>Growth Rate:</strong> {{ plant.growth_rate }}</div><div class="info"><strong>Light Requirement:</strong> {{ plant.light_requirement }}</div><div class="info"><strong>Watering Frequency:</strong> {{ plant.watering_frequency }}</div><div class="actions"><a href="/" class="btn">← Back</a><a href="/edit/{{ plant.plant_id }}" class="btn btn-orange">Edit</a><form method="POST" action="/delete/{{ plant.plant_id }}" style="display:inline;" onsubmit="return confirm('Are you sure?');"><button type="submit" class="btn btn-red">Delete</button></form></div></div></body></html>"""

    FORM_HTML = """<!DOCTYPE html><html><head><title>{{ "Edit" if plant else "Add" }} Plant</title><style>""" + BASE_STYLE + """</style></head><body><div class="container"><h1>{{ "Edit" if plant else "Add" }} Plant</h1><div class="form-container"><form method="POST"><div class="form-group"><label>Plant Name *</label><input type="text" name="plant_name" class="form-control" value="{{ plant.plant_name if plant else '' }}" required></div><div class="form-group"><label>Category Name</label><input type="text" name="category_name" class="form-control" value="{{ plant.category_name if plant else '' }}"></div><div class="form-group"><label>Category ID</label><input type="number" name="category_id" class="form-control" value="{{ plant.category_id if plant else '' }}"></div><div class="form-group"><label>Growth Rate</label><input type="text" name="growth_rate" class="form-control" value="{{ plant.growth_rate if plant else '' }}"></div><div class="form-group"><label>Humidity Requirement</label><input type="text" name="humidity_requirement" class="form-control" value="{{ plant.humidity_requirement if plant else '' }}"></div><div class="form-group"><label>Light Requirement</label><input type="text" name="light_requirement" class="form-control" value="{{ plant.light_requirement if plant else '' }}"></div><div class="form-group"><label>Maintenance Level</label><input type="text" name="maintenance_level" class="form-control" value="{{ plant.maintenance_level if plant else '' }}"></div><div class="form-group"><label>Size Category</label><input type="text" name="size_category" class="form-control" value="{{ plant.size_category if plant else '' }}"></div><div class="form-group"><label>Temperature Range</label><input type="text" name="temperature_range" class="form-control" value="{{ plant.temperature_range if plant else '' }}"></div><div class="form-group"><label>Toxicity Level</label><input type="text" name="toxicity_level" class="form-control" value="{{ plant.toxicity_level if plant else '' }}"></div><div class="form-group"><label>Watering Frequency</label><input type="text" name="watering_frequency" class="form-control" value="{{ plant.watering_frequency if plant else '' }}"></div><button type="submit" class="btn">Save Plant</button><a href="/" class="btn" style="background:#757575; margin-left:10px;">Cancel</a></form></div></div></body></html>"""

    # ==================================================
    # HELPER: Map API data to alg.py's expected format
    # ==================================================
    def map_plant_for_alg(api_plant):
        """Translates API fields (e.g., light_requirement) to alg.py fields (e.g., light)"""
        light_raw = str(api_plant.get("light_requirement", "medium")).lower()
        light = "low" if "low" in light_raw else ("bright" if "bright" in light_raw or "high" in light_raw else "medium")

        hum_raw = str(api_plant.get("humidity_requirement", "medium")).lower()
        humidity = "low" if "low" in hum_raw else ("high" if "high" in hum_raw else "medium")

        care_raw = str(api_plant.get("maintenance_level", "medium")).lower()
        care = "easy" if "easy" in care_raw or "low" in care_raw else ("hard" if "hard" in care_raw or "high" in care_raw else "medium")

        toxicity_raw = str(api_plant.get("toxicity_level", "")).lower()
        pet_friendly = "non-toxic" in toxicity_raw or "safe" in toxicity_raw or toxicity_raw == "false"

        return {
            "id": api_plant.get("plant_id"),
            "name": api_plant.get("plant_name", "Unknown"),
            "light": light,
            "humidity": humidity,
            "care": care,
            "experience": "beginner",  # Default since API doesn't track experience
            "pet_friendly": pet_friendly
        }

    # ==================================================
    # HTML ROUTES (Calling CRUD.py)
    # ==================================================
    @app.route("/")
    def home():
        search = request.args.get("search", "").lower()
        page = request.args.get("page", 1, type=int)
        per_page = 6

        plants = CRUD.get_all_plants() # <--- CALLING CRUD
        filtered_plants = [p for p in plants if search in p.get("plant_name", "").lower() or search in p.get("category_name", "").lower()]
        
        total_pages = max(1, math.ceil(len(filtered_plants) / per_page))
        start = (page - 1) * per_page
        end = start + per_page
        return render_template_string(HOME_HTML, plants=filtered_plants[start:end], search=search, total_pages=total_pages, current_page=page)

    @app.route("/plant/<int:plant_id>")
    def plant_details(plant_id):
        plant = CRUD.get_plant_by_id(plant_id) # <--- CALLING CRUD
        if not plant: return "Plant not found", 404
        return render_template_string(DETAILS_HTML, plant=plant)

    @app.route("/add", methods=["GET", "POST"])
    def add_plant():
        if request.method == "POST":
            new_plant = {k: request.form.get(k) for k in ["plant_name", "category_name", "growth_rate", "humidity_requirement", "light_requirement", "maintenance_level", "size_category", "temperature_range", "toxicity_level", "watering_frequency"]}
            new_plant["category_id"] = int(request.form.get("category_id")) if request.form.get("category_id") else None
            CRUD.create_plant(new_plant) # <--- CALLING CRUD
            return redirect(url_for("home"))
        return render_template_string(FORM_HTML, plant=None)

    @app.route("/edit/<int:plant_id>", methods=["GET", "POST"])
    def edit_plant(plant_id):
        if request.method == "POST":
            updated_plant = {k: request.form.get(k) for k in ["plant_name", "category_name", "growth_rate", "humidity_requirement", "light_requirement", "maintenance_level", "size_category", "temperature_range", "toxicity_level", "watering_frequency"]}
            updated_plant["category_id"] = int(request.form.get("category_id")) if request.form.get("category_id") else None
            CRUD.update_plant(plant_id, updated_plant) # <--- CALLING CRUD
            return redirect(url_for("plant_details", plant_id=plant_id))
        
        plant = CRUD.get_plant_by_id(plant_id) # <--- CALLING CRUD
        if not plant: return "Plant not found", 404
        return render_template_string(FORM_HTML, plant=plant)

    @app.route("/delete/<int:plant_id>", methods=["POST"])
    def delete_plant(plant_id):
        CRUD.delete_plant(plant_id) # <--- CALLING CRUD
        return redirect(url_for("home"))

    # ==================================================
    # JSON API ENDPOINTS (Calling CRUD.py & alg.py)
    # ==================================================
    @app.route("/api/plants", methods=["GET"])
    def api_get_all_plants():
        return jsonify({"plants": CRUD.get_all_plants()}), 200

    @app.route("/api/recommend", methods=["POST"])
    def api_recommend_plants():
        """
        Calls alg.py to get recommendations.
        Expects JSON: {"preferences": {...}, "top_n": 5}
        """
        data = request.get_json()
        if not data or "preferences" not in data:
            return jsonify({"error": "Missing 'preferences' in JSON body"}), 400

        # 1. Get raw data from CRUD
        raw_plants = CRUD.get_all_plants() 
        
        # 2. Map data so alg.py doesn't crash on missing keys
        mapped_plants = [map_plant_for_alg(p) for p in raw_plants]
        
        # 3. Call alg.py
        try:
            recommendations = alg.recommend_plants(
                plants=mapped_plants,
                current_preferences=data["preferences"],
                top_n=data.get("top_n", 5)
            )
            return jsonify({"recommendations": recommendations}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app

# ==================================================
# RUN APP
# ==================================================
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
