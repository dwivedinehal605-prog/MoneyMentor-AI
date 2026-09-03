from app.services.insights_service import (
    generate_financial_insights,
)


def generate_financial_advice(
    incomes,
    expenses,
):
    insights = generate_financial_insights(
        incomes,
        expenses,
    )

    advice = []

    savings_rate = insights.get(
        "savings_rate",
        0,
    )

    highest_category = insights.get(
        "highest_spending_category",
        "N/A",
    )

    health_status = insights.get(
        "health_status",
        "Unknown",
    )

    monthly_trend = insights.get(
        "monthly_trend",
        "Unknown",
    )

    # Savings Advice

    if savings_rate >= 30:

        advice.append(
            f"Excellent job. You are saving "
            f"{savings_rate:.2f}% of your income."
        )

    elif savings_rate >= 15:

        advice.append(
            f"You are saving "
            f"{savings_rate:.2f}% of your income. "
            f"Try reaching 30% for stronger "
            f"financial growth."
        )

    else:

        advice.append(
            f"Your savings rate is only "
            f"{savings_rate:.2f}%. "
            f"Consider reducing expenses."
        )

    # Category Advice

    if highest_category != "N/A":

        advice.append(
            f"Your highest spending category is "
            f"'{highest_category}'. Review this "
            f"category for possible savings."
        )

    # Trend Advice

    if monthly_trend == "Increasing":

        advice.append(
            "Your monthly expenses are increasing. "
            "Monitor spending carefully."
        )

    elif monthly_trend == "Decreasing":

        advice.append(
            "Your monthly expenses are decreasing. "
            "Keep maintaining this trend."
        )

    # Health Score Advice

    advice.append(
        f"Current financial health status: "
        f"{health_status}."
    )

    return {
        "advice": advice
    }