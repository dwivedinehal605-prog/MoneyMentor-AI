from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.income import Income


def get_expense_health_score(
    db: Session,
    user_id: int,
):
    now = datetime.now()

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
            ) == now.year,
            func.extract(
                "month",
                Income.created_at,
            ) == now.month,
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
            ) == now.year,
            func.extract(
                "month",
                Expense.created_at,
            ) == now.month,
        )
        .scalar()
    )

    current_income = float(current_income or 0)
    current_expense = float(current_expense or 0)

    if current_income > 0:
        expense_income_ratio = (
            current_expense / current_income
        ) * 100
    else:
        expense_income_ratio = 0

    # Calculate financial health score
    if current_income <= 0:
        health_score = 0
        financial_status = "No Income Data"
        message = (
            "No income recorded for the current month. "
            "Add income to evaluate your financial health."
        )

    elif expense_income_ratio <= 50:
        health_score = 100
        financial_status = "Excellent"
        message = (
            "Your expenses are well controlled "
            "compared with your income."
        )

    elif expense_income_ratio <= 70:
        health_score = 80
        financial_status = "Good"
        message = (
            "Your spending is within a healthy range."
        )

    elif expense_income_ratio <= 90:
        health_score = 60
        financial_status = "Moderate"
        message = (
            "Your expenses are getting close to "
            "your income. Consider reducing spending."
        )

    elif expense_income_ratio <= 100:
        health_score = 40
        financial_status = "Needs Improvement"
        message = (
            "Your expenses are consuming most of "
            "your income. Review your spending."
        )

    else:
        health_score = 20
        financial_status = "Critical"
        message = (
            "Your expenses exceed your income. "
            "Immediate spending control is recommended."
        )

    return {
        "current_month_income": round(
            current_income,
            2,
        ),
        "current_month_expense": round(
            current_expense,
            2,
        ),
        "expense_income_ratio": round(
            expense_income_ratio,
            2,
        ),
        "health_score": health_score,
        "financial_status": financial_status,
        "message": message,
    }