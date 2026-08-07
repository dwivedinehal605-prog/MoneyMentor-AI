from collections import defaultdict

from sqlalchemy.orm import Session

from app.models.expense import Expense


def get_monthly_trend(
    db: Session,
    user_id: int,
):
    """
    Generate month-wise expense trend.
    """

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id
        )
        .order_by(
            Expense.created_at.asc()
        )
        .all()
    )

    monthly_totals = defaultdict(float)

    for expense in expenses:

        month = expense.created_at.strftime(
            "%Y-%m"
        )

        monthly_totals[month] += expense.amount

    months = sorted(
        monthly_totals.keys()
    )

    expense_values = [
        round(
            monthly_totals[month],
            2,
        )
        for month in months
    ]

    return {
        "months": months,
        "expenses": expense_values,
    }