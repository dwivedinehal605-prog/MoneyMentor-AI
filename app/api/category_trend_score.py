from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.category_trend_score import (
    CategoryTrendScoreResponse,
)

from app.services.category_trend_score_service import (
    get_category_trend_score,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/category-trend-score",
    response_model=list[CategoryTrendScoreResponse],
)
def category_trend_score(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Analyze category-wise spending trend
    and assign a trend score.
    """

    return get_category_trend_score(
        db=db,
        user_id=current_user.id,
    )
