from collections import defaultdict

from sqlalchemy.orm import Session

from app.models.expense import Expense


def get_expense_category_report(
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

    category_totals = (
        defaultdict(float)
    )

    for expense in expenses:

        category_totals[
            expense.category
        ] += expense.amount

    categories = [

        {
            "category": category,
            "amount": round(
                amount,
                2,
            ),
        }

        for category, amount
        in sorted(
            category_totals.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    ]

    return {
        "total_categories": len(
            category_totals
        ),
        "categories": categories,
    }