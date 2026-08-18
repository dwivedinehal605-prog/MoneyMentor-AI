from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.expense_volatility import (
    ExpenseVolatilityResponse,
)

from app.services.expense_volatility_service import (
    get_expense_volatility,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/expense-volatility",
    response_model=ExpenseVolatilityResponse,
)
def expense_volatility(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Analyze monthly expense volatility.
    """

    return get_expense_volatility(
        db=db,
        user_id=current_user.id,
    )
