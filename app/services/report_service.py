from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.income import Income


def get_report_summary(
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

    savings = (
        total_income -
        total_expense
    )

    savings_rate = 0

    if total_income > 0:

        savings_rate = (
            savings /
            total_income
        ) * 100

    return {
        "total_income": round(
            total_income,
            2,
        ),
        "total_expense": round(
            total_expense,
            2,
        ),
        "savings": round(
            savings,
            2,
        ),
        "savings_rate": round(
            savings_rate,
            2,
        ),
    }