from collections import defaultdict

from sqlalchemy.orm import Session

from app.models.expense import Expense


def get_spending_trend(
    db: Session,
    user_id: int,
):
    """
    Analyze the user's monthly spending trend
    by comparing the current month's expenses
    with the previous month's expenses.
    """

    # =====================================
    # Fetch Expense Records
    # =====================================

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

    # =====================================
    # Calculate Monthly Totals
    # =====================================

    monthly_totals = defaultdict(float)

    for expense in expenses:

        month = expense.created_at.strftime(
            "%Y-%m"
        )

        monthly_totals[month] += expense.amount

    months = sorted(
        monthly_totals.keys()
    )

    # =====================================
    # No Expense Records
    # =====================================

    if not months:

        return {
            "trend": "No Data",
            "change_percentage": 0.0,
            "current_month_expense": 0.0,
            "previous_month_expense": 0.0,
        }

    # =====================================
    # Only One Month Available
    # =====================================

    if len(months) < 2:

        return {
            "trend": "Insufficient Data",
            "change_percentage": 0.0,
            "current_month_expense": round(
                monthly_totals[months[-1]],
                2,
            ),
            "previous_month_expense": 0.0,
        }

    # =====================================
    # Compare Current vs Previous Month
    # =====================================

    previous_month_expense = monthly_totals[
        months[-2]
    ]

    current_month_expense = monthly_totals[
        months[-1]
    ]

    if previous_month_expense == 0:

        change_percentage = 100.0

    else:

        change_percentage = (
            (
                current_month_expense
                - previous_month_expense
            )
            / previous_month_expense
        ) * 100

    if change_percentage > 0:

        trend = "Increasing"

    elif change_percentage < 0:

        trend = "Decreasing"

    else:

        trend = "Stable"

    # =====================================
    # Response
    # =====================================

    return {
        "trend": trend,
        "change_percentage": round(
            change_percentage,
            2,
        ),
        "current_month_expense": round(
            current_month_expense,
            2,
        ),
        "previous_month_expense": round(
            previous_month_expense,
            2,
        ),
    }