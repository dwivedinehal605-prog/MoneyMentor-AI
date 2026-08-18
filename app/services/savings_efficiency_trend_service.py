from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.income import Income


def get_savings_efficiency_trend(
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

    def get_month_data(year, month):
        income = (
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
                ) == year,
                func.extract(
                    "month",
                    Income.created_at,
                ) == month,
            )
            .scalar()
        )

        expense = (
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
                ) == year,
                func.extract(
                    "month",
                    Expense.created_at,
                ) == month,
            )
            .scalar()
        )

        return (
            float(income or 0),
            float(expense or 0),
        )

    current_income, current_expense = get_month_data(
        current_year,
        current_month,
    )

    previous_income, previous_expense = get_month_data(
        previous_year,
        previous_month,
    )

    def calculate_savings_rate(
        income,
        expense,
    ):
        if income <= 0:
            return 0

        return (
            (income - expense)
            / income
        ) * 100

    current_rate = calculate_savings_rate(
        current_income,
        current_expense,
    )

    previous_rate = calculate_savings_rate(
        previous_income,
        previous_expense,
    )

    rate_change = (
        current_rate -
        previous_rate
    )

    if rate_change > 0:
        trend = "Improving"
        message = (
            "Your savings efficiency improved "
            "compared with the previous month."
        )

    elif rate_change < 0:
        trend = "Declining"
        message = (
            "Your savings efficiency declined "
            "compared with the previous month."
        )

    else:
        trend = "Stable"
        message = (
            "Your savings efficiency remained stable "
            "compared with the previous month."
        )

    return {
        "current_month_savings_rate": round(
            current_rate,
            2,
        ),
        "previous_month_savings_rate": round(
            previous_rate,
            2,
        ),
        "rate_change": round(
            rate_change,
            2,
        ),
        "trend": trend,
        "message": message,
    }
