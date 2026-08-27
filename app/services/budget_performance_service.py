def get_budget_performance(
    budget,
    expenses,
):
    if not budget:
        return {
            "budget": 0,
            "spent": 0,
            "remaining": 0,
            "utilization_percentage": 0,
            "status": "No Budget Found",
        }

    spent = sum(
        expense.amount
        for expense in expenses
    )

    remaining = (
        budget.budget_amount - spent
    )

    utilization_percentage = 0

    if budget.budget_amount > 0:
        utilization_percentage = round(
            (
                spent /
                budget.budget_amount
            ) * 100,
            2,
        )

    if utilization_percentage >= 100:
        status = "Budget Exceeded"
    elif utilization_percentage >= 80:
        status = "Warning"
    else:
        status = "On Track"

    return {
        "budget": budget.budget_amount,
        "spent": round(spent, 2),
        "remaining": round(remaining, 2),
        "utilization_percentage": utilization_percentage,
        "status": status,
    }