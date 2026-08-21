from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.income import Income
from app.models.expense import Expense


def get_savings_coverage(
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

    if total_expense > 0:
        coverage_ratio = (
            savings_amount / total_expense
        ) * 100
    else:
        coverage_ratio = 0

    if total_expense <= 0:
        coverage_score = 90
        coverage_status = "Excellent"
        message = (
            "No expenses are recorded. "
            "Your savings currently cover all recorded spending."
        )

    elif coverage_ratio >= 50:
        coverage_score = 90
        coverage_status = "Excellent"
        message = (
            "Your savings provide strong coverage "
            "relative to your expenses."
        )

    elif coverage_ratio >= 25:
        coverage_score = 75
        coverage_status = "Good"
        message = (
            "Your savings provide good coverage "
            "relative to your expenses."
        )

    elif coverage_ratio >= 10:
        coverage_score = 50
        coverage_status = "Moderate"
        message = (
            "Your savings provide limited coverage "
            "relative to your expenses."
        )

    elif coverage_ratio >= 0:
        coverage_score = 30
        coverage_status = "Poor"
        message = (
            "Your savings provide very little coverage "
            "relative to your expenses."
        )

    else:
        coverage_score = 10
        coverage_status = "Critical"
        message = (
            "Your savings are negative because "
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
        "coverage_ratio": round(
            coverage_ratio,
            2,
        ),
        "coverage_score": coverage_score,
        "coverage_status": coverage_status,
        "message": message,
    }
