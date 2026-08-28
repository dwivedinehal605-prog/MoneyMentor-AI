def generate_budget_alert(
    budget,
    expenses,
):
    """
    Generate budget alert based on
    current spending vs budget.
    """

    if not budget:
        return {
            "alert_level": "Info",
            "message": (
                "No budget has been set yet. "
                "Create a budget to start tracking your spending."
            ),
        }

    spent = sum(
        expense.amount
        for expense in expenses
    )

    budget_amount = (
        budget.budget_amount
    )

    utilization = 0

    if budget_amount > 0:
        utilization = (
            spent /
            budget_amount
        ) * 100

    # -------------------------------
    # Critical Alert
    # -------------------------------

    if utilization >= 100:

        exceeded = round(
            spent - budget_amount,
            2,
        )

        return {
            "alert_level": "Critical",
            "message": (
                f"Your spending is ₹{exceeded} over budget. "
                "Review non-essential expenses and rebalance your finances."
            ),
        }

    # -------------------------------
    # Warning Alert
    # -------------------------------

    elif utilization >= 80:

        remaining = round(
            budget_amount - spent,
            2,
        )

        return {
            "alert_level": "Warning",
            "message": (
                f"You have used over 80% of your budget. "
                f"Only ₹{remaining} remains available for this period."
            ),
        }

    # -------------------------------
    # Safe Alert
    # -------------------------------

    else:

        remaining = round(
            budget_amount - spent,
            2,
        )

        return {
            "alert_level": "Safe",
            "message": (
                f"Your spending is under control. "
                f"₹{remaining} remains in your budget."
            ),
        }