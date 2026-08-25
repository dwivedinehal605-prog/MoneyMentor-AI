from datetime import date


def generate_goal_recommendation(goal):

    today = date.today()

    remaining_amount = (
        goal.target_amount
        - goal.saved_amount
    )

    days_left = (
        goal.deadline
        - today
    ).days

    if days_left <= 0:

        return {
            "title": goal.title,

            "target_amount": goal.target_amount,
            "saved_amount": goal.saved_amount,

            "remaining_amount": remaining_amount,

            "months_left": 0,

            "required_monthly_saving": 0,
            "required_daily_saving": 0,

            "goal_probability": "Expired",

            "recommendation":
            "Goal deadline has already passed.",
        }

    months_left = max(
        1,
        round(days_left / 30),
    )

    required_monthly_saving = (
        remaining_amount
        / months_left
    )

    required_daily_saving = (
        remaining_amount
        / days_left
    )

    progress_percentage = (
        goal.saved_amount
        / goal.target_amount
    ) * 100

    if progress_percentage >= 80:
        probability = "High"

        recommendation = (
            "You are on track to achieve this goal."
        )

    elif progress_percentage >= 50:
        probability = "Medium"

        recommendation = (
            "Increase monthly savings slightly."
        )

    else:
        probability = "Low"

        recommendation = (
            "Current savings rate is too low."
        )

    return {
        "title": goal.title,

        "target_amount": round(
            goal.target_amount,
            2,
        ),

        "saved_amount": round(
            goal.saved_amount,
            2,
        ),

        "remaining_amount": round(
            remaining_amount,
            2,
        ),

        "months_left": months_left,

        "required_monthly_saving": round(
            required_monthly_saving,
            2,
        ),

        "required_daily_saving": round(
            required_daily_saving,
            2,
        ),

        "goal_probability": probability,

        "recommendation": recommendation,
    }