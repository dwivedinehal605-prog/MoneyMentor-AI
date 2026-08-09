from collections import defaultdict

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.income import Income


def get_category_expense_chart(
    db: Session,
    user_id: int,
):
    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id
        )
        .all()
    )

    category_totals = defaultdict(float)

    for expense in expenses:

        category_totals[
            expense.category
        ] += expense.amount

    return {
        "data": [
            {
                "label": category,
                "value": round(amount, 2),
            }
            for category, amount
            in category_totals.items()
        ]
    }


def get_monthly_expense_chart(
    db: Session,
    user_id: int,
):
    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id
        )
        .all()
    )

    monthly_totals = defaultdict(float)

    for expense in expenses:

        month = expense.created_at.strftime(
            "%Y-%m"
        )

        monthly_totals[
            month
        ] += expense.amount

    return {
        "data": [
            {
                "label": month,
                "value": round(amount, 2),
            }
            for month, amount
            in sorted(
                monthly_totals.items()
            )
        ]
    }


def get_income_vs_expense_chart(
    db: Session,
    user_id: int,
):
    total_income = (
        db.query(
            func.coalesce(
                func.sum(
                    Income.amount
                ),
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
                func.sum(
                    Expense.amount
                ),
                0,
            )
        )
        .filter(
            Expense.user_id == user_id
        )
        .scalar()
    )

    return {
        "data": [
            {
                "label": "Income",
                "value": round(
                    total_income,
                    2,
                ),
            },
            {
                "label": "Expense",
                "value": round(
                    total_expense,
                    2,
                ),
            },
        ]
    }

def get_spending_percentage_chart(
    db: Session,
    user_id: int,
):
    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id
        )
        .all()
    )

    category_totals = defaultdict(float)

    total_expense = 0

    for expense in expenses:

        category_totals[
            expense.category
        ] += expense.amount

        total_expense += (
            expense.amount
        )

    if total_expense == 0:

        return {
            "data": []
        }

    return {
        "data": [
            {
                "label": category,
                "value": round(
                    (
                        amount
                        / total_expense
                    )
                    * 100,
                    2,
                ),
            }
            for category, amount
            in category_totals.items()
        ]
    }