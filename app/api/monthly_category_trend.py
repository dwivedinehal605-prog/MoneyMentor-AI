from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.services.monthly_category_trend_service import (
    get_monthly_category_trend,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/monthly-category-trend",
)
def monthly_category_trend(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Compare category-wise expenses
    between the current and previous month.
    """

    return get_monthly_category_trend(
        db=db,
        user_id=current_user.id,
    )
