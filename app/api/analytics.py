from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.services.analytics_service import (
    get_total_expense,
    category_summary,
)

from app.schemas.category_analytics import (
    CategoryAnalyticsResponse,
)

from app.services.category_analytics_service import (
    get_category_analytics,
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/total")
def total(db: Session = Depends(get_db)):
    return get_total_expense(db)


@router.get("/category-summary")
def summary(db: Session = Depends(get_db)):
    return category_summary(db)


@router.get(
    "/category-wise",
    response_model=CategoryAnalyticsResponse,
)
def category_wise_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate category-wise
    expense analytics.
    """

    return get_category_analytics(
        db=db,
        user_id=current_user.id,
    )