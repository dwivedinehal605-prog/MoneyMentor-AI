from collections import defaultdict


def generate_financial_insights(incomes, expenses):
    """
    Generate financial insights from income and expense data.
    """

    total_income = sum(income.amount for income in incomes)
    total_expense = sum(expense.amount for expense in expenses)

    savings = total_income - total_expense

    savings_rate = (
        (savings / total_income) * 100
        if total_income > 0
        else 0
    )

    # -------------------------------
    # Category-wise Expense Analysis
    # -------------------------------
    category_totals = defaultdict(float)

    for expense in expenses:
        category_totals[expense.category] += expense.amount

    if category_totals:
        highest_spending_category = max(
            category_totals,
            key=category_totals.get,
        )
    else:
        highest_spending_category = "N/A"

    # -------------------------------
    # Monthly Trend Analysis
    # -------------------------------
    monthly_totals = defaultdict(float)

    for expense in expenses:
        month = expense.created_at.strftime("%Y-%m")
        monthly_totals[month] += expense.amount

    months = sorted(monthly_totals.keys())

    if len(months) >= 2:
        previous_month_expense = monthly_totals[months[-2]]
        current_month_expense = monthly_totals[months[-1]]

        if current_month_expense > previous_month_expense:
            monthly_trend = "Increasing"

        elif current_month_expense < previous_month_expense:
            monthly_trend = "Decreasing"

        else:
            monthly_trend = "Stable"

    elif len(months) == 1:
        previous_month_expense = 0
        current_month_expense = monthly_totals[months[0]]
        monthly_trend = "Not enough monthly data"

    else:
        previous_month_expense = 0
        current_month_expense = 0
        monthly_trend = "No expense data"

    # -------------------------------
    # AI Insight
    # -------------------------------
    if savings_rate >= 30:
        insight = (
            f"Excellent! You are saving {savings_rate:.2f}% of your income. "
            f"Your highest spending category is '{highest_spending_category}'. "
            "Keep maintaining this financial discipline."
        )

    elif savings_rate >= 15:
        insight = (
            f"You are saving {savings_rate:.2f}% of your income. "
            f"Try reducing spending in '{highest_spending_category}' "
            "to increase your monthly savings."
        )

    else:
        insight = (
            f"Your savings rate is only {savings_rate:.2f}%. "
            f"You spend the most on '{highest_spending_category}'. "
            "Consider creating a budget and reducing unnecessary expenses."
        )

    # -------------------------------
    # Financial Health Score
    # -------------------------------
    if total_income == 0:
        financial_health_score = 20

    elif savings_rate >= 40:
        financial_health_score = 95

    elif savings_rate >= 30:
        financial_health_score = 85

    elif savings_rate >= 20:
        financial_health_score = 70

    elif savings_rate >= 10:
        financial_health_score = 55

    else:
        financial_health_score = 35

    # -------------------------------
    # Health Status
    # -------------------------------
    if financial_health_score >= 85:
        health_status = "Excellent"

    elif financial_health_score >= 70:
        health_status = "Good"

    elif financial_health_score >= 50:
        health_status = "Average"

    else:
        health_status = "Needs Improvement"

    return {
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2),
        "savings": round(savings, 2),
        "savings_rate": round(savings_rate, 2),
        "highest_spending_category": highest_spending_category,
        "financial_health_score": financial_health_score,
        "health_status": health_status,
        "monthly_trend": monthly_trend,
        "previous_month_expense": round(previous_month_expense, 2),
        "current_month_expense": round(current_month_expense, 2),
        "insight": insight,
    }