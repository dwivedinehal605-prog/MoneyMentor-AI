from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.monthly_comparison import (
    MonthlyComparisonResponse,
)

from app.services.monthly_comparison_service import (
    get_monthly_comparison,
)


router = APIRouter(
    prefix="/monthly-comparison",
    tags=["Monthly Comparison"],
)


@router.get(
    "",
    response_model=MonthlyComparisonResponse,
)
def monthly_comparison(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Compare current month spending
    with previous month spending.
    """

    return get_monthly_comparison(
        db=db,
        user_id=current_user.id,
    )