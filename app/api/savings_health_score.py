from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.savings_health_score import (
    SavingsHealthScoreResponse,
)

from app.services.savings_health_score_service import (
    get_savings_health_score,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/savings-health-score",
    response_model=SavingsHealthScoreResponse,
)
def savings_health_score(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Calculate the user's current
    monthly savings health score.
    """

    return get_savings_health_score(
        db=db,
        user_id=current_user.id,
    )
