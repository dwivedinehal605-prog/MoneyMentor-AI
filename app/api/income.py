from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.income import (
    IncomeCreate,
    IncomeUpdate,
    IncomeResponse
)

from app.services.income_service import (
    create_income,
    get_incomes,
    get_income,
    update_income,
    delete_income
)

router = APIRouter(
    prefix="/income",
    tags=["Income"]
)


@router.post("/", response_model=IncomeResponse)
def add_income(
    income: IncomeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_income(db, income, current_user.id)


@router.get("/", response_model=list[IncomeResponse])
def read_incomes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_incomes(db, current_user.id)


@router.get("/{income_id}", response_model=IncomeResponse)
def read_income(
    income_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    income = get_income(db, income_id, current_user.id)

    if not income:
        raise HTTPException(status_code=404, detail="Income not found")

    return income


@router.put("/{income_id}", response_model=IncomeResponse)
def edit_income(
    income_id: int,
    income: IncomeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_income = update_income(
        db,
        income_id,
        income,
        current_user.id
    )

    if not updated_income:
        raise HTTPException(status_code=404, detail="Income not found")

    return updated_income


@router.delete("/{income_id}")
def remove_income(
    income_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted_income = delete_income(
        db,
        income_id,
        current_user.id
    )

    if not deleted_income:
        raise HTTPException(status_code=404, detail="Income not found")

    return {"message": "Income deleted successfully"}