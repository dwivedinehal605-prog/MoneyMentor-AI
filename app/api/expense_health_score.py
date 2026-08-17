from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.expense_health_score import (
    ExpenseHealthScoreResponse,
)

from app.services.expense_health_score_service import (
    get_expense_health_score,
)


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/expense-health-score",
    response_model=ExpenseHealthScoreResponse,
)
def expense_health_score(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Calculate the user's current-month
    expense-to-income financial health score.
    """

    return get_expense_health_score(
        db=db,
        user_id=current_user.id,
    )