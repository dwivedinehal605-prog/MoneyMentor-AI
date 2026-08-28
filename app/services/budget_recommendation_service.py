def generate_budget_recommendation(
    expenses,
):
    total_spent = sum(
        expense.amount
        for expense in expenses
    )

    if total_spent == 0:
        return {
            "recommended_budget": 0,
            "basis": "No spending data",
            "message": (
                "Add expenses to receive budget recommendations."
            ),
        }

    recommended_budget = round(
        total_spent * 1.2,
        2,
    )

    return {
    "recommended_budget":
    recommended_budget,

    "basis":
    "Historical spending pattern",

    "message":
    (
        f"Based on your financial activity, we recommend setting a monthly budget of ₹{recommended_budget:,.0f}. "
        "This recommendation includes a 20% safety margin to help manage unexpected expenses and maintain healthy spending habits."
    ),
} 