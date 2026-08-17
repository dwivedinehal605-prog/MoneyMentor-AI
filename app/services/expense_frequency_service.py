from collections import Counter
from sqlalchemy.orm import Session

from app.models.expense import Expense


def get_expense_frequency(
    db: Session,
    user_id: int,
):
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

    if not expenses:
        return {
            "total_expenses_analyzed": 0,
            "months_analyzed": 0,
            "average_expenses_per_month": 0,
            "most_active_month": "N/A",
            "highest_monthly_expense_count": 0,
            "frequency_trend": "No Data",
            "message": (
                "No expense records found. "
                "Add expenses to analyze spending frequency."
            ),
        }

    monthly_counts = Counter()

    for expense in expenses:
        if expense.created_at:
            month_key = expense.created_at.strftime(
                "%Y-%m"
            )
            monthly_counts[month_key] += 1

    months_analyzed = len(monthly_counts)

    if months_analyzed == 0:
        return {
            "total_expenses_analyzed": len(expenses),
            "months_analyzed": 0,
            "average_expenses_per_month": 0,
            "most_active_month": "N/A",
            "highest_monthly_expense_count": 0,
            "frequency_trend": "No Data",
            "message": (
                "Expense dates are unavailable "
                "for frequency analysis."
            ),
        }

    average_expenses_per_month = (
        len(expenses) / months_analyzed
    )

    most_active_month = max(
        monthly_counts,
        key=monthly_counts.get,
    )

    highest_monthly_expense_count = (
        monthly_counts[most_active_month]
    )

    if months_analyzed < 2:
        frequency_trend = "Insufficient Data"
        message = (
            "More monthly expense data is needed "
            "to determine your spending frequency trend."
        )
    else:
        monthly_values = list(
            monthly_counts.values()
        )

        if monthly_values[-1] > monthly_values[0]:
            frequency_trend = "Increasing"
            message = (
                "Your expense transaction frequency "
                "is increasing."
            )

        elif monthly_values[-1] < monthly_values[0]:
            frequency_trend = "Decreasing"
            message = (
                "Your expense transaction frequency "
                "is decreasing."
            )

        else:
            frequency_trend = "Stable"
            message = (
                "Your expense transaction frequency "
                "is relatively stable."
            )

    return {
        "total_expenses_analyzed": len(expenses),
        "months_analyzed": months_analyzed,
        "average_expenses_per_month": round(
            average_expenses_per_month,
            2,
        ),
        "most_active_month": most_active_month,
        "highest_monthly_expense_count": (
            highest_monthly_expense_count
        ),
        "frequency_trend": frequency_trend,
        "message": message,
    }