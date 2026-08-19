from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.category_diversity import (
    CategoryDiversityResponse,
)

from app.services.category_diversity_service import (
    get_category_diversity,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/category-diversity",
    response_model=CategoryDiversityResponse,
)
def category_diversity(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Analyze the diversity of
    expense categories.
    """

    return get_category_diversity(
        db=db,
        user_id=current_user.id,
    )
