from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.schemas.budget import BudgetCreate, BudgetUpdate


def create_budget(
    db: Session,
    budget: BudgetCreate,
    user_id: int
):
    existing_budget = (
        db.query(Budget)
        .filter(
            Budget.user_id == user_id,
            Budget.month == budget.month,
            Budget.year == budget.year
        )
        .first()
    )

    if existing_budget:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Budget already exists for this month."
        )

    db_budget = Budget(
        user_id=user_id,
        month=budget.month,
        year=budget.year,
        budget_amount=budget.budget_amount
    )

    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)

    return db_budget


def get_current_budget(
    db: Session,
    user_id: int
):
    now = datetime.now()

    current_budget = (
        db.query(Budget)
        .filter(
            Budget.user_id == user_id,
            Budget.month == now.month,
            Budget.year == now.year
        )
        .first()
    )

    if not current_budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No budget found for the current month."
        )

    return current_budget


def get_all_budgets(
    db: Session,
    user_id: int
):
    return (
        db.query(Budget)
        .filter(Budget.user_id == user_id)
        .order_by(
            Budget.year.desc(),
            Budget.month.desc()
        )
        .all()
    )


def update_budget(
    db: Session,
    budget_id: int,
    budget: BudgetUpdate,
    user_id: int
):
    db_budget = (
        db.query(Budget)
        .filter(
            Budget.id == budget_id,
            Budget.user_id == user_id
        )
        .first()
    )

    if not db_budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found."
        )

    db_budget.budget_amount = budget.budget_amount

    db.commit()
    db.refresh(db_budget)

    return db_budget


def delete_budget(
    db: Session,
    budget_id: int,
    user_id: int
):
    db_budget = (
        db.query(Budget)
        .filter(
            Budget.id == budget_id,
            Budget.user_id == user_id
        )
        .first()
    )

    if not db_budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found."
        )

    db.delete(db_budget)
    db.commit()

    return {"message": "Budget deleted successfully."}