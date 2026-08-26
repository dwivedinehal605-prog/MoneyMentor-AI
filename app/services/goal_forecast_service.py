import math

PRIORITY_MAP = {
    "emergency fund": 100,
    "education": 90,
    "home": 80,
    "house": 80,
    "vehicle": 70,
    "car": 70,
    "bike": 70,
    "laptop": 60,
    "vacation": 40,
}


def generate_goal_forecast(
    goals,
    monthly_savings_capacity,
):
    if not goals:
        return {
            "forecasts": []
        }

    scored_goals = []
    total_score = 0

    for goal in goals:

        score = PRIORITY_MAP.get(
            goal.title.lower(),
            50,
        )

        scored_goals.append(
            (goal, score)
        )

        total_score += score

    forecasts = []

    for goal, score in scored_goals:

        monthly_allocation = round(
            (
                score /
                total_score
            )
            *
            monthly_savings_capacity,
            2,
        )

        remaining_amount = max(
            goal.target_amount -
            goal.saved_amount,
            0,
        )

        if monthly_allocation > 0:
            months_to_complete = math.ceil(
                remaining_amount /
                monthly_allocation
            )
        else:
            months_to_complete = 0

        forecasts.append(
            {
                "goal": goal.title,
                "remaining_amount": round(
                    remaining_amount,
                    2,
                ),
                "monthly_allocation":
                monthly_allocation,
                "months_to_complete":
                months_to_complete,
            }
        )

    return {
        "forecasts": forecasts
    }