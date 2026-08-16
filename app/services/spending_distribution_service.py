from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense


def get_spending_distribution(
    db: Session,
    user_id: int,
):
    """
    Calculate how the user's total expenses
    are distributed across categories.
    """

    category_data = (
        db.query(
            Expense.category,
            func.sum(
                Expense.amount
            ).label("total"),
        )
        .filter(
            Expense.user_id == user_id
        )
        .group_by(
            Expense.category
        )
        .order_by(
            func.sum(
                Expense.amount
            ).desc()
        )
        .all()
    )

    if not category_data:
        return {
            "total_expense": 0.0,
            "categories": [],
        }

    total_expense = sum(
        float(row.total or 0)
        for row in category_data
    )

    categories = []

    for row in category_data:

        amount = float(
            row.total or 0
        )

        percentage = 0.0

        if total_expense > 0:
            percentage = (
                amount / total_expense
            ) * 100

        categories.append(
            {
                "category": (
                    row.category
                    or "Uncategorized"
                ),
                "amount": round(
                    amount,
                    2,
                ),
                "percentage": round(
                    percentage,
                    2,
                ),
            }
        )

    return {
        "total_expense": round(
            total_expense,
            2,
        ),
        "categories": categories,
    }