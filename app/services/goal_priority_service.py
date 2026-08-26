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


def get_goal_priority(goals):

    if not goals:
        return {
            "highest_priority_goal": "No Goal",
            "priority_score": 0,
            "reason": "No active goals found.",
        }

    best_goal = None
    best_score = -1

    for goal in goals:

        score = PRIORITY_MAP.get(
            goal.title.lower(),
            50,
        )

        if score > best_score:
            best_score = score
            best_goal = goal

    reason = (
        "Emergency funds should be completed before discretionary goals."
        if best_score >= 100
        else "Focus on the highest priority financial goal first."
    )

    return {
        "highest_priority_goal": best_goal.title,
        "priority_score": best_score,
        "reason": reason,
    }