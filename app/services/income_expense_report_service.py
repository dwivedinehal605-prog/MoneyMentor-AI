from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.income import Income
from app.models.expense import Expense


def get_income_expense_report(
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

    difference = (
        total_income -
        total_expense
    )

    status = (
        "Surplus"
        if difference >= 0
        else "Deficit"
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
        "difference": round(
            difference,
            2,
        ),
        "status": status,
    }