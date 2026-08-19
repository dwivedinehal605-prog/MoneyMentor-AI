from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense


def get_category_trend_score(
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

    current_data = (
        db.query(
            Expense.category,
            func.sum(Expense.amount).label("amount"),
        )
        .filter(
            Expense.user_id == user_id,
            func.extract("year", Expense.created_at)
            == current_year,
            func.extract("month", Expense.created_at)
            == current_month,
        )
        .group_by(Expense.category)
        .all()
    )

    previous_data = (
        db.query(
            Expense.category,
            func.sum(Expense.amount).label("amount"),
        )
        .filter(
            Expense.user_id == user_id,
            func.extract("year", Expense.created_at)
            == previous_year,
            func.extract("month", Expense.created_at)
            == previous_month,
        )
        .group_by(Expense.category)
        .all()
    )

    current_categories = {
        category: float(amount)
        for category, amount in current_data
    }

    previous_categories = {
        category: float(amount)
        for category, amount in previous_data
    }

    categories = set(current_categories) | set(previous_categories)

    if not categories:
        return []

    results = []

    for category in sorted(categories):
        current_expense = current_categories.get(
            category, 0
        )
        previous_expense = previous_categories.get(
            category, 0
        )

        difference = (
            current_expense - previous_expense
        )

        if previous_expense > 0:
            change_percentage = (
                difference
                / previous_expense
            ) * 100
        elif current_expense > 0:
            change_percentage = 100
        else:
            change_percentage = 0

        if change_percentage <= -20:
            trend_score = 90
            trend_status = "Excellent"
            message = (
                f"{category} spending has decreased "
                "significantly."
            )

        elif change_percentage < 0:
            trend_score = 75
            trend_status = "Good"
            message = (
                f"{category} spending has decreased."
            )

        elif change_percentage == 0:
            trend_score = 60
            trend_status = "Stable"
            message = (
                f"{category} spending is stable."
            )

        elif change_percentage <= 20:
            trend_score = 45
            trend_status = "Moderate"
            message = (
                f"{category} spending has increased "
                "slightly."
            )

        else:
            trend_score = 20
            trend_status = "Risky"
            message = (
                f"{category} spending has increased "
                "significantly. Consider reducing "
                "unnecessary spending."
            )

        results.append(
            {
                "category": category,
                "current_month_expense": round(
                    current_expense, 2
                ),
                "previous_month_expense": round(
                    previous_expense, 2
                ),
                "change_percentage": round(
                    change_percentage, 2
                ),
                "trend_score": trend_score,
                "trend_status": trend_status,
                "message": message,
            }
        )

    return results
