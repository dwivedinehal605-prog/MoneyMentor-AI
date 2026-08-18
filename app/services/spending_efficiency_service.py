from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.income import Income


def get_spending_efficiency(
    db: Session,
    user_id: int,
):
    now = datetime.now()

    year = now.year
    month = now.month

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

    income = float(income or 0)
    expense = float(expense or 0)

    if income > 0:
        expense_income_ratio = (
            expense / income
        ) * 100
    else:
        expense_income_ratio = 0

    if income <= 0:
        efficiency_score = 0
        efficiency_status = "No Income"
        message = (
            "No income was recorded for this month. "
            "Add income to evaluate spending efficiency."
        )

    elif expense_income_ratio <= 50:
        efficiency_score = 100
        efficiency_status = "Excellent"
        message = (
            "Your spending is highly efficient "
            "relative to your income."
        )

    elif expense_income_ratio <= 70:
        efficiency_score = 80
        efficiency_status = "Good"
        message = (
            "Your spending efficiency is good. "
            "You are maintaining reasonable expense levels."
        )

    elif expense_income_ratio <= 90:
        efficiency_score = 60
        efficiency_status = "Moderate"
        message = (
            "Your spending efficiency is moderate. "
            "Consider reducing unnecessary expenses."
        )

    elif expense_income_ratio <= 100:
        efficiency_score = 40
        efficiency_status = "Low"
        message = (
            "Your spending is close to your income. "
            "Try to increase your savings margin."
        )

    else:
        efficiency_score = 20
        efficiency_status = "Critical"
        message = (
            "Your expenses exceed your income. "
            "Immediate spending control is recommended."
        )

    return {
        "current_month_income": round(
            income,
            2,
        ),
        "current_month_expense": round(
            expense,
            2,
        ),
        "expense_income_ratio": round(
            expense_income_ratio,
            2,
        ),
        "efficiency_score": efficiency_score,
        "efficiency_status": efficiency_status,
        "message": message,
    }
