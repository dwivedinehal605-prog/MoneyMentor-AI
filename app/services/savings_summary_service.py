from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.income import Income
from app.models.expense import Expense


def get_savings_summary(
    db: Session,
    user_id: int,
):

    total_income = (
        db.query(
            func.coalesce(
                func.sum(
                    Income.amount
                ),
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
                func.sum(
                    Expense.amount
                ),
                0,
            )
        )
        .filter(
            Expense.user_id == user_id
        )
        .scalar()
    )

    total_savings = (
        total_income -
        total_expense
    )

    savings_rate = 0

    if total_income > 0:

        savings_rate = (
            total_savings /
            total_income
        ) * 100

    if savings_rate >= 30:

        status = (
            "Healthy Savings"
        )

    elif savings_rate >= 10:

        status = (
            "Average Savings"
        )

    else:

        status = (
            "Low Savings"
        )

    return {
        "total_income": round(
            total_income,
            2,
        ),
        "total_expense": round(
            total_expense,
            2,
        ),
        "total_savings": round(
            total_savings,
            2,
        ),
        "savings_rate": round(
            savings_rate,
            2,
        ),
        "savings_status": status,
    }