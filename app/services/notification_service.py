from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.expense import Expense
from app.models.budget import Budget
from app.models.savings_goal import SavingsGoal


def get_notifications(
    db: Session,
    user_id: int,
):
    notifications = []

    # Total Expense
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

    # Latest Budget
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

    # Budget Notifications
    if budget:

        if total_expense > budget.budget_amount:

            notifications.append(
                {
                    "type": "Budget Alert",
                    "message": "You have exceeded your budget."
                }
            )

        elif total_expense >= (
            budget.budget_amount * 0.8
        ):

            notifications.append(
                {
                    "type": "Warning",
                    "message": "You have used more than 80% of your budget."
                }
            )

    # Latest Savings Goal
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

    # Savings Goal Notifications
    if goal:

        progress = 0

        if goal.target_amount > 0:

            progress = (
                goal.saved_amount /
                goal.target_amount
            ) * 100

        if progress >= 100:

            notifications.append(
                {
                    "type": "Goal Completed",
                    "message": "Congratulations! Savings goal achieved."
                }
            )

        elif progress >= 80:

            notifications.append(
                {
                    "type": "Goal Progress",
                    "message": "You have completed over 80% of your savings goal."
                }
            )

    return {
        "notifications": notifications
    }