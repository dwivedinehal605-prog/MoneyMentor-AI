from datetime import date

from sqlalchemy.orm import Session

from app.models.recurring_transaction import (
    RecurringTransaction,
)


def get_payment_reminders(
    db: Session,
    user_id: int,
):
    reminders = []

    transactions = (
        db.query(RecurringTransaction)
        .filter(
            RecurringTransaction.user_id == user_id,
            RecurringTransaction.is_active == True,
        )
        .order_by(
            RecurringTransaction.next_due_date.asc()
        )
        .all()
    )

    today = date.today()

    for transaction in transactions:

        due_date = transaction.next_due_date

        if hasattr(due_date, "date"):
            due_date = due_date.date()

        days_remaining = (
            due_date - today
        ).days

        # ==========================
        # Status
        # ==========================

        if days_remaining < 0:

            status = "Overdue"

            message = (
                f"Your {transaction.title} payment "
                f"of ₹{transaction.amount:.2f} is overdue. "
                "Please complete the payment as soon as possible."
            )

        elif days_remaining == 0:

            status = "Due Today"

            message = (
                f"Your {transaction.title} payment "
                f"of ₹{transaction.amount:.2f} is due today."
            )

        elif days_remaining <= 7:

            status = "Due Soon"

            message = (
                f"Your {transaction.title} payment "
                f"of ₹{transaction.amount:.2f} is due in "
                f"{days_remaining} days."
            )

        else:

            status = "Upcoming"

            message = (
                f"Upcoming payment: {transaction.title} "
                f"(₹{transaction.amount:.2f}) is due in "
                f"{days_remaining} days."
            )

        reminders.append(
            {
                "title": transaction.title,
                "amount": transaction.amount,
                "category": transaction.category,
                "due_date": due_date,
                "days_remaining": days_remaining,
                "status": status,
                "message": message,
            }
        )

    return {
        "reminders": reminders
    }