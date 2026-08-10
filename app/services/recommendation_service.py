
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.expense import Expense
from app.models.income import Income


def generate_recommendations(
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

    recommendations = []

    if total_income == 0:
        financial_health = "No Income Data"

        recommendations.append(
            "Add income records to get recommendations."
        )

    else:
        expense_ratio = (
            total_expense /
            total_income
        ) * 100

        if expense_ratio > 90:
            financial_health = "Poor"

            recommendations.extend([
                "Reduce unnecessary expenses.",
                "Create a strict monthly budget.",
                "Increase savings immediately."
            ])

        elif expense_ratio > 70:
            financial_health = "Average"

            recommendations.extend([
                "Track spending more carefully.",
                "Increase monthly savings.",
                "Review high expense categories."
            ])

        else:
            financial_health = "Good"

            recommendations.extend([
                "Keep maintaining your budget.",
                "Invest part of your savings.",
                "Set long-term financial goals."
            ])

    return {
        "financial_health": financial_health,
        "recommendations": recommendations,
    }