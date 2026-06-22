# alg.py

# Ranking scales for partial matching
LIGHT_LEVELS = {
    "low": 1,
    "medium": 2,
    "bright": 3
}

HUMIDITY_LEVELS = {
    "low": 1,
    "medium": 2,
    "high": 3
}

CARE_LEVELS = {
    "easy": 1,
    "medium": 2,
    "hard": 3
}

EXPERIENCE_LEVELS = {
    "beginner": 1,
    "intermediate": 2,
    "advanced": 3
}


def partial_match(user_value, plant_value, scale, max_points):
    """
    Award points based on how close values are.
    """

    user_rank = scale[user_value.lower()]   
    plant_rank = scale[plant_value.lower()]

    difference = abs(user_rank - plant_rank)

    # Exact match
    if difference == 0:
        return max_points

    # Close match   
    elif difference == 1:
        return max_points * 0.5

    # Very different
    return 0


def calculate_score(plant, preferences):
    """
    Calculate score for a plant.
    Maximum possible score = 100
    """

    score = 0

    # Light (25)
    score += partial_match(
        preferences["light"],
        plant["light"],
        LIGHT_LEVELS,
        25
    )

    # Humidity (20)
    score += partial_match(
        preferences["humidity"],
        plant["humidity"],
        HUMIDITY_LEVELS,
        20
    )

    # Care (20)
    score += partial_match(
        preferences["care"],
        plant["care"],
        CARE_LEVELS,
        20
    )

    # Experience (15)
    score += partial_match(
        preferences["experience"],
        plant["experience"],
        EXPERIENCE_LEVELS,
        15
    )

    # Pet Friendly (20)
    if bool(preferences["pet_friendly"]) == bool(plant["pet_friendly"]):
        score += 20

    return round(score, 2)


def recommend_plants(
    plants,
    current_preferences,
    previous_preferences=None,
    top_n=5
):
    """
    Hybrid Recommendation Algorithm

    Case 1:
    No previous data
    -> Use current preferences only

    Case 2:
    Previous data exists
    -> Combine previous and current preferences
    """

    recommendations = []

    for plant in plants:

        # No history available
        if previous_preferences is None:

            final_score = calculate_score(
                plant,
                current_preferences
            )

        # History available
        else:

            previous_score = calculate_score(
                plant,
                previous_preferences
            )

            current_score = calculate_score(
                plant,
                current_preferences
            )

            # Hybrid score
            final_score = (
                previous_score * 0.5 +
                current_score * 0.5
            )

        recommendations.append({
            "id": plant.get("id"),
            "name": plant["name"],
            "score": round(final_score, 2)
        })

    # Highest score first
    recommendations.sort(
        key=lambda plant: plant["score"],
        reverse=True
    )

    return recommendations[:top_n]