from flask import Flask, render_template_string, request
import requests
import math

app = Flask(__name__)

API_URL = "https://plant-recommendation-system-hptd.onrender.com/api/plants"

# ==================================================
# HOME PAGE
# ==================================================

@app.route("/")
def home():

    search = request.args.get("search", "").lower()
    page = request.args.get("page", 1, type=int)

    per_page = 6

    try:
        response = requests.get(API_URL)
        data = response.json()

        plants = data.get("plants", [])

    except Exception:
        plants = []

    filtered_plants = []

    for plant in plants:

        plant_name = plant.get("plant_name", "").lower()
        category_name = plant.get("category_name", "").lower()

        if search in plant_name or search in category_name:
            filtered_plants.append(plant)

    total_plants = len(filtered_plants)
    total_pages = max(1, math.ceil(total_plants / per_page))

    start = (page - 1) * per_page
    end = start + per_page

    paginated_plants = filtered_plants[start:end]

    html = """

    <!DOCTYPE html>
    <html>
    <head>

        <title>Plant Recommendation System</title>

        <style>

            body{
                font-family: Arial, sans-serif;
                background:#f0f4f0;
                margin:0;
                padding:20px;
            }

            h1{
                text-align:center;
                color:#2e7d32;
                margin-bottom:25px;
            }

            .search-box{
                text-align:center;
                margin-bottom:30px;
            }

            input[type=text]{
                width:300px;
                padding:12px;
                border:1px solid #ccc;
                border-radius:8px;
            }

            button{
                padding:12px 18px;
                border:none;
                background:#2e7d32;
                color:white;
                border-radius:8px;
                cursor:pointer;
            }

            button:hover{
                background:#1b5e20;
            }

            .container{
                display:flex;
                flex-wrap:wrap;
                justify-content:center;
                gap:20px;
            }

            .card{
                background:white;
                width:320px;
                padding:20px;
                border-radius:12px;
                box-shadow:0px 2px 8px rgba(0,0,0,0.1);
                transition:0.3s;
            }

            .card:hover{
                transform:translateY(-5px);
            }

            .plant-name{
                color:#1b5e20;
                margin-bottom:10px;
            }

            .info{
                margin-bottom:10px;
                color:#444;
            }

            .details-link{
                display:inline-block;
                margin-top:15px;
                padding:10px 15px;
                background:#2e7d32;
                color:white;
                text-decoration:none;
                border-radius:8px;
            }

            .details-link:hover{
                background:#1b5e20;
            }

            .pagination{
                text-align:center;
                margin-top:30px;
            }

            .pagination a{
                display:inline-block;
                margin:5px;
                padding:10px 15px;
                background:white;
                color:#2e7d32;
                text-decoration:none;
                border-radius:8px;
                box-shadow:0px 2px 5px rgba(0,0,0,0.1);
            }

            .pagination a:hover{
                background:#1b5e20;
                color:white;
            }

            .active{
                background:#2e7d32 !important;
                color:white !important;
            }

            .empty{
                text-align:center;
                color:red;
                font-size:20px;
                margin-top:40px;
            }

        </style>

    </head>

    <body>

        <h1>🌱 Plant Recommendation System</h1>

        <div class="search-box">

            <form method="GET">

                <input
                    type="text"
                    name="search"
                    placeholder="Search plant or category..."
                    value="{{ search }}"
                >

                <button type="submit">
                    Search
                </button>

            </form>

        </div>

        {% if plants %}

            <div class="container">

                {% for plant in plants %}

                    <div class="card">

                        <h2 class="plant-name">
                            {{ plant.plant_name }}
                        </h2>

                        <div class="info">
                            <strong>Category:</strong>
                            {{ plant.category_name }}
                        </div>

                        <div class="info">
                            <strong>Light:</strong>
                            {{ plant.light_requirement }}
                        </div>

                        <div class="info">
                            <strong>Watering:</strong>
                            {{ plant.watering_frequency }}
                        </div>

                        <a
                            class="details-link"
                            href="/plant/{{ plant.plant_id }}"
                        >
                            View Details
                        </a>

                    </div>

                {% endfor %}

            </div>

            <div class="pagination">

                {% if current_page > 1 %}
                    <a href="/?page={{ current_page - 1 }}&search={{ search }}">
                        ← Prev
                    </a>
                {% endif %}

                {% for p in range(1, total_pages + 1) %}

                    <a
                        href="/?page={{ p }}&search={{ search }}"
                        class="{% if p == current_page %}active{% endif %}"
                    >
                        {{ p }}
                    </a>

                {% endfor %}

                {% if current_page < total_pages %}
                    <a href="/?page={{ current_page + 1 }}&search={{ search }}">
                        Next →
                    </a>
                {% endif %}

            </div>

        {% else %}

            <div class="empty">
                No plants found.
            </div>

        {% endif %}

    </body>
    </html>

    """

    return render_template_string(
        html,
        plants=paginated_plants,
        search=search,
        total_pages=total_pages,
        current_page=page
    )

# ==================================================
# PLANT DETAILS PAGE
# ==================================================

@app.route("/plant/<int:plant_id>")
def plant_details(plant_id):

    try:
        response = requests.get(API_URL)
        data = response.json()

        plants = data.get("plants", [])

    except Exception:
        plants = []

    selected_plant = None

    for plant in plants:

        if plant.get("plant_id") == plant_id:
            selected_plant = plant
            break

    if not selected_plant:
        return "Plant not found", 404

    html = """

    <!DOCTYPE html>
    <html>
    <head>

        <title>{{ plant.plant_name }}</title>

        <style>

            body{
                font-family:Arial,sans-serif;
                background:#f0f4f0;
                padding:40px;
            }

            .card{
                max-width:700px;
                margin:auto;
                background:white;
                padding:30px;
                border-radius:12px;
                box-shadow:0px 2px 10px rgba(0,0,0,0.1);
            }

            h1{
                color:#1b5e20;
                margin-bottom:20px;
            }

            .info{
                margin-bottom:12px;
                font-size:18px;
            }

            .back-btn{
                display:inline-block;
                margin-top:20px;
                padding:12px 18px;
                background:#2e7d32;
                color:white;
                text-decoration:none;
                border-radius:8px;
            }

        </style>

    </head>

    <body>

        <div class="card">

            <h1>{{ plant.plant_name }}</h1>

            <div class="info"><strong>Plant ID:</strong> {{ plant.plant_id }}</div>

            <div class="info"><strong>Category:</strong> {{ plant.category_name }}</div>

            <div class="info"><strong>Category ID:</strong> {{ plant.category_id }}</div>

            <div class="info"><strong>Growth Rate:</strong> {{ plant.growth_rate }}</div>

            <div class="info"><strong>Humidity Requirement:</strong> {{ plant.humidity_requirement }}</div>

            <div class="info"><strong>Light Requirement:</strong> {{ plant.light_requirement }}</div>

            <div class="info"><strong>Maintenance Level:</strong> {{ plant.maintenance_level }}</div>

            <div class="info"><strong>Size Category:</strong> {{ plant.size_category }}</div>

            <div class="info"><strong>Temperature Range:</strong> {{ plant.temperature_range }}</div>

            <div class="info"><strong>Toxicity Level:</strong> {{ plant.toxicity_level }}</div>

            <div class="info"><strong>Watering Frequency:</strong> {{ plant.watering_frequency }}</div>

            <a href="/" class="back-btn">
                ← Back to Home
            </a>

        </div>

    </body>
    </html>

    """

    return render_template_string(
        html,
        plant=selected_plant
    )

# ==================================================
# RUN APP
# ==================================================

if __name__ == "__main__":
    app.run(debug=True)