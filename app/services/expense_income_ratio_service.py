from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.income import Income
from app.models.expense import Expense


def get_expense_income_ratio(
    db: Session,
    user_id: int,
):
    now = datetime.now()

    current_year = now.year
    current_month = now.month

    total_income = (
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

    total_expense = (
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

    total_income = float(total_income or 0)
    total_expense = float(total_expense or 0)

    if total_income > 0:
        ratio = (
            total_expense / total_income
        ) * 100
    else:
        ratio = 0

    if total_income == 0:
        financial_status = "No Income Data"
        message = (
            "No income recorded for the current month. "
            "Add income to analyze your expense-to-income ratio."
        )

    elif ratio <= 50:
        financial_status = "Healthy"
        message = (
            "Your expenses are within a healthy range "
            "compared with your income."
        )

    elif ratio <= 80:
        financial_status = "Moderate"
        message = (
            "Your expenses are moderately high compared "
            "with your income. Consider controlling spending."
        )

    else:
        financial_status = "High"
        message = (
            "Your expenses are high compared with your income. "
            "Consider reducing unnecessary spending."
        )

    return {
        "current_month_income": round(
            total_income,
            2,
        ),
        "current_month_expense": round(
            total_expense,
            2,
        ),
        "expense_income_ratio": round(
            ratio,
            2,
        ),
        "financial_status": financial_status,
        "message": message,
    }
