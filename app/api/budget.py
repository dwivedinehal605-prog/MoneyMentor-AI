from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.budget import (
    BudgetCreate,
    BudgetUpdate,
    BudgetResponse,
)

from app.services.budget_service import (
    create_budget,
    get_current_budget,
    get_all_budgets,
    update_budget,
    delete_budget,
)

router = APIRouter(
    prefix="/budgets",
    tags=["Budgets"]
)

@router.post("/", response_model=BudgetResponse)
def add_budget(
    budget: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_budget(db, budget, current_user.id)


@router.get("/current", response_model=BudgetResponse)
def read_current_budget(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_current_budget(
        db,
        current_user.id
    )


@router.get("/", response_model=list[BudgetResponse])
def read_all_budgets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_budgets(
        db,
        current_user.id
    )


@router.put("/{budget_id}", response_model=BudgetResponse)
def edit_budget(
    budget_id: int,
    budget: BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_budget(
        db,
        budget_id,
        budget,
        current_user.id
    )


@router.delete("/{budget_id}")
def remove_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_budget(
        db,
        budget_id,
        current_user.id
    )