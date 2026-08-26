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


def generate_goal_allocation(
    goals,
    monthly_savings_capacity,
):

    if not goals:

        return {
            "monthly_savings_capacity": 0,
            "allocations": [],
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

    allocations = []

    for goal, score in scored_goals:

        allocation = round(
            (
                score /
                total_score
            )
            *
            monthly_savings_capacity,
            2,
        )

        allocations.append(
            {
                "goal": goal.title,
                "allocation": allocation,
            }
        )

    return {
        "monthly_savings_capacity":
        monthly_savings_capacity,
        "allocations":
        allocations,
    }