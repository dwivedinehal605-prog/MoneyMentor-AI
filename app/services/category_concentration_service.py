from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense


def get_category_concentration(
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
        .order_by(
            func.sum(Expense.amount).desc()
        )
        .all()
    )

    if not category_data:
        return {
            "total_expense": 0,
            "top_category": "N/A",
            "top_category_amount": 0,
            "top_category_percentage": 0,
            "concentration_status": "Low",
            "message": "No expense data available for analysis.",
        }

    total_expense = sum(
        float(amount)
        for _, amount in category_data
    )

    top_category = category_data[0][0]
    top_category_amount = float(
        category_data[0][1]
    )

    if total_expense > 0:
        top_category_percentage = (
            top_category_amount
            / total_expense
        ) * 100
    else:
        top_category_percentage = 0

    if top_category_percentage >= 60:
        concentration_status = "High"
        message = (
            f"A large portion of your spending "
            f"is concentrated in {top_category}."
        )

    elif top_category_percentage >= 40:
        concentration_status = "Moderate"
        message = (
            f"Your spending has moderate "
            f"concentration in {top_category}."
        )

    else:
        concentration_status = "Low"
        message = (
            "Your spending is well distributed "
            "across categories."
        )

    return {
        "total_expense": round(
            total_expense,
            2,
        ),
        "top_category": top_category,
        "top_category_amount": round(
            top_category_amount,
            2,
        ),
        "top_category_percentage": round(
            top_category_percentage,
            2,
        ),
        "concentration_status": concentration_status,
        "message": message,
    }
