from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.spending_efficiency import (
    SpendingEfficiencyResponse,
)

from app.services.spending_efficiency_service import (
    get_spending_efficiency,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/spending-efficiency",
    response_model=SpendingEfficiencyResponse,
)
def spending_efficiency(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Evaluate current month spending
    efficiency relative to income.
    """

    return get_spending_efficiency(
        db=db,
        user_id=current_user.id,
    )
