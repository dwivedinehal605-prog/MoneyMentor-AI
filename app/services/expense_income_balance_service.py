from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.income import Income
from app.models.expense import Expense


def get_expense_income_balance(
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

    balance_amount = (
        total_income - total_expense
    )

    if total_income > 0:
        balance_ratio = (
            balance_amount / total_income
        ) * 100
    else:
        balance_ratio = 0

    if total_income <= 0:
        balance_score = 0
        balance_status = "Critical"
        message = (
            "No income data is available. "
            "Add income to evaluate your financial balance."
        )

    elif balance_ratio >= 50:
        balance_score = 90
        balance_status = "Excellent"
        message = (
            "Your income significantly exceeds "
            "your expenses. Your financial balance is strong."
        )

    elif balance_ratio >= 30:
        balance_score = 75
        balance_status = "Good"
        message = (
            "Your income is comfortably higher "
            "than your expenses."
        )

    elif balance_ratio >= 10:
        balance_score = 50
        balance_status = "Moderate"
        message = (
            "Your income is only moderately higher "
            "than your expenses. Consider increasing savings."
        )

    elif balance_ratio >= 0:
        balance_score = 30
        balance_status = "Poor"
        message = (
            "Your expenses are close to your income. "
            "Reducing unnecessary spending is recommended."
        )

    else:
        balance_score = 10
        balance_status = "Critical"
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
        "balance_amount": round(
            balance_amount,
            2,
        ),
        "balance_ratio": round(
            balance_ratio,
            2,
        ),
        "balance_score": balance_score,
        "balance_status": balance_status,
        "message": message,
    }
