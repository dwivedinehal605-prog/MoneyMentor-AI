from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.savings_rate_trend import (
    SavingsRateTrendResponse,
)

from app.services.savings_rate_trend_service import (
    get_savings_rate_trend,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/savings-rate-trend",
    response_model=SavingsRateTrendResponse,
)
def savings_rate_trend(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Compare current and previous month
    savings rates.
    """

    return get_savings_rate_trend(
        db=db,
        user_id=current_user.id,
    )