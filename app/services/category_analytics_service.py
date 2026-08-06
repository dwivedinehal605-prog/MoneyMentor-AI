from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense


def get_category_analytics(
    db: Session,
    user_id: int,
):
    """
    Generate category-wise
    expense analytics.
    """

    results = (
        db.query(
            Expense.category,
            func.sum(
                Expense.amount
            ).label(
                "total_amount"
            ),
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

    return {
        "categories": [
            {
                "category": category,
                "total_amount": round(
                    total_amount,
                    2,
                ),
            }
            for category, total_amount in results
        ]
    }