from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.expense import Expense


def get_monthly_comparison(
    db: Session,
    user_id: int,
):
    now = datetime.now()

    current_year = now.year
    current_month = now.month

    if current_month == 1:
        previous_year = current_year - 1
        previous_month = 12
    else:
        previous_year = current_year
        previous_month = current_month - 1

    current_total = (
        db.query(
            func.coalesce(
                func.sum(Expense.amount),
                0,
            )
        )
        .filter(
            Expense.user_id == user_id,
            func.extract(
                "year",
                Expense.created_at,
            ) == current_year,
            func.extract(
                "month",
                Expense.created_at,
            ) == current_month,
        )
        .scalar()
    )

    previous_total = (
        db.query(
            func.coalesce(
                func.sum(Expense.amount),
                0,
            )
        )
        .filter(
            Expense.user_id == user_id,
            func.extract(
                "year",
                Expense.created_at,
            ) == previous_year,
            func.extract(
                "month",
                Expense.created_at,
            ) == previous_month,
        )
        .scalar()
    )

    current_total = float(
        current_total or 0
    )

    previous_total = float(
        previous_total or 0
    )

    difference = (
        current_total - previous_total
    )

    if previous_total > 0:
        change_percentage = (
            difference / previous_total
        ) * 100
    else:
        change_percentage = 0

    if difference > 0:
        trend = "Increasing"

        message = (
            f"Your spending increased by "
            f"{abs(change_percentage):.2f}% "
            f"compared with the previous month."
        )

    elif difference < 0:
        trend = "Decreasing"

        message = (
            f"Your spending decreased by "
            f"{abs(change_percentage):.2f}% "
            f"compared with the previous month."
        )

    else:
        trend = "Stable"

        message = (
            "Your spending remained the same "
            "as the previous month."
        )

    return {
        "current_month_expense": round(
            current_total,
            2,
        ),
        "previous_month_expense": round(
            previous_total,
            2,
        ),
        "difference": round(
            difference,
            2,
        ),
        "change_percentage": round(
            change_percentage,
            2,
        ),
        "trend": trend,
        "message": message,
    }