from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.category_spending_risk import (
    CategorySpendingRiskResponse,
)

from app.services.category_spending_risk_service import (
    get_category_spending_risk,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/category-spending-risk",
    response_model=list[CategorySpendingRiskResponse],
)
def category_spending_risk(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Analyze spending risk for each
    expense category.
    """

    return get_category_spending_risk(
        db=db,
        user_id=current_user.id,
    )
