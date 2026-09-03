from collections import defaultdict
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.budget import Budget
from app.models.savings_goal import SavingsGoal


def get_notifications(
    db: Session,
    user_id: int,
):
    notifications = []

    current_month = datetime.now().month
    current_year = datetime.now().year

    # =====================================
    # Fetch Expenses
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

    total_expense = sum(
        expense.amount
        for expense in expenses
    )

    # =====================================
    # Current Month Expense
    # =====================================

    current_month_expense = sum(
        expense.amount
        for expense in expenses
        if (
            expense.created_at.month
            == current_month
            and expense.created_at.year
            == current_year
        )
    )

    # =====================================
    # Budget Monitoring
    # =====================================

    budget = (
        db.query(Budget)
        .filter(
            Budget.user_id == user_id,
            Budget.month == current_month,
            Budget.year == current_year,
        )
        .first()
    )

    if budget:

        budget_amount = float(
            budget.budget_amount
        )

        if budget_amount > 0:

            usage_percentage = (
                current_month_expense
                / budget_amount
            ) * 100

            if usage_percentage > 100:

                notifications.append(
                    {
                        "priority": "high",
                        "type": "Budget Alert",
                        "message": (
                            f"You have exceeded your monthly budget "
                            f"by {usage_percentage - 100:.2f}%."
                        ),
                    }
                )

            elif usage_percentage >= 80:

                notifications.append(
                    {
                        "priority": "medium",
                        "type": "Budget Warning",
                        "message": (
                            f"You have already used "
                            f"{usage_percentage:.2f}% "
                            f"of your monthly budget."
                        ),
                    }
                )

    # =====================================
    # Large Transaction Alert
    # =====================================

    if expenses and total_expense > 0:

        largest_expense = max(
            expenses,
            key=lambda x: x.amount,
        )

        if (
            largest_expense.amount
            >= total_expense * 0.30
        ):

            notifications.append(
                {
                    "priority": "high",
                    "type": "Large Transaction",
                    "message": (
                        f"Large expense detected: "
                        f"₹{largest_expense.amount:,.2f} "
                        f"for '{largest_expense.title}'."
                    ),
                }
            )

    # =====================================
    # Monthly Spending Trend
    # =====================================

    monthly_totals = defaultdict(float)

    for expense in expenses:

        month_key = (
            expense.created_at.strftime(
                "%Y-%m"
            )
        )

        monthly_totals[
            month_key
        ] += expense.amount

    months = sorted(
        monthly_totals.keys()
    )

    if len(months) >= 2:

        previous_month_total = (
            monthly_totals[
                months[-2]
            ]
        )

        current_month_total = (
            monthly_totals[
                months[-1]
            ]
        )

        increase_amount = (
            current_month_total
            - previous_month_total
        )

        if (
            previous_month_total > 0
            and increase_amount > 0
        ):

            growth_percentage = (
                increase_amount
                / previous_month_total
            ) * 100

            if growth_percentage > 20:

                notifications.append(
                    {
                        "priority": "medium",
                        "type": "Spending Trend",
                        "message": (
                            f"Monthly spending increased by "
                            f"₹{increase_amount:,.2f} "
                            f"compared to last month."
                        ),
                    }
                )

    # =====================================
    # Savings Goal Progress
    # =====================================

    goals = (
        db.query(SavingsGoal)
        .filter(
            SavingsGoal.user_id
            == user_id
        )
        .all()
    )

    for goal in goals:

        if goal.target_amount <= 0:
            continue

        progress = (
            goal.saved_amount
            / goal.target_amount
        ) * 100

        if progress >= 100:

            notifications.append(
                {
                    "priority": "high",
                    "type": "Goal Completed",
                    "message": (
                        f"Congratulations! "
                        f"'{goal.title}' "
                        f"has been achieved."
                    ),
                }
            )

        elif progress >= 80:

            notifications.append(
                {
                    "priority": "medium",
                    "type": "Goal Progress",
                    "message": (
                        f"'{goal.title}' is "
                        f"{progress:.2f}% complete."
                    ),
                }
            )

        elif progress > 0:

            notifications.append(
                {
                    "priority": "low",
                    "type": "Goal Progress",
                    "message": (
                        f"'{goal.title}' is "
                        f"{progress:.2f}% complete."
                    ),
                }
            )

    # =====================================
    # Default Notification
    # =====================================

    if not notifications:

        notifications.append(
            {
                "priority": "low",
                "type": "Financial Update",
                "message": (
                    "Everything looks good. "
                    "Your finances are stable."
                ),
            }
        )

    # =====================================
    # Sort Notifications
    # =====================================

    priority_order = {
        "high": 1,
        "medium": 2,
        "low": 3,
    }

    notifications = sorted(
        notifications,
        key=lambda item:
        priority_order[
            item["priority"]
        ],
    )

    # =====================================
    # Final Response
    # =====================================

    return {
        "total_notifications": len(
            notifications
        ),
        "notifications": notifications,
    }