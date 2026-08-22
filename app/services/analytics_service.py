from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense


def get_total_expense(
    db: Session,
    user_id: int,
):
    """
    Return the total expense for the authenticated user.
    """

    total = (
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

    return {
        "total_expense": round(
            total,
            2,
        )
    }


def category_summary(
    db: Session,
    user_id: int,
):
    """
    Return category-wise expense summary
    for the authenticated user.
    """

    data = (
        db.query(
            Expense.category,
            func.coalesce(
                func.sum(Expense.amount),
                0,
            ).label("total"),
        )
        .filter(
            Expense.user_id == user_id
        )
        .group_by(
            Expense.category
        )
        .order_by(
            func.sum(Expense.amount).desc()
        )
        .all()
    )

    return [
        {
            "category": row.category,
            "amount": round(
                row.total,
                2,
            ),
        }
        for row in data
    ]