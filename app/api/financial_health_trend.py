from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.financial_health_trend import (
    FinancialHealthTrendResponse,
)

from app.services.financial_health_trend_service import (
    get_financial_health_trend,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/financial-health-trend",
    response_model=FinancialHealthTrendResponse,
)
def financial_health_trend(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Compare current and previous month
    financial health scores.
    """

    return get_financial_health_trend(
        db=db,
        user_id=current_user.id,
    )
