from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.savings_coverage import (
    SavingsCoverageResponse,
)

from app.services.savings_coverage_service import (
    get_savings_coverage,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/savings-coverage",
    response_model=SavingsCoverageResponse,
)
def savings_coverage(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Analyze how savings compare
    with total expenses.
    """

    return get_savings_coverage(
        db=db,
        user_id=current_user.id,
    )
