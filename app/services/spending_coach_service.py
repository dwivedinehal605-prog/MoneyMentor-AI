def generate_spending_coach(insights):

    tips = []

    score = insights["financial_health_score"]

    # Financial health based advice

    if score >= 80:

        tips.append(
            "Excellent financial health. Continue your current strategy."
        )

    elif score >= 60:

        tips.append(
            "Good financial health. Try increasing your savings rate."
        )

    elif score >= 40:

        tips.append(
            "Your finances are stable but need improvement."
        )

    else:

        tips.append(
            "Reduce unnecessary expenses immediately."
        )

    # Savings advice

    if insights["savings_rate"] < 20:

        tips.append(
            "Aim to save at least 20% of your income."
        )

    # Spending warning

    if insights["total_expense"] > insights["total_income"]:

        tips.append(
            "Your expenses exceed your income."
        )

    # Monthly trend

    trend = insights["monthly_trend"]

    if trend == "Increasing":

        tips.append(
            "Your spending trend is increasing month over month."
        )

    elif trend == "Decreasing":

        tips.append(
            "Good job. Your spending trend is decreasing."
        )

    return {
        "financial_health_score": score,
        "health_status": insights["health_status"],
        "coach_tips": tips,
    }