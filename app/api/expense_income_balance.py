from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.expense_income_balance import (
    ExpenseIncomeBalanceResponse,
)

from app.services.expense_income_balance_service import (
    get_expense_income_balance,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/expense-income-balance",
    response_model=ExpenseIncomeBalanceResponse,
)
def expense_income_balance(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Analyze the balance between
    total income and total expenses.
    """

    return get_expense_income_balance(
        db=db,
        user_id=current_user.id,
    )
