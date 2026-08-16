from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.spending_distribution import (
    SpendingDistributionResponse,
)

from app.services.spending_distribution_service import (
    get_spending_distribution,
)


router = APIRouter(
    prefix="/spending-distribution",
    tags=["Spending Distribution"],
)


@router.get(
    "",
    response_model=SpendingDistributionResponse,
)
def spending_distribution(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Generate category-wise spending
    distribution for the current user.
    """

    return get_spending_distribution(
        db=db,
        user_id=current_user.id,
    )