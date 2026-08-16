from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.income import Income


def get_savings_rate_trend(
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

    current_income = (
        db.query(
            func.coalesce(
                func.sum(Income.amount),
                0,
            )
        )
        .filter(
            Income.user_id == user_id,
            func.extract(
                "year",
                Income.created_at,
            ) == current_year,
            func.extract(
                "month",
                Income.created_at,
            ) == current_month,
        )
        .scalar()
    )

    current_expense = (
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

    previous_income = (
        db.query(
            func.coalesce(
                func.sum(Income.amount),
                0,
            )
        )
        .filter(
            Income.user_id == user_id,
            func.extract(
                "year",
                Income.created_at,
            ) == previous_year,
            func.extract(
                "month",
                Income.created_at,
            ) == previous_month,
        )
        .scalar()
    )

    previous_expense = (
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

    current_income = float(current_income or 0)
    current_expense = float(current_expense or 0)
    previous_income = float(previous_income or 0)
    previous_expense = float(previous_expense or 0)

    if current_income > 0:
        current_savings_rate = (
            (current_income - current_expense)
            / current_income
        ) * 100
    else:
        current_savings_rate = 0

    if previous_income > 0:
        previous_savings_rate = (
            (previous_income - previous_expense)
            / previous_income
        ) * 100
    else:
        previous_savings_rate = 0

    difference = (
        current_savings_rate -
        previous_savings_rate
    )

    if previous_savings_rate != 0:
        change_percentage = (
            difference /
            abs(previous_savings_rate)
        ) * 100
    else:
        change_percentage = 0

    if difference > 0:
        trend = "Improving"
        message = (
            "Your savings rate improved compared "
            "with the previous month."
        )

    elif difference < 0:
        trend = "Declining"
        message = (
            "Your savings rate declined compared "
            "with the previous month."
        )

    else:
        trend = "Stable"
        message = (
            "Your savings rate remained stable "
            "compared with the previous month."
        )

    return {
        "current_month_savings_rate": round(
            current_savings_rate,
            2,
        ),
        "previous_month_savings_rate": round(
            previous_savings_rate,
            2,
        ),
        "change_percentage": round(
            change_percentage,
            2,
        ),
        "trend": trend,
        "message": message,
    }