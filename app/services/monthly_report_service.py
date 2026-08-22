from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.income import Income
from app.models.expense import Expense


def get_monthly_report(
    db: Session,
    user_id: int,
):
    """
    Generate a financial report for the current user's
    income, expenses, savings, and savings rate.

    The report is user-specific and only includes records
    belonging to the authenticated user.
    """

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

    total_income = float(total_income or 0)
    total_expense = float(total_expense or 0)

    total_savings = (
        total_income - total_expense
    )

    savings_rate = 0.0

    if total_income > 0:
        savings_rate = (
            total_savings / total_income
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
        "total_savings": round(
            total_savings,
            2,
        ),
        "savings_rate": round(
            savings_rate,
            2,
        ),
    }