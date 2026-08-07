from collections import defaultdict

from sqlalchemy.orm import Session

from app.models.expense import Expense


def get_top_categories(
    db: Session,
    user_id: int,
):
    """
    Return the user's top spending
    categories ranked by total amount.
    """

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id
        )
        .all()
    )

    if not expenses:

        return {
            "top_categories": []
        }

    category_totals = defaultdict(float)

    for expense in expenses:

        category_totals[
            expense.category
        ] += expense.amount

    sorted_categories = sorted(
        category_totals.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    top_categories = [
        {
            "category": category,
            "amount": round(
                amount,
                2,
            ),
        }
        for category, amount
        in sorted_categories[:5]
    ]

    return {
        "top_categories": top_categories
    }