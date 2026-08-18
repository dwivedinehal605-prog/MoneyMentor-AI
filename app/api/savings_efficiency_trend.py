from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.savings_efficiency_trend import (
    SavingsEfficiencyTrendResponse,
)

from app.services.savings_efficiency_trend_service import (
    get_savings_efficiency_trend,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/savings-efficiency-trend",
    response_model=SavingsEfficiencyTrendResponse,
)
def savings_efficiency_trend(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Compare current and previous month
    savings efficiency.
    """

    return get_savings_efficiency_trend(
        db=db,
        user_id=current_user.id,
    )
