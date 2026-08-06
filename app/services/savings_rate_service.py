from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.income import Income


def get_savings_rate(
    db: Session,
    user_id: int,
):
    """
    Calculate the user's
    monthly savings rate.
    """

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

    if total_income == 0:

        savings_rate = 0.0

    else:

        savings_rate = (
            total_savings /
            total_income
        ) * 100

    if savings_rate >= 30:

        financial_status = "Excellent"

    elif savings_rate >= 20:

        financial_status = "Healthy"

    elif savings_rate >= 10:

        financial_status = "Average"

    else:

        financial_status = "Needs Improvement"

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
        "financial_status": financial_status,
    }