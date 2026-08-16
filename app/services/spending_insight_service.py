
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense


def get_spending_insight(
    db: Session,
    user_id: int,
):
    """
    Identify the user's highest spending category
    and generate a spending insight.
    """

    # =====================================
    # Total Expense
    # =====================================

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

    total_expense = float(
        total_expense or 0
    )

    # =====================================
    # Category Totals
    # =====================================

    category_data = (
        db.query(
            Expense.category,
            func.sum(
                Expense.amount
            ).label("total"),
        )
        .filter(
            Expense.user_id == user_id
        )
        .group_by(
            Expense.category
        )
        .order_by(
            func.sum(
                Expense.amount
            ).desc()
        )
        .all()
    )

    # =====================================
    # No Expense Data
    # =====================================

    if not category_data:

        return {
            "highest_category": "None",
            "highest_category_amount": 0.0,
            "total_expense": 0.0,
            "percentage_of_total": 0.0,
            "insight": (
                "No expense records found. "
                "Add expenses to receive spending insights."
            ),
        }

    # =====================================
    # Highest Spending Category
    # =====================================

    highest_category = (
        category_data[0].category
        or "Uncategorized"
    )

    highest_category_amount = float(
        category_data[0].total or 0
    )

    # =====================================
    # Percentage Calculation
    # =====================================

    percentage_of_total = 0.0

    if total_expense > 0:

        percentage_of_total = (
            highest_category_amount
            / total_expense
        ) * 100

    percentage_of_total = round(
        percentage_of_total,
        2,
    )

    highest_category_amount = round(
        highest_category_amount,
        2,
    )

    total_expense = round(
        total_expense,
        2,
    )

    # =====================================
    # Generate Insight
    # =====================================

    if percentage_of_total >= 50:

        insight = (
            f"{highest_category} represents "
            f"{percentage_of_total:.2f}% of your "
            "total expenses. Consider reviewing "
            "this category to improve spending control."
        )

    elif percentage_of_total >= 30:

        insight = (
            f"{highest_category} is your highest "
            f"spending category at "
            f"{percentage_of_total:.2f}% of total expenses. "
            "Monitor this category carefully."
        )

    else:

        insight = (
            f"{highest_category} is your highest "
            f"spending category, accounting for "
            f"{percentage_of_total:.2f}% of your "
            "total expenses."
        )

    # =====================================
    # Final Response
    # =====================================

    return {
        "highest_category": highest_category,
        "highest_category_amount": highest_category_amount,
        "total_expense": total_expense,
        "percentage_of_total": percentage_of_total,
        "insight": insight,
    }