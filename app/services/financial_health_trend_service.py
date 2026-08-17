from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.income import Income


def get_financial_health_trend(
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
                func.extract("year", Income.created_at) == year,
                func.extract("month", Income.created_at) == month,
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
                func.extract("year", Expense.created_at) == year,
                func.extract("month", Expense.created_at) == month,
            )
            .scalar()
        )

        return float(income or 0), float(expense or 0)

    current_income, current_expense = get_month_data(
        current_year,
        current_month,
    )

    previous_income, previous_expense = get_month_data(
        previous_year,
        previous_month,
    )

    def calculate_score(income, expense):
        if income <= 0:
            return 0

        ratio = (expense / income) * 100

        if ratio <= 50:
            return 100
        elif ratio <= 70:
            return 80
        elif ratio <= 90:
            return 60
        elif ratio <= 100:
            return 40
        else:
            return 20

    current_score = calculate_score(
        current_income,
        current_expense,
    )

    previous_score = calculate_score(
        previous_income,
        previous_expense,
    )

    score_change = current_score - previous_score

    if score_change > 0:
        trend = "Improving"
        message = (
            "Your financial health improved "
            "compared with the previous month."
        )

    elif score_change < 0:
        trend = "Declining"
        message = (
            "Your financial health declined "
            "compared with the previous month."
        )

    else:
        trend = "Stable"
        message = (
            "Your financial health remained stable "
            "compared with the previous month."
        )

    return {
        "current_month_score": current_score,
        "previous_month_score": previous_score,
        "score_change": score_change,
        "trend": trend,
        "message": message,
    }
