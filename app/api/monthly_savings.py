from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.monthly_savings import (
    MonthlySavingsResponse,
)

from app.services.monthly_savings_service import (
    get_monthly_savings,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/monthly-savings",
    response_model=MonthlySavingsResponse,
)
def monthly_savings(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Compare current and previous month
    savings.
    """

    return get_monthly_savings(
        db=db,
        user_id=current_user.id,
    )
