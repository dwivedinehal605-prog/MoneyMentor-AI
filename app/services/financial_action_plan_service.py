def generate_action_plan(insights):

    actions = []

    score = insights["financial_health_score"]

    total_income = insights["total_income"]

    total_expense = insights["total_expense"]

    savings_rate = insights["savings_rate"]

    # ---------------------------------
    # Priority
    # ---------------------------------

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

    # ---------------------------------
    # Income vs Expense
    # ---------------------------------

    if total_expense > total_income:

        actions.append(
            "Your expenses exceed income. Reduce spending immediately."
        )

    # ---------------------------------
    # Savings Rate
    # ---------------------------------

    if savings_rate < 20:

        actions.append(
            "Try to save at least 20% of monthly income."
        )

    elif savings_rate >= 40:

        actions.append(
            "Excellent savings rate. Continue investing regularly."
        )

    return {
        "priority": priority,
        "actions": actions,
    }