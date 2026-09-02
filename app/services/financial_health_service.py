from sqlalchemy.orm import Session

from app.models.income import Income
from app.models.expense import Expense
from app.models.budget import Budget
from app.models.savings_goal import SavingsGoal


def get_financial_health_score(
    db: Session,
    user_id: int,
):
    incomes = (
        db.query(Income)
        .filter(Income.user_id == user_id)
        .all()
    )

    expenses = (
        db.query(Expense)
        .filter(Expense.user_id == user_id)
        .all()
    )

    budgets = (
        db.query(Budget)
        .filter(Budget.user_id == user_id)
        .all()
    )

    goals = (
        db.query(SavingsGoal)
        .filter(SavingsGoal.user_id == user_id)
        .all()
    )

    total_income = sum(
        income.amount
        for income in incomes
    )

    total_expense = sum(
        expense.amount
        for expense in expenses
    )

    savings = max(
        total_income - total_expense,
        0,
    )

    score = 0

    # Savings Rate (40 points)

    if total_income > 0:

        savings_rate = (
            savings / total_income
        ) * 100

        score += min(
            40,
            savings_rate * 0.4,
        )

    else:
        savings_rate = 0

    # Budget Usage (30 points)

    total_budget = sum(
    budget.budget_amount
    for budget in budgets
    )

    if total_budget > 0:

        budget_usage = (
            total_expense
            / total_budget
        ) * 100

        if budget_usage <= 80:
            score += 30

        elif budget_usage <= 100:
            score += 20

        else:
            score += 10

    else:
        budget_usage = 0

    # Savings Goals Progress (30 points)

    if goals:

        progress_values = []

        for goal in goals:

            if goal.target_amount > 0:

                progress = (
                    goal.saved_amount
                    / goal.target_amount
                ) * 100

                progress_values.append(
                    min(progress, 100)
                )

        avg_progress = (
            sum(progress_values)
            / len(progress_values)
            if progress_values
            else 0
        )

        score += (
            avg_progress * 0.3
        )

    else:
        avg_progress = 0

    score = round(score)

    if score >= 80:
        rating = "Excellent"

    elif score >= 60:
        rating = "Good"

    elif score >= 40:
        rating = "Average"

    else:
        rating = "Poor"

    recommendations = []

    if savings_rate < 20:
        recommendations.append(
            "Increase monthly savings."
        )

    if total_budget > 0 and budget_usage > 100:
        recommendations.append(
            "Reduce spending to stay within budget."
        )

    if avg_progress < 50:
        recommendations.append(
            "Increase contributions towards savings goals."
        )

    return {
        "score": score,
        "rating": rating,
        "savings_rate": round(
            savings_rate,
            2,
        ),
        "budget_usage": round(
            budget_usage,
            2,
        ),
        "goal_progress": round(
            avg_progress,
            2,
        ),
        "recommendations": recommendations,
    }