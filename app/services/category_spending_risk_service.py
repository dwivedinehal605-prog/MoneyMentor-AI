from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense


def get_category_spending_risk(
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
        return []

    total_expense = sum(
        float(amount)
        for _, amount in category_data
    )

    results = []

    for category, amount in category_data:

        current_month_expense = float(amount)

        if total_expense > 0:
            expense_percentage = (
                current_month_expense
                / total_expense
            ) * 100
        else:
            expense_percentage = 0

        if expense_percentage >= 60:
            risk_score = 90
            risk_status = "Critical"
            message = (
                f"{category} accounts for a very large "
                "portion of your total spending."
            )

        elif expense_percentage >= 40:
            risk_score = 70
            risk_status = "High"
            message = (
                f"{category} represents a high portion "
                "of your total spending."
            )

        elif expense_percentage >= 20:
            risk_score = 50
            risk_status = "Moderate"
            message = (
                f"{category} represents a moderate portion "
                "of your total spending."
            )

        else:
            risk_score = 20
            risk_status = "Low"
            message = (
                f"{category} represents a relatively small "
                "portion of your total spending."
            )

        results.append(
            {
                "category": category,
                "current_month_expense": round(
                    current_month_expense,
                    2,
                ),
                "total_expense": round(
                    total_expense,
                    2,
                ),
                "expense_percentage": round(
                    expense_percentage,
                    2,
                ),
                "risk_score": risk_score,
                "risk_status": risk_status,
                "message": message,
            }
        )

    return results
