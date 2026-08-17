from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.expense_income_ratio import (
    ExpenseIncomeRatioResponse,
)

from app.services.expense_income_ratio_service import (
    get_expense_income_ratio,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/expense-income-ratio",
    response_model=ExpenseIncomeRatioResponse,
)
def expense_income_ratio(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Analyze current month expenses
    compared with current month income.
    """

    return get_expense_income_ratio(
        db=db,
        user_id=current_user.id,
    )
