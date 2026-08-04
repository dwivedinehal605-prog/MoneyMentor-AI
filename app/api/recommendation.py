from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.recommendation import (
    RecommendationResponse,
)

from app.services.recommendation_service import (
    generate_recommendations,
)

router = APIRouter(
    prefix="/recommendations",
    tags=["AI Recommendations"],
)


@router.get(
    "/",
    response_model=RecommendationResponse,
)
def get_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return generate_recommendations(
        db=db,
        user_id=current_user.id,
    )