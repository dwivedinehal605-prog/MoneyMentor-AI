from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.income import Income
from app.models.expense import Expense


def get_savings_income_ratio(
    db: Session,
    user_id: int,
):
    total_income = (
        db.query(
            func.coalesce(
                func.sum(Income.amount),
                0,
            )
        )
        .filter(
            Income.user_id == user_id
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
            Expense.user_id == user_id
        )
        .scalar()
    )

    total_income = float(total_income)
    total_expense = float(total_expense)

    savings_amount = (
        total_income - total_expense
    )

    if total_income > 0:
        savings_income_ratio = (
            savings_amount / total_income
        ) * 100
    else:
        savings_income_ratio = 0

    if total_income <= 0:
        savings_score = 0
        savings_status = "Critical"
        message = (
            "No income data is available. "
            "Add income to evaluate your savings."
        )

    elif savings_income_ratio >= 30:
        savings_score = 90
        savings_status = "Excellent"
        message = (
            "You are saving a healthy portion "
            "of your income."
        )

    elif savings_income_ratio >= 20:
        savings_score = 75
        savings_status = "Good"
        message = (
            "Your savings level is good. "
            "Continue maintaining disciplined spending."
        )

    elif savings_income_ratio >= 10:
        savings_score = 50
        savings_status = "Moderate"
        message = (
            "You are saving some of your income, "
            "but there is room for improvement."
        )

    elif savings_income_ratio >= 0:
        savings_score = 30
        savings_status = "Poor"
        message = (
            "Your savings are very low. "
            "Consider reducing unnecessary expenses."
        )

    else:
        savings_score = 10
        savings_status = "Critical"
        message = (
            "You are not saving money because "
            "your expenses exceed your income."
        )

    return {
        "total_income": round(
            total_income,
            2,
        ),
        "total_expense": round(
            total_expense,
            2,
        ),
        "savings_amount": round(
            savings_amount,
            2,
        ),
        "savings_income_ratio": round(
            savings_income_ratio,
            2,
        ),
        "savings_score": savings_score,
        "savings_status": savings_status,
        "message": message,
    }
