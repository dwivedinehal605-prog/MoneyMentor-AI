from collections import defaultdict

from sqlalchemy.orm import Session

from app.models.expense import Expense


def get_category_insights(
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

    if not expenses:

        return {
            "highest_spending_category": "N/A",
            "highest_spending_amount": 0,
            "lowest_spending_category": "N/A",
            "lowest_spending_amount": 0,
            "total_categories": 0,
            "category_breakdown": [],
        }

    category_totals = defaultdict(float)

    for expense in expenses:

        category_totals[
            expense.category
        ] += expense.amount

    highest_category = max(
        category_totals,
        key=category_totals.get,
    )

    lowest_category = min(
        category_totals,
        key=category_totals.get,
    )

    breakdown = [
        {
            "category": category,
            "amount": round(amount, 2),
        }
        for category, amount
        in category_totals.items()
    ]

    return {
        "highest_spending_category": highest_category,
        "highest_spending_amount": round(
            category_totals[highest_category],
            2,
        ),
        "lowest_spending_category": lowest_category,
        "lowest_spending_amount": round(
            category_totals[lowest_category],
            2,
        ),
        "total_categories": len(
            category_totals
        ),
        "category_breakdown": breakdown,
    }