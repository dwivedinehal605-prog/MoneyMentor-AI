from collections import defaultdict

from sqlalchemy.orm import Session

from app.models.expense import Expense


def get_expense_volatility(
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

    monthly_expenses = defaultdict(float)

    for expense in expenses:
        if expense.created_at is None:
            continue

        month_key = expense.created_at.strftime(
            "%Y-%m"
        )

        monthly_expenses[month_key] += float(
            expense.amount or 0
        )

    values = list(
        monthly_expenses.values()
    )

    if not values:
        return {
            "months_analyzed": 0,
            "average_monthly_expense": 0,
            "highest_monthly_expense": 0,
            "lowest_monthly_expense": 0,
            "volatility_percentage": 0,
            "volatility_status": "No Data",
            "message": (
                "No expense data available "
                "for volatility analysis."
            ),
        }

    average_expense = (
        sum(values) / len(values)
    )

    highest_expense = max(values)
    lowest_expense = min(values)

    if average_expense > 0:
        volatility_percentage = (
            (
                highest_expense -
                lowest_expense
            )
            / average_expense
        ) * 100
    else:
        volatility_percentage = 0

    if volatility_percentage <= 25:
        volatility_status = "Stable"
        message = (
            "Your monthly spending is relatively stable."
        )

    elif volatility_percentage <= 50:
        volatility_status = "Moderate"
        message = (
            "Your monthly spending shows moderate "
            "variation."
        )

    else:
        volatility_status = "High"
        message = (
            "Your monthly spending is highly variable. "
            "Consider maintaining a more consistent budget."
        )

    return {
        "months_analyzed": len(values),
        "average_monthly_expense": round(
            average_expense,
            2,
        ),
        "highest_monthly_expense": round(
            highest_expense,
            2,
        ),
        "lowest_monthly_expense": round(
            lowest_expense,
            2,
        ),
        "volatility_percentage": round(
            volatility_percentage,
            2,
        ),
        "volatility_status": volatility_status,
        "message": message,
    }
