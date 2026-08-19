from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.overall_spending_risk import (
    OverallSpendingRiskResponse,
)

from app.services.overall_spending_risk_service import (
    get_overall_spending_risk,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/overall-spending-risk",
    response_model=OverallSpendingRiskResponse,
)
def overall_spending_risk(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Analyze the user's overall
    spending risk.
    """

    return get_overall_spending_risk(
        db=db,
        user_id=current_user.id,
    )
