from flask import Flask, request, jsonify, Response
from app import recommend_plants
import sqlite3

app = Flask(__name__)

DATABASE = "plants.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/image/<int:plant_id>")
def get_image(plant_id):
    conn = get_db_connection()

    plant = conn.execute(
        "SELECT image FROM plants WHERE id = ?",
        (plant_id,)
    ).fetchone()

    conn.close()

    if plant is None or plant["image"] is None:
        return "Image not found", 404

    return Response(
        plant["image"],
        mimetype="image/png"   # change if your images are png
    )


@app.route("/recommend", methods=["POST"])
def recommend():

    data = request.get_json()

    user_preferences = {
        "light": data["light"].lower(),
        "humidity": data["humidity"].lower(),
        "care": data["care"].lower(),
        "experience": data["experience"].lower(),
        "pet_friendly": data["pet_friendly"]
    }

    recommendations = recommend_plants(user_preferences)

    result = []

    for plant in recommendations:

        plant_data = dict(plant)

        plant_data["image_url"] = (
            f"http://127.0.0.1:5000/image/{plant['id']}"
        )

        result.append(plant_data)

    return jsonify({
        "recommendations": result
    })


if __name__ == "__main__":
    app.run(debug=True)