from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.spending_insight import (
    SpendingInsightResponse,
)

from app.services.spending_insight_service import (
    get_spending_insight,
)


router = APIRouter(
    prefix="/spending-insight",
    tags=["Spending Insights"],
)


@router.get(
    "",
    response_model=SpendingInsightResponse,
)
def spending_insight(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Generate spending insight
    based on the user's highest
    spending category.
    """

    return get_spending_insight(
        db=db,
        user_id=current_user.id,
    )