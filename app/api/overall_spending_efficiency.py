from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.overall_spending_efficiency import (
    OverallSpendingEfficiencyResponse,
)

from app.services.overall_spending_efficiency_service import (
    get_overall_spending_efficiency,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/overall-spending-efficiency",
    response_model=OverallSpendingEfficiencyResponse,
)
def overall_spending_efficiency(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Analyze overall spending efficiency
    compared with total income.
    """

    return get_overall_spending_efficiency(
        db=db,
        user_id=current_user.id,
    )
