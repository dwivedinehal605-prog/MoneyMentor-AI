from sqlalchemy.orm import Session

from app.models.expense import Expense


def detect_expense_anomalies(
    db: Session,
    user_id: int,
):
    """
    Detect unusually high expenses
    based on the user's average expense.
    """

    # =====================================
    # Fetch User Expenses
    # =====================================

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id
        )
        .order_by(
            Expense.created_at.asc()
        )
        .all()
    )

    # =====================================
    # No Expense Data
    # =====================================

    if not expenses:

        return {
            "anomaly_detected": False,
            "total_expenses_analyzed": 0,
            "anomalies": [],
            "message": (
                "No expense records found. "
                "Add expenses to analyze unusual spending."
            ),
        }

    # =====================================
    # Need Minimum Data
    # =====================================

    if len(expenses) < 3:

        return {
            "anomaly_detected": False,
            "total_expenses_analyzed": len(expenses),
            "anomalies": [],
            "message": (
                "Insufficient expense data. "
                "Add at least 3 expenses for anomaly detection."
            ),
        }

    # =====================================
    # Calculate Average Expense
    # =====================================

    total_amount = sum(
        float(expense.amount or 0)
        for expense in expenses
    )

    average_expense = (
        total_amount /
        len(expenses)
    )

    # =====================================
    # Detect Anomalies
    # =====================================
    #
    # An expense is considered anomalous
    # if it is more than 2x the average.
    # =====================================

    anomalies = []

    threshold = average_expense * 2

    for expense in expenses:

        amount = float(
            expense.amount or 0
        )

        if amount > threshold:

            if average_expense > 0:

                deviation_percentage = (
                    (
                        amount -
                        average_expense
                    )
                    /
                    average_expense
                ) * 100

            else:

                deviation_percentage = 0

            anomalies.append(
                {
                    "title": expense.title or "Untitled Expense",
                    "category": (
                        expense.category
                        or "Uncategorized"
                    ),
                    "amount": round(
                        amount,
                        2,
                    ),
                    "average_expense": round(
                        average_expense,
                        2,
                    ),
                    "deviation_percentage": round(
                        deviation_percentage,
                        2,
                    ),
                    "message": (
                        f"This expense of ₹{amount:.2f} "
                        f"is significantly higher than "
                        f"your average expense of "
                        f"₹{average_expense:.2f}."
                    ),
                }
            )

    # =====================================
    # Final Response
    # =====================================

    if anomalies:

        message = (
            f"{len(anomalies)} unusual expense(s) "
            "detected. Review these transactions "
            "to maintain better spending control."
        )

    else:

        message = (
            "No unusual expenses detected. "
            "Your spending appears to be within "
            "your normal expense range."
        )

    return {
        "anomaly_detected": bool(
            anomalies
        ),
        "total_expenses_analyzed": len(
            expenses
        ),
        "anomalies": anomalies,
        "message": message,
    }