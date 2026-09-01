from sqlalchemy.orm import Session

from app.models.recurring_transaction import (
    RecurringTransaction,
)

from app.schemas.recurring_transaction import (
    RecurringTransactionCreate,
)


def create_recurring_transaction(
    db: Session,
    user_id: int,
    data: RecurringTransactionCreate,
):
    transaction = RecurringTransaction(
    user_id=user_id,
    title=data.title,
    amount=data.amount,
    category=data.category,
    transaction_type=data.transaction_type,
    frequency=data.frequency,
    next_due_date=data.next_due_date,
)

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction


def get_recurring_transactions(
    db: Session,
    user_id: int,
):
    return (
        db.query(RecurringTransaction)
        .filter(
            RecurringTransaction.user_id == user_id
        )
        .order_by(
            RecurringTransaction.id.desc()
        )
        .all()
    )


def delete_recurring_transaction(
    db: Session,
    transaction_id: int,
    user_id: int,
):
    transaction = (
        db.query(RecurringTransaction)
        .filter(
            RecurringTransaction.id == transaction_id,
            RecurringTransaction.user_id == user_id,
        )
        .first()
    )

    if not transaction:
        return None

    db.delete(transaction)
    db.commit()

    return {
        "message": "Recurring transaction deleted successfully."
    }