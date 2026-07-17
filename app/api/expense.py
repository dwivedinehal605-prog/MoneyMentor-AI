from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.database.database import get_db
from app.schemas.expense import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse
) 
from app.services.expense_service import (
    create_expense,
    get_expenses,
    delete_expense,
    update_expense
)
router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

@router.post("/", response_model=ExpenseResponse)
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_expense(
        db,
        expense,
        current_user.id
    )


@router.get("/", response_model=list[ExpenseResponse])
def read_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_expenses(
        db,
        current_user.id
    )

@router.delete("/{expense_id}")
def delete_expense_route(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expense = delete_expense(
        db,
        expense_id,
        current_user.id
    )

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return {
        "message": "Expense deleted successfully"
    }

@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense_route(
    expense_id: int,
    expense: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = update_expense(
        db,
        expense_id,
        current_user.id,
        expense
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return updated