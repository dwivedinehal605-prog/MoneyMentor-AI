from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.savings_income_ratio import (
    SavingsIncomeRatioResponse,
)

from app.services.savings_income_ratio_service import (
    get_savings_income_ratio,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/savings-income-ratio",
    response_model=SavingsIncomeRatioResponse,
)
def savings_income_ratio(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Analyze savings compared with total income.
    """

    return get_savings_income_ratio(
        db=db,
        user_id=current_user.id,
    )
