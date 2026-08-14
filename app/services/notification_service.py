from collections import defaultdict

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.budget import Budget
from app.models.savings_goal import SavingsGoal


def get_notifications(
    db: Session,
    user_id: int,
):
    notifications = []

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
    # Latest Budget
    # =====================================

    budget = (
        db.query(Budget)
        .filter(
            Budget.user_id == user_id
        )
        .order_by(
            Budget.id.desc()
        )
        .first()
    )

    # =====================================
    # Budget Notifications
    # =====================================

    if budget:

        budget_amount = float(
            budget.budget_amount or 0
        )

        if budget_amount > 0:

            if total_expense > budget_amount:

                notifications.append(
                    {
                        "type": "Budget Alert",
                        "message": (
                            "You have exceeded your "
                            "monthly budget."
                        ),
                    }
                )

            elif total_expense >= (
                budget_amount * 0.8
            ):

                notifications.append(
                    {
                        "type": "Budget Warning",
                        "message": (
                            "You have used more than "
                            "80% of your monthly budget."
                        ),
                    }
                )

    # =====================================
    # Expense Records
    # =====================================

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id
        )
        .order_by(
            Expense.created_at.desc()
        )
        .all()
    )

    # =====================================
    # High Expense Notification
    # =====================================

    if expenses:

        highest_expense = max(
            expenses,
            key=lambda expense: expense.amount,
        )

        # High expense threshold:
        # 50% of total recorded expenses
        if (
            total_expense > 0
            and highest_expense.amount
            >= total_expense * 0.5
        ):

            notifications.append(
                {
                    "type": "High Expense Alert",
                    "message": (
                        f"Your largest expense was "
                        f"₹{highest_expense.amount:.2f} "
                        f"for '{highest_expense.title}'. "
                        "Review this expense to maintain "
                        "better spending control."
                    ),
                }
            )

    # =====================================
    # Monthly Spending Trend
    # =====================================

    monthly_totals = defaultdict(float)

    for expense in expenses:

        month = expense.created_at.strftime(
            "%Y-%m"
        )

        monthly_totals[month] += expense.amount

    months = sorted(
        monthly_totals.keys()
    )

    if len(months) >= 2:

        previous_month = monthly_totals[
            months[-2]
        ]

        current_month = monthly_totals[
            months[-1]
        ]

        if previous_month > 0:

            change_percentage = (
                (
                    current_month
                    - previous_month
                )
                / previous_month
            ) * 100

            # Alert when spending increases
            # by more than 20%

            if change_percentage > 20:

                notifications.append(
                    {
                        "type": "Spending Alert",
                        "message": (
                            f"Your spending increased by "
                            f"{change_percentage:.2f}% compared "
                            "with the previous month. "
                            "Consider reviewing your recent "
                            "expenses."
                        ),
                    }
                )

    # =====================================
    # Latest Savings Goal
    # =====================================

    goal = (
        db.query(SavingsGoal)
        .filter(
            SavingsGoal.user_id == user_id
        )
        .order_by(
            SavingsGoal.id.desc()
        )
        .first()
    )

    # =====================================
    # Savings Goal Notifications
    # =====================================

    if goal:

        target_amount = float(
            goal.target_amount or 0
        )

        saved_amount = float(
            goal.saved_amount or 0
        )

        progress = 0

        if target_amount > 0:

            progress = (
                saved_amount
                / target_amount
            ) * 100

        if progress >= 100:

            notifications.append(
                {
                    "type": "Goal Completed",
                    "message": (
                        f"Congratulations! You have "
                        f"achieved your savings goal "
                        f"'{goal.title}'."
                    ),
                }
            )

        elif progress >= 80:

            notifications.append(
                {
                    "type": "Goal Progress",
                    "message": (
                        f"You have completed "
                        f"{progress:.2f}% of your "
                        f"savings goal '{goal.title}'."
                    ),
                }
            )

        elif progress > 0:

            notifications.append(
                {
                    "type": "Goal Progress",
                    "message": (
                        f"You have saved "
                        f"{progress:.2f}% of your "
                        f"savings goal '{goal.title}'."
                    ),
                }
            )

    # =====================================
    # No Notifications
    # =====================================

    if not notifications:

        notifications.append(
            {
                "type": "Financial Update",
                "message": (
                    "Your finances are currently "
                    "on track. Keep monitoring your "
                    "spending and savings."
                ),
            }
        )

    # =====================================
    # Final Response
    # =====================================

    return {
        "notifications": notifications
    }