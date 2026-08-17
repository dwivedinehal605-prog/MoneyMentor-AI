from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.expense_frequency import (
    ExpenseFrequencyResponse,
)

from app.services.expense_frequency_service import (
    get_expense_frequency,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/expense-frequency",
    response_model=ExpenseFrequencyResponse,
)
def expense_frequency(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Analyze the user's expense
    transaction frequency.
    """

    return get_expense_frequency(
        db=db,
        user_id=current_user.id,
    )