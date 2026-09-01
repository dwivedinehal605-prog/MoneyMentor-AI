import math
from datetime import date
from datetime import timedelta

from sqlalchemy.orm import Session

from app.models.savings_goal import SavingsGoal
from app.models.income import Income
from app.models.expense import Expense


def get_goal_forecast(
    db: Session,
    user_id: int,
):
    goals = (
        db.query(SavingsGoal)
        .filter(SavingsGoal.user_id == user_id)
        .all()
    )

    total_income = (
        db.query(Income)
        .filter(Income.user_id == user_id)
        .all()
    )

    total_expense = (
        db.query(Expense)
        .filter(Expense.user_id == user_id)
        .all()
    )

    income_amount = sum(
        income.amount
        for income in total_income
    )

    expense_amount = sum(
        expense.amount
        for expense in total_expense
    )

    monthly_saving_capacity = max(
        income_amount - expense_amount,
        0,
    )

    result = []

    for goal in goals:

        remaining_amount = (
            goal.target_amount
            - goal.saved_amount
        )

        if monthly_saving_capacity <= 0:

            estimated_months = None
            completion_date = None

        else:

            estimated_months = math.ceil(
                remaining_amount
                / monthly_saving_capacity
            )

            completion_date = (
                date.today()
        +       timedelta(
                     days=estimated_months * 30
                )
            )
        result.append(
            {
                "goal": goal.title,
                "target_amount": goal.target_amount,
                "saved_amount": goal.saved_amount,
                "remaining_amount": remaining_amount,
                "monthly_saving_capacity": monthly_saving_capacity,
                "estimated_months_to_complete": estimated_months,
                "expected_completion_date": completion_date,
            }
        )

    return {
        "forecasts": result
    }