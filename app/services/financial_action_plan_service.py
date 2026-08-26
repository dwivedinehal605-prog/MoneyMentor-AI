from datetime import date


def generate_action_plan(
    insights,
    goals,
):

    actions = []
    goal_actions = []

    score = insights["financial_health_score"]

    total_income = insights["total_income"]
    total_expense = insights["total_expense"]
    savings_rate = insights["savings_rate"]

    # -------------------------
    # Financial Health
    # -------------------------

    if score < 40:

        priority = "High"

        actions.append(
            "Reduce non-essential expenses immediately."
        )

        actions.append(
            "Create a monthly savings target."
        )

        actions.append(
            "Increase income sources."
        )

    elif score < 70:

        priority = "Medium"

        actions.append(
            "Increase savings rate."
        )

        actions.append(
            "Monitor monthly expenses."
        )

    else:

        priority = "Low"

        actions.append(
            "Maintain current financial habits."
        )

    # -------------------------
    # Income vs Expense
    # -------------------------

    if total_expense > total_income:

        actions.append(
            "Your expenses exceed income. Reduce spending immediately."
        )

    if savings_rate < 20:

        actions.append(
            "Try to save at least 20% of monthly income."
        )

    # -------------------------
    # Goal Based Recommendations
    # -------------------------

    today = date.today()

    for goal in goals:

        remaining = (
            goal.target_amount -
            goal.saved_amount
        )

        if remaining <= 0:

            goal_actions.append(
                f"{goal.title} already achieved."
            )

            continue

        months_left = (
            (goal.deadline.year - today.year) * 12
            +
            (goal.deadline.month - today.month)
        )

        if months_left <= 0:
            months_left = 1

        monthly_required = round(
            remaining / months_left,
            2,
        )

        goal_actions.append(
            f"Save ₹{monthly_required} per month for {goal.title}."
        )

    return {
        "priority": priority,
        "actions": actions,
        "goal_actions": goal_actions,
    }