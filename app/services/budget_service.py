from datetime import datetime
import calendar
from fastapi import HTTPException, status
from sqlalchemy import extract
from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.models.expense import Expense

from app.schemas.budget import (
    BudgetCreate,
    BudgetUpdate,
)


def create_budget(
    db: Session,
    budget: BudgetCreate,
    user_id: int,
):
    existing_budget = (
        db.query(Budget)
        .filter(
            Budget.user_id == user_id,
            Budget.month == budget.month,
            Budget.year == budget.year,
        )
        .first()
    )

    if existing_budget:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Budget already exists for this month.",
        )

    db_budget = Budget(
        user_id=user_id,
        month=budget.month,
        year=budget.year,
        budget_amount=budget.budget_amount,
    )

    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)

    return db_budget


def get_current_budget(
    db: Session,
    user_id: int,
):
    now = datetime.now()

    current_budget = (
        db.query(Budget)
        .filter(
            Budget.user_id == user_id,
            Budget.month == now.month,
            Budget.year == now.year,
        )
        .first()
    )

    if not current_budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No budget found for the current month.",
        )

    return current_budget


def get_all_budgets(
    db: Session,
    user_id: int,
):
    return (
        db.query(Budget)
        .filter(Budget.user_id == user_id)
        .order_by(
            Budget.year.desc(),
            Budget.month.desc(),
        )
        .all()
    )


def update_budget(
    db: Session,
    budget_id: int,
    budget: BudgetUpdate,
    user_id: int,
):
    db_budget = (
        db.query(Budget)
        .filter(
            Budget.id == budget_id,
            Budget.user_id == user_id,
        )
        .first()
    )

    if not db_budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found.",
        )

    db_budget.budget_amount = budget.budget_amount

    db.commit()
    db.refresh(db_budget)

    return db_budget


def delete_budget(
    db: Session,
    budget_id: int,
    user_id: int,
):
    db_budget = (
        db.query(Budget)
        .filter(
            Budget.id == budget_id,
            Budget.user_id == user_id,
        )
        .first()
    )

    if not db_budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found.",
        )

    db.delete(db_budget)
    db.commit()

    return {
        "message": "Budget deleted successfully."
    }


def analyze_budget(
    db: Session,
    user_id: int,
):
    now = datetime.now()

    budget = (
        db.query(Budget)
        .filter(
            Budget.user_id == user_id,
            Budget.month == now.month,
            Budget.year == now.year,
        )
        .first()
    )

    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Current month budget not found.",
        )

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id,
            extract("month", Expense.created_at) == now.month,
            extract("year", Expense.created_at) == now.year,
        )
        .all()
    )

    total_spent = sum(
        expense.amount
        for expense in expenses
    )

    remaining_budget = (
        budget.budget_amount - total_spent
    )

    utilization_percentage = (
        (total_spent / budget.budget_amount) * 100
        if budget.budget_amount > 0
        else 0
    )

    if utilization_percentage < 70:
        status = "Healthy"

    elif utilization_percentage < 90:
        status = "Within Budget"

    elif utilization_percentage <= 100:
        status = "Budget Almost Reached"

    else:
        status = "Over Budget"

    budget_exceeded = (
        total_spent > budget.budget_amount
    )

    amount_over_budget = (
        total_spent - budget.budget_amount
        if budget_exceeded
        else 0
    )

    return {
        "budget_amount": round(
            budget.budget_amount,
            2,
        ),
        "total_spent": round(
            total_spent,
            2,
        ),
        "remaining_budget": round(
            remaining_budget,
            2,
        ),
        "utilization_percentage": round(
            utilization_percentage,
            2,
        ),
        "status": status,
        "budget_exceeded": budget_exceeded,
        "amount_over_budget": round(
            amount_over_budget,
            2,
        ),
    }

def budget_dashboard(
    db: Session,
    user_id: int,
):
    analysis = analyze_budget(
        db=db,
        user_id=user_id,
    )

    today = datetime.now()

    last_day = calendar.monthrange(
        today.year,
        today.month,
    )[1]

    days_remaining = last_day - today.day + 1

    if analysis["remaining_budget"] > 0:
        daily_safe_spending = (
            analysis["remaining_budget"] / days_remaining
        )
    else:
        daily_safe_spending = 0

    return {
        **analysis,
        "days_remaining": days_remaining,
        "daily_safe_spending": round(
            daily_safe_spending,
            2,
        ),
    }