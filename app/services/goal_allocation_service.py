from datetime import date


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
            "total_allocated": 0,
            "remaining_capacity": 0,
            "allocations": [],
        }

    scored_goals = []

    total_score = 0

    for goal in goals:

        if goal.saved_amount >= goal.target_amount:
            continue

        remaining_amount = (
            goal.target_amount
            - goal.saved_amount
        )

        days_left = max(
            (
                goal.deadline
                - date.today()
            ).days,
            1,
        )

        months_left = max(
            days_left / 30,
            1,
        )

        monthly_required = (
            remaining_amount
            / months_left
        )

        title_priority = PRIORITY_MAP.get(
            goal.title.lower(),
            50,
        )

        urgency_score = (
            monthly_required / 1000
        )

        progress_score = (
            100
            -
            (
                goal.saved_amount
                /
                goal.target_amount
            )
            * 100
        )

        final_score = (
            title_priority
            + urgency_score
            + progress_score
        )

        total_score += final_score

        scored_goals.append(
            {
                "goal": goal,
                "score": final_score,
                "monthly_required":
                monthly_required,
                "remaining_amount":
                remaining_amount,
            }
        )

    allocations = []

    allocated_total = 0

    for item in scored_goals:

        allocation = round(
            (
                item["score"]
                / total_score
            )
            * monthly_savings_capacity,
            2,
        )

        allocated_total += allocation

        allocations.append(
            {
                "goal":
                item["goal"].title,

                "remaining_amount":
                round(
                    item["remaining_amount"],
                    2,
                ),

                "monthly_required":
                round(
                    item["monthly_required"],
                    2,
                ),

                "recommended_allocation":
                allocation,

                "funding_status":
                (
                    "On Track"
                    if allocation
                    >= item["monthly_required"]
                    else "Needs More Funding"
                ),
            }
        )

    return {
        "monthly_savings_capacity":
        monthly_savings_capacity,

        "total_allocated":
        round(
            allocated_total,
            2,
        ),

        "remaining_capacity":
        round(
            monthly_savings_capacity
            - allocated_total,
            2,
        ),

        "allocations":
        allocations,
    }