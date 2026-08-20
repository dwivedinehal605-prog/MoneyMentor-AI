from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.income import Income
from app.models.expense import Expense


def get_overall_spending_efficiency(
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

    if total_income > 0:
        expense_income_ratio = (
            total_expense / total_income
        ) * 100
    else:
        expense_income_ratio = 0

    if total_income <= 0:
        efficiency_score = 0
        efficiency_status = "Critical"
        message = (
            "No income data is available. "
            "Add income to evaluate spending efficiency."
        )

    elif expense_income_ratio <= 50:
        efficiency_score = 90
        efficiency_status = "Excellent"
        message = (
            "Your spending is well controlled "
            "compared with your income."
        )

    elif expense_income_ratio <= 70:
        efficiency_score = 75
        efficiency_status = "Good"
        message = (
            "Your spending efficiency is good, "
            "but there is room for improvement."
        )

    elif expense_income_ratio <= 90:
        efficiency_score = 50
        efficiency_status = "Moderate"
        message = (
            "Your expenses are taking a significant "
            "portion of your income."
        )

    elif expense_income_ratio <= 100:
        efficiency_score = 30
        efficiency_status = "Poor"
        message = (
            "Your expenses are very close to your income. "
            "Consider reducing unnecessary spending."
        )

    else:
        efficiency_score = 10
        efficiency_status = "Critical"
        message = (
            "Your expenses exceed your income. "
            "Immediate spending control is recommended."
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
        "expense_income_ratio": round(
            expense_income_ratio,
            2,
        ),
        "efficiency_score": efficiency_score,
        "efficiency_status": efficiency_status,
        "message": message,
    }
