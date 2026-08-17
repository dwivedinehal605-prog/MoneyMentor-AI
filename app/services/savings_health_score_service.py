from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.income import Income


def get_savings_health_score(
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

    savings = income - expense

    if income > 0:
        savings_rate = (savings / income) * 100
    else:
        savings_rate = 0

    if savings_rate >= 30:
        health_score = 100
        financial_status = "Excellent"
        message = (
            "Your savings rate is excellent. "
            "You are maintaining strong financial discipline."
        )

    elif savings_rate >= 20:
        health_score = 80
        financial_status = "Good"
        message = (
            "Your savings rate is good. "
            "Keep maintaining your current savings habits."
        )

    elif savings_rate >= 10:
        health_score = 60
        financial_status = "Moderate"
        message = (
            "Your savings rate is moderate. "
            "Consider increasing your monthly savings."
        )

    elif savings_rate > 0:
        health_score = 40
        financial_status = "Low"
        message = (
            "Your savings rate is low. "
            "Try reducing unnecessary expenses."
        )

    else:
        health_score = 20
        financial_status = "Critical"
        message = (
            "You are not saving money this month. "
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
        "savings_amount": round(
            savings,
            2,
        ),
        "savings_rate": round(
            savings_rate,
            2,
        ),
        "health_score": health_score,
        "financial_status": financial_status,
        "message": message,
    }
