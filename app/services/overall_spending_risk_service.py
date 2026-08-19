from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense


def get_overall_spending_risk(
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
            "top_category_percentage": 0,
            "risk_score": 0,
            "risk_status": "Low",
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

    if top_category_percentage >= 80:
        risk_score = 90
        risk_status = "Critical"
        message = (
            f"Your spending is highly concentrated "
            f"in {top_category}. Immediate spending "
            "diversification is recommended."
        )

    elif top_category_percentage >= 60:
        risk_score = 75
        risk_status = "High"
        message = (
            f"A large portion of your spending is "
            f"concentrated in {top_category}."
        )

    elif top_category_percentage >= 40:
        risk_score = 50
        risk_status = "Moderate"
        message = (
            f"Your spending has moderate concentration "
            f"in {top_category}."
        )

    else:
        risk_score = 20
        risk_status = "Low"
        message = (
            "Your overall spending is reasonably "
            "distributed across categories."
        )

    return {
        "total_expense": round(
            total_expense,
            2,
        ),
        "top_category": top_category,
        "top_category_percentage": round(
            top_category_percentage,
            2,
        ),
        "risk_score": risk_score,
        "risk_status": risk_status,
        "message": message,
    }
