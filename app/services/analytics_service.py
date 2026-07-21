from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.expense import Expense


def get_total_expense(db: Session):
    total = db.query(func.sum(Expense.amount)).scalar()

    return {
        "total_expense": total or 0
    }


def category_summary(db: Session):
    data = (
        db.query(
            Expense.category,
            func.sum(Expense.amount).label("total")
        )
        .group_by(Expense.category)
        .all()
    )

    return [
        {
            "category": row.category,
            "amount": row.total
        }
        for row in data
    ]