from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.dependencies.auth import (
    get_current_user,
)

from app.models.user import User
from app.models.expense import Expense
from app.models.budget import Budget

from app.schemas.budget_performance import (
    BudgetPerformanceResponse,
)

from app.services.budget_performance_service import (
    get_budget_performance,
)

router = APIRouter(
    prefix="/budget-performance",
    tags=["Budget Performance"],
)


@router.get(
    "/",
    response_model=BudgetPerformanceResponse,
)
def budget_performance(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):

    budget = (
        db.query(Budget)
        .filter(
            Budget.user_id
            == current_user.id
        )
        .order_by(
            Budget.id.desc()
        )
        .first()
    )

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id
            == current_user.id
        )
        .all()
    )

    return get_budget_performance(
        budget,
        expenses,
    )