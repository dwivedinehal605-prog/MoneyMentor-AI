from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.income import Income


def get_financial_health_report(
    db: Session,
    user_id: int,
):

    total_income = (
        db.query(
            func.coalesce(
                func.sum(Income.amount),
                0,
            )
        )
        .filter(
            Income.user_id == user_id
        )
        .scalar()
    )

    total_expense = (
        db.query(
            func.coalesce(
                func.sum(Expense.amount),
                0,
            )
        )
        .filter(
            Expense.user_id == user_id
        )
        .scalar()
    )

    savings = (
        total_income -
        total_expense
    )

    score = 100

    if total_income == 0:
        score -= 40

    if savings < 0:
        score -= 30

    if (
        total_income > 0
        and (
            total_expense /
            total_income
        ) > 0.80
    ):
        score -= 20

    score = max(
        0,
        min(score, 100)
    )

    if score >= 80:

        status = "Excellent"

        recommendation = (
            "Maintain your current spending habits."
        )

    elif score >= 60:

        status = "Good"

        recommendation = (
            "Try increasing your monthly savings."
        )

    elif score >= 40:

        status = "Average"

        recommendation = (
            "Reduce non-essential expenses."
        )

    else:

        status = (
            "Needs Improvement"
        )

        recommendation = (
            "Create a strict budget and reduce expenses."
        )

    return {
        "financial_score": score,
        "health_status": status,
        "income": round(
            total_income,
            2,
        ),
        "expense": round(
            total_expense,
            2,
        ),
        "savings": round(
            savings,
            2,
        ),
        "recommendation": recommendation,
    }