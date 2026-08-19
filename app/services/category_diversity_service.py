from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense


def get_category_diversity(
    db: Session,
    user_id: int,
):
    category_data = (
        db.query(
            Expense.category,
            func.sum(Expense.amount).label("amount"),
        )
        .filter(
            Expense.user_id == user_id
        )
        .group_by(
            Expense.category
        )
        .all()
    )

    if not category_data:
        return {
            "total_categories": 0,
            "total_expense": 0,
            "average_expense_per_category": 0,
            "diversity_status": "Low",
            "message": "No expense data available for analysis.",
        }

    total_categories = len(category_data)

    total_expense = sum(
        float(amount)
        for _, amount in category_data
    )

    average_expense_per_category = (
        total_expense / total_categories
    )

    if total_categories >= 6:
        diversity_status = "High"
        message = (
            "Your spending is spread across many categories."
        )
    elif total_categories >= 3:
        diversity_status = "Moderate"
        message = (
            "Your spending is distributed across several categories."
        )
    else:
        diversity_status = "Low"
        message = (
            "Your spending is concentrated in a small number of categories."
        )

    return {
        "total_categories": total_categories,
        "total_expense": round(total_expense, 2),
        "average_expense_per_category": round(
            average_expense_per_category,
            2,
        ),
        "diversity_status": diversity_status,
        "message": message,
    }
